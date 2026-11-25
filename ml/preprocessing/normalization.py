import numpy as np


class HyperspectralNormalizer:
    """Per-band min-max normalization for hyperspectral images."""

    def __init__(self):
        self.band_min = None
        self.band_max = None

    def fit(self, images):
        images = np.asarray(images, dtype=np.float32)

        if images.ndim != 4:
            raise ValueError(
                f"Expected (N, H, W, Bands), got {images.shape}"
            )

        finite = np.isfinite(images)

        if not finite.any(axis=(0, 1, 2)).all():
            raise ValueError("A spectral band has no valid values")

        self.band_min = np.min(
            np.where(finite, images, np.inf),
            axis=(0, 1, 2)
        )

        self.band_max = np.max(
            np.where(finite, images, -np.inf),
            axis=(0, 1, 2)
        )

        return self

    def transform(self, images):
        if self.band_min is None:
            raise RuntimeError("Call fit() before transform()")

        images = np.asarray(images, dtype=np.float32)

        if images.ndim != 4 or images.shape[-1] != len(self.band_min):
            raise ValueError("Invalid image shape or band count")

        denominator = np.maximum(
            self.band_max - self.band_min, 1e-8
        )

        normalized = (images - self.band_min) / denominator
        normalized = np.clip(normalized, 0.0, 1.0)
        normalized = np.where(
            np.isfinite(normalized), normalized, 0.0
        )

        return normalized.astype(np.float32)

    def fit_transform(self, images):
        return self.fit(images).transform(images)


if __name__ == "__main__":
    import h5py

    with h5py.File("data/synthetic/synthetic_data.h5", "r") as f:
        images = f["images"][:]

    print("Original shape:", images.shape)

    split = int(len(images) * 0.8)
    train_images = images[:split]
    test_images = images[split:]

    normalizer = HyperspectralNormalizer()

    train_normalized = normalizer.fit_transform(train_images)
    test_normalized = normalizer.transform(test_images)

    print("Training shape:", train_normalized.shape)
    print("Training range:", train_normalized.min(), train_normalized.max())
    print("Test shape:", test_normalized.shape)
    print("Test range:", test_normalized.min(), test_normalized.max())

    assert np.isfinite(train_normalized).all()
    assert np.isfinite(test_normalized).all()
    assert train_normalized.min() >= 0
    assert train_normalized.max() <= 1

    print("Normalization test PASSED!")
