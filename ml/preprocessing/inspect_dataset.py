
from pathlib import Path
import h5py

# Path to the synthetic hyperspectral dataset
DATASET_PATH = Path("datasets/raw/synthetic_data.h5")


def inspect_dataset():
    if not DATASET_PATH.exists():
        print("Dataset file not found!")
        print(f"Expected location: {DATASET_PATH}")
        print("Please place synthetic_data.h5 inside datasets/raw/")
        return

    print("\n===== TerraSpectra Dataset Inspection =====")

    with h5py.File(DATASET_PATH, "r") as file:

        def show_item(name, item):
            if isinstance(item, h5py.Dataset):
                print(f"\nDataset name: {name}")
                print(f"Shape: {item.shape}")
                print(f"Data type: {item.dtype}")
            else:
                print(f"\nGroup: {name}")

        file.visititems(show_item)

    print("\n===== Inspection Completed =====")


if __name__ == "__main__":
    inspect_dataset()
