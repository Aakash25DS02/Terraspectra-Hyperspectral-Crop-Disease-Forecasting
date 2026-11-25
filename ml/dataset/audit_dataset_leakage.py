import csv
import hashlib
import re
from pathlib import Path
from collections import defaultdict, Counter

import numpy as np
import rasterio


ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data/real/kaggle_2026"
REPORT_DIR = ROOT / "reports/real"

EXPECTED_BANDS = 125
EXPECTED_SHAPE = (125, 32, 32)

CLASS_MAP = {
    "Healthy": 0,
    "Rust": 1,
    "Other": 2,
}

PREFIX_MAP = {
    "Health": "Healthy",
    "Rust": "Rust",
    "Other": "Other",
}


def load_manifest(filename, split):
    records = []

    with open(DATA_DIR / filename, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            records.append({
                "filepath": row["filepath"],
                "class_name": row["class_name"],
                "class_id": int(row["class_id"]),
                "split": split,
            })

    return records


def calculate_image_hash(filepath):
    path = ROOT / filepath

    with rasterio.open(path) as src:

        if src.count not in (125, 126):
            raise ValueError(
                f"Unexpected band count: {src.count}"
            )

        if src.count == 126:
            extra_band = src.read(126)

            if not np.all(extra_band == 65535):
                raise ValueError("Invalid extra band")

        image = src.read(
            list(range(1, EXPECTED_BANDS + 1))
        )

    if image.shape != EXPECTED_SHAPE:
        raise ValueError(
            f"Unexpected image shape: {image.shape}"
        )

    if not np.any(image):
        raise ValueError("All-zero hyperspectral image")

    image = np.ascontiguousarray(
        image, dtype="<u2"
    ) if image.dtype.kind == "u" and image.dtype.itemsize == 2 else None

    if image is None:
        raise ValueError("Expected uint16 pixel data")

    return hashlib.sha256(image.tobytes()).hexdigest()


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    train_records = load_manifest(
        "train_manifest.csv", "train"
    )

    val_records = load_manifest(
        "val_manifest.csv", "validation"
    )

    records = train_records + val_records

    print("=" * 60)
    print("TERRASPECTRA DATASET LEAKAGE AUDIT")
    print("=" * 60)

    print(f"Training samples: {len(train_records)}")
    print(f"Validation samples: {len(val_records)}")
    print(f"Total samples: {len(records)}")

    train_paths = {
        (ROOT / r["filepath"]).resolve()
        for r in train_records
    }

    val_paths = {
        (ROOT / r["filepath"]).resolve()
        for r in val_records
    }

    path_overlap = train_paths & val_paths

    repeated_paths = {
        path: count
        for path, count in Counter(
            (ROOT / r["filepath"]).resolve()
            for r in records
        ).items()
        if count > 1
    }

    hash_groups = defaultdict(list)
    filename_patterns = Counter()
    errors = []
    label_mismatches = []

    print("\nScanning hyperspectral images...")

    for index, record in enumerate(records, start=1):

        filename = Path(record["filepath"]).name

        match = re.fullmatch(
            r"(Health|Rust|Other)_hyper_(\d+)\.tif",
            filename
        )

        if match:
            prefix = match.group(1)
            filename_patterns[prefix] += 1

            if PREFIX_MAP[prefix] != record["class_name"]:
                label_mismatches.append(record)
        else:
            filename_patterns["Unknown"] += 1

        if CLASS_MAP.get(record["class_name"]) != record["class_id"]:
            label_mismatches.append(record)

        try:
            image_hash = calculate_image_hash(
                record["filepath"]
            )

            hash_groups[image_hash].append(record)

        except Exception as error:
            errors.append({
                "filepath": record["filepath"],
                "error": str(error),
            })

        if index % 50 == 0 or index == len(records):
            print(f"Processed {index}/{len(records)}")

    duplicate_groups = {
        key: group
        for key, group in hash_groups.items()
        if len(group) > 1
    }

    cross_split_groups = {
        key: group
        for key, group in duplicate_groups.items()
        if len({r["split"] for r in group}) > 1
    }

    conflicting_labels = {
        key: group
        for key, group in duplicate_groups.items()
        if len({r["class_id"] for r in group}) > 1
    }

    summary = [
        f"Training samples: {len(train_records)}",
        f"Validation samples: {len(val_records)}",
        f"Total samples: {len(records)}",
        f"Successfully hashed: {len(records) - len(errors)}",
        f"Unique image hashes: {len(hash_groups)}",
        f"Overlapping file paths: {len(path_overlap)}",
        f"Repeated file paths: {len(repeated_paths)}",
        f"Exact duplicate groups: {len(duplicate_groups)}",
        f"Cross-split duplicate groups: {len(cross_split_groups)}",
        f"Conflicting-label duplicate groups: {len(conflicting_labels)}",
        f"Label mismatch checks failed: {len(label_mismatches)}",
        f"Image processing errors: {len(errors)}",
    ]

    print("\n" + "=" * 60)
    print("AUDIT RESULTS")
    print("=" * 60)

    for line in summary:
        print(line)

    print("\nFilename patterns:")

    for pattern, count in sorted(filename_patterns.items()):
        print(f"{pattern}: {count}")

    duplicate_report = REPORT_DIR / "dataset_duplicates.csv"

    with open(duplicate_report, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "image_hash",
            "split",
            "class_name",
            "class_id",
            "filepath",
            "cross_split",
            "conflicting_labels",
        ])

        for image_hash, group in duplicate_groups.items():
            for record in group:
                writer.writerow([
                    image_hash,
                    record["split"],
                    record["class_name"],
                    record["class_id"],
                    record["filepath"],
                    image_hash in cross_split_groups,
                    image_hash in conflicting_labels,
                ])

    if errors:
        status = "INCOMPLETE: Image processing errors detected."

    elif (
        path_overlap
        or repeated_paths
        or duplicate_groups
        or label_mismatches
    ):
        status = "REVIEW REQUIRED: Dataset issues detected."

    else:
        status = "PASSED: No exact duplicates or path overlap detected."

    limitation = (
        "Exact hashing cannot rule out near-duplicates, "
        "shared plants, or acquisition-level leakage."
    )

    report_path = REPORT_DIR / "dataset_leakage_audit.txt"

    with open(report_path, "w") as file:
        file.write("TERRASPECTRA DATASET LEAKAGE AUDIT\n\n")
        file.write("\n".join(summary))

        file.write("\n\nFilename patterns:\n")

        for pattern, count in sorted(filename_patterns.items()):
            file.write(f"{pattern}: {count}\n")

        for path, count in repeated_paths.items():
            file.write(f"\nRepeated path: {path} ({count})")

        for record in label_mismatches:
            file.write(f"\nLabel mismatch: {record}")

        for error in errors:
            file.write(f"\nProcessing error: {error}")

        file.write(f"\n\nStatus: {status}\n")
        file.write(f"\nLimitation: {limitation}\n")

    print(f"\nStatus: {status}")
    print(f"Limitation: {limitation}")

    print(f"\nAudit report: {report_path}")
    print(f"Duplicate report: {duplicate_report}")


if __name__ == "__main__":
    main()
