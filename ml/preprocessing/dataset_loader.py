
from pathlib import Path

import h5py

# Project paths
DATASET_PATH = Path("datasets/raw/synthetic_data.h5")
CLASS_NAMES_PATH = Path("datasets/sample/class_names.txt")


def load_class_names():
    """Load numeric class labels and their readable names."""
    if not CLASS_NAMES_PATH.exists():
        raise FileNotFoundError(
            f"Class names file not found: {CLASS_NAMES_PATH}"
        )

    class_names = {}

    with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            label, name = line.split(":", 1)
            class_names[int(label.strip())] = name.strip()

    return class_names


def get_dataset_info():
    """Read dataset metadata without loading all images into memory."""
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Hyperspectral dataset not found: {DATASET_PATH}"
        )

    class_names = load_class_names()

    with h5py.File(DATASET_PATH, "r") as file:
        images_shape = file["images"].shape
        labels_shape = file["labels"].shape
        wavelengths_shape = file["wavelengths"].shape

        unique_labels = sorted(
            set(file["labels"][:].tolist())
        )

        label_counts = {
            int(label): int((file["labels"][:] == label).sum())
            for label in unique_labels
        }

        return {
            "total_samples": images_shape[0],
            "image_height": images_shape[1],
            "image_width": images_shape[2],
            "spectral_bands": images_shape[3],
            "labels_count": labels_shape[0],
            "wavelength_count": wavelengths_shape[0],
            "classes": {
                str(label): class_names.get(label, "unknown")
                for label in unique_labels
            },
            "class_distribution": {
                class_names.get(label, "unknown"): count
                for label, count in label_counts.items()
            },
        }


if __name__ == "__main__":
    info = get_dataset_info()

    print("\n===== TerraSpectra Dataset Information =====")

    for key, value in info.items():
        print(f"{key}: {value}")

    print("\n===== Dataset Loading Completed =====")
