from pathlib import Path

import h5py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


DATASET_PATH = Path("data/synthetic/synthetic_data.h5")
OUTPUT_PATH = Path("docs/week2_dataset_gallery.png")


def create_false_color(cube):
    """Convert a hyperspectral cube into a displayable image."""
    if cube.ndim != 3:
        raise ValueError(f"Expected (H, W, Bands), got {cube.shape}")

    bands = cube.shape[-1]

    if bands < 3:
        raise ValueError("At least 3 spectral bands are required")

    indices = [
        int(0.70 * (bands - 1)),
        int(0.40 * (bands - 1)),
        int(0.10 * (bands - 1)),
    ]

    rgb = cube[:, :, indices].astype(np.float32)
    rgb = np.where(np.isfinite(rgb), rgb, np.nan)

    for channel in range(3):
        values = rgb[:, :, channel]
        valid = values[np.isfinite(values)]

        if valid.size == 0:
            rgb[:, :, channel] = 0
            continue

        low, high = np.percentile(valid, [2, 98])

        if high <= low:
            rgb[:, :, channel] = 0
        else:
            rgb[:, :, channel] = np.clip(
                (values - low) / (high - low), 0, 1
            )

    return np.nan_to_num(rgb, nan=0.0)


def create_gallery():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(DATASET_PATH)

    with h5py.File(DATASET_PATH, "r") as file:
        images = file["images"]
        labels = file["labels"]

        if images.ndim != 4:
            raise ValueError("Expected (N, H, W, Bands)")

        if len(images) != len(labels):
            raise ValueError("Image and label counts differ")

        count = min(12, len(images))
        if count == 0:
            raise ValueError("Dataset is empty")

        fig, axes = plt.subplots(3, 4, figsize=(14, 11))

        for i, ax in enumerate(axes.flat):
            if i >= count:
                ax.axis("off")
                continue

            cube = images[i]
            rgb = create_false_color(cube)

            ax.imshow(rgb)
            ax.set_title(
                f"Sample {i + 1} | Class {labels[i]}"
            )
            ax.axis("off")

        fig.suptitle(
            "TerraSpectra - Hyperspectral Dataset Gallery",
            fontsize=16,
            fontweight="bold",
        )

        plt.tight_layout()
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(OUTPUT_PATH, dpi=160)
        plt.close(fig)

        print("Dataset shape:", images.shape)
        print("Total samples:", len(images))
        print("Gallery samples:", count)
        print("Gallery saved:", OUTPUT_PATH)
        print("DATASET VISUALIZATION PASSED!")


if __name__ == "__main__":
    create_gallery()
