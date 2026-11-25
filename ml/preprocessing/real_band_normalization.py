import csv
import warnings
from pathlib import Path

import numpy as np
import rasterio


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MANIFEST = (
    PROJECT_ROOT
    / "data/real/kaggle_2026/train_manifest.csv"
)

OUTPUT = (
    PROJECT_ROOT
    / "data/real/kaggle_2026/band_normalization.npz"
)

NUM_BANDS = 125


def calculate_band_statistics():
    if not MANIFEST.exists():
        raise FileNotFoundError(
            f"Training manifest not found: {MANIFEST}"
        )

    with MANIFEST.open(newline="") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        raise ValueError("Training manifest is empty.")

    band_sum = np.zeros(NUM_BANDS, dtype=np.float64)
    band_sum_sq = np.zeros(NUM_BANDS, dtype=np.float64)

    total_pixels_per_band = 0

    for row in rows:
        image_path = Path(row["filepath"])

        if not image_path.is_absolute():
            image_path = PROJECT_ROOT / image_path

        with warnings.catch_warnings():
            warnings.simplefilter(
                "ignore",
                rasterio.errors.NotGeoreferencedWarning
            )

            with rasterio.open(image_path) as src:
                if src.count not in (125, 126):
                    raise ValueError(
                        f"Unexpected band count: {src.count}"
                    )

                if src.count == 126:
                    extra = src.read(126)

                    if not np.all(extra == 65535):
                        raise ValueError(
                            f"Invalid extra band: {image_path}"
                        )

                image = src.read(
                    indexes=list(range(1, NUM_BANDS + 1))
                ).astype(np.float64)

        if image.shape != (125, 32, 32):
            raise ValueError(
                f"Unexpected shape: {image.shape}"
            )

        if not np.isfinite(image).all():
            raise ValueError(
                f"Non-finite values: {image_path}"
            )

        band_sum += image.sum(axis=(1, 2))
        band_sum_sq += np.square(image).sum(axis=(1, 2))

        total_pixels_per_band += image.shape[1] * image.shape[2]

    mean = band_sum / total_pixels_per_band

    variance = (
        band_sum_sq / total_pixels_per_band
        - np.square(mean)
    )

    variance = np.maximum(variance, 0.0)
    std = np.sqrt(variance)

    near_constant = std < 1e-6
    std[near_constant] = 1.0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    np.savez(
        OUTPUT,
        mean=mean.astype(np.float32),
        std=std.astype(np.float32),
        num_bands=np.array(NUM_BANDS),
    )

    print("TERRASPECTRA PER-BAND NORMALIZATION")
    print("----------------------------------")
    print("Training images:", len(rows))
    print("Spectral bands:", NUM_BANDS)
    print("Pixels per band:", total_pixels_per_band)
    print("Mean range:", round(float(mean.min()), 4),
          "to", round(float(mean.max()), 4))
    print("Std range:", round(float(std.min()), 4),
          "to", round(float(std.max()), 4))
    print("Near-constant bands:", int(near_constant.sum()))
    print("Saved statistics:", OUTPUT)
    print("\nNormalization statistics generated successfully!")


if __name__ == "__main__":
    calculate_band_statistics()
