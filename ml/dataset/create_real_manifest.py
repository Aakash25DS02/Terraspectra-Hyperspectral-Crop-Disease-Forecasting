from pathlib import Path
from collections import Counter
import csv
import warnings

import numpy as np
import rasterio

ROOT = Path("data/real/kaggle_2026/Kaggle_Prepared")
TRAIN_DIR = ROOT / "train" / "HS"
OUTPUT = Path("data/real/kaggle_2026/clean_train_manifest.csv")

LABELS = {
    "health": ("Healthy", 0),
    "rust": ("Rust", 1),
    "other": ("Other", 2),
}

def inspect_image(path):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter(
                "ignore",
                rasterio.errors.NotGeoreferencedWarning
            )

            with rasterio.open(path) as src:
                if (src.height, src.width) != (32, 32):
                    return False, "incorrect_dimensions"

                if src.count == 125:
                    data = src.read()

                elif src.count == 126:
                    extra = src.read(126)

                    if not np.all(extra == 65535):
                        return False, "unexpected_extra_band"

                    data = src.read(indexes=list(range(1, 126)))

                else:
                    return False, "incorrect_band_count"

                if not np.any(data != 0):
                    return False, "all_zero"

                return True, "valid"

    except Exception as error:
        return False, f"read_error:{type(error).__name__}"

def main():
    if not TRAIN_DIR.is_dir():
        raise FileNotFoundError(f"Missing dataset folder: {TRAIN_DIR}")

    rows = []
    excluded = Counter()

    files = sorted(TRAIN_DIR.glob("*.tif"))

    for path in files:
        name = path.stem.lower()

        label = next(
            (value for prefix, value in LABELS.items()
             if name.startswith(prefix)),
            None
        )

        if label is None:
            excluded["unknown_label"] += 1
            continue

        valid, reason = inspect_image(path)

        if not valid:
            excluded[reason] += 1
            continue

        class_name, class_id = label

        rows.append({
            "filepath": str(path),
            "class_name": class_name,
            "class_id": class_id,
        })

    if not rows:
        raise RuntimeError("No valid labeled images found.")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["filepath", "class_name", "class_id"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print("TERRASPECTRA REAL DATASET MANIFEST")
    print("---------------------------------")
    print("Total inspected:", len(files))
    print("Valid labeled images:", len(rows))
    print("Class distribution:")

    counts = Counter(row["class_name"] for row in rows)
    for class_name in ["Healthy", "Rust", "Other"]:
        print(f"  {class_name}: {counts[class_name]}")

    print("Excluded:", dict(excluded))
    print("Saved:", OUTPUT)

if __name__ == "__main__":
    main()
