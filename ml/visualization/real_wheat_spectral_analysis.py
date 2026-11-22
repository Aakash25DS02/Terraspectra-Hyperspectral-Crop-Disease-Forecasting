import csv
import warnings
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import rasterio


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MANIFEST = (
    PROJECT_ROOT
    / "data/real/kaggle_2026/train_manifest.csv"
)

OUTPUT = (
    PROJECT_ROOT
    / "docs/real_wheat_spectral_signatures.png"
)

CLASS_NAMES = ["Healthy", "Rust", "Other"]
NUM_BANDS = 125


def analyze_spectral_signatures():
    if not MANIFEST.exists():
        raise FileNotFoundError(
            f"Training manifest not found: {MANIFEST}"
        )

    with MANIFEST.open(newline="") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        raise ValueError("Training manifest is empty.")

    spectra = defaultdict(list)

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
                    extra_band = src.read(126)

                    if not np.all(extra_band == 65535):
                        raise ValueError(
                            f"Invalid extra band: {image_path}"
                        )

                image = src.read(
                    indexes=list(range(1, NUM_BANDS + 1))
                ).astype(np.float32)

        if image.shape != (125, 32, 32):
            raise ValueError(
                f"Unexpected image shape: {image.shape}"
            )

        if not np.isfinite(image).all():
            raise ValueError(
                f"Non-finite pixel values: {image_path}"
            )

        class_name = row["class_name"]

        if class_name not in CLASS_NAMES:
            raise ValueError(
                f"Unknown class: {class_name}"
            )

        mean_spectrum = image.mean(axis=(1, 2))
        spectra[class_name].append(mean_spectrum)

    plt.figure(figsize=(11, 6))

    for class_name in CLASS_NAMES:
        if not spectra[class_name]:
            raise ValueError(
                f"No samples for class: {class_name}"
            )

        values = np.stack(spectra[class_name])
        mean_spectrum = values.mean(axis=0)

        plt.plot(
            np.arange(1, NUM_BANDS + 1),
            mean_spectrum,
            label=f"{class_name} (n={len(values)})",
            linewidth=2
        )

    plt.xlabel("Spectral Band Index")
    plt.ylabel("Mean Pixel Intensity")
    plt.title(
        "TerraSpectra: Real Wheat Class Spectral Profiles"
    )
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT, dpi=180)
    plt.close()

    print("TERRASPECTRA SPECTRAL SIGNATURE ANALYSIS")
    print("---------------------------------------")
    print("Training images analyzed:", len(rows))
    print("Spectral bands:", NUM_BANDS)

    for class_name in CLASS_NAMES:
        print(
            f"{class_name}: {len(spectra[class_name])} images"
        )

    print("Saved plot:", OUTPUT)
    print("\nSpectral analysis completed!")


if __name__ == "__main__":
    analyze_spectral_signatures()
