from pathlib import Path
from collections import Counter
import csv

from sklearn.model_selection import train_test_split

ROOT = Path("data/real/kaggle_2026")
SOURCE = ROOT / "clean_train_manifest.csv"
TRAIN_OUTPUT = ROOT / "train_manifest.csv"
VAL_OUTPUT = ROOT / "val_manifest.csv"

def save_csv(path, rows):
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["filepath", "class_name", "class_id"]
        )
        writer.writeheader()
        writer.writerows(rows)

def show_distribution(name, rows):
    counts = Counter(row["class_name"] for row in rows)

    print(f"\n{name}: {len(rows)} images")

    for class_name in ["Healthy", "Rust", "Other"]:
        print(f"  {class_name}: {counts[class_name]}")

def main():
    if not SOURCE.exists():
        raise FileNotFoundError(f"Missing manifest: {SOURCE}")

    with SOURCE.open(newline="") as file:
        rows = list(csv.DictReader(file))

    if len(rows) != 575:
        raise ValueError(
            f"Expected 575 valid images, found {len(rows)}"
        )

    paths = [row["filepath"] for row in rows]

    if len(paths) != len(set(paths)):
        raise ValueError("Duplicate filepaths detected.")

    for path in paths:
        if not Path(path).is_file():
            raise FileNotFoundError(path)

    train_rows, val_rows = train_test_split(
        rows,
        test_size=0.20,
        random_state=42,
        stratify=[row["class_id"] for row in rows]
    )

    train_paths = {row["filepath"] for row in train_rows}
    val_paths = {row["filepath"] for row in val_rows}

    assert train_paths.isdisjoint(val_paths)
    assert len(train_rows) + len(val_rows) == len(rows)

    save_csv(TRAIN_OUTPUT, train_rows)
    save_csv(VAL_OUTPUT, val_rows)

    print("TERRASPECTRA REAL DATASET SPLIT")
    print("--------------------------------")

    show_distribution("TRAINING", train_rows)
    show_distribution("VALIDATION", val_rows)

    print("\nTrain/validation overlap: 0")
    print("Saved:", TRAIN_OUTPUT)
    print("Saved:", VAL_OUTPUT)
    print("\nDataset split PASSED!")

if __name__ == "__main__":
    main()
