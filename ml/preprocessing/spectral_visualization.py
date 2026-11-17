from pathlib import Path

import h5py
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


def plot_spectral_signatures(
    h5_path="data/synthetic/synthetic_data.h5",
    output_path="docs/spectral_signatures.png",
    num_samples=5,
):
    with h5py.File(h5_path, "r") as f:
        images = f["images"]
        wavelengths = f["wavelengths"][:]

        if images.ndim != 4:
            raise ValueError("Expected (N, H, W, Bands)")

        if len(wavelengths) != images.shape[-1]:
            raise ValueError("Wavelength count does not match bands")

        count = min(num_samples, images.shape[0])

        if count < 1:
            raise ValueError("Dataset contains no samples")

        plt.figure(figsize=(10, 6))

        for i in range(count):
            cube = images[i]
            signature = np.nanmean(cube, axis=(0, 1))

            plt.plot(
                wavelengths,
                signature,
                label=f"Sample {i + 1}",
            )

    plt.xlabel("Wavelength (dataset units)")
    plt.ylabel("Mean spectral value")
    plt.title("TerraSpectra - Spectral Signatures")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    Path(output_path).parent.mkdir(
        parents=True, exist_ok=True
    )

    plt.savefig(output_path, dpi=150)
    plt.close()

    print("Spectral visualization saved:", output_path)
    print("Samples plotted:", count)
    print("Spectral bands:", len(wavelengths))


if __name__ == "__main__":
    plot_spectral_signatures()
