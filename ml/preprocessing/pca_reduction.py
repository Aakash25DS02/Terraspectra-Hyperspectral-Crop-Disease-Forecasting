import h5py
import numpy as np
from sklearn.decomposition import IncrementalPCA

try:
    from .normalization import HyperspectralNormalizer
except ImportError:
    from normalization import HyperspectralNormalizer


class HyperspectralPCA:
    """Reduce spectral bands using PCA fitted on training data."""

    def __init__(self, n_components=10):
        self.n_components = n_components
        self.model = IncrementalPCA(n_components=n_components)

    def fit(self, images, batch_size=4096):
        if images.ndim != 4:
            raise ValueError("Expected (N, H, W, Bands)")

        pixels = images.reshape(-1, images.shape[-1])

        if pixels.shape[1] < self.n_components:
            raise ValueError("PCA components exceed band count")

        for start in range(0, len(pixels), batch_size):
            batch = pixels[start:start + batch_size]

            if len(batch) >= self.n_components:
                self.model.partial_fit(batch)

        return self

    def transform(self, images, batch_size=4096):
        if images.ndim != 4:
            raise ValueError("Expected (N, H, W, Bands)")

        n, h, w, bands = images.shape
        pixels = images.reshape(-1, bands)
        result = np.empty(
            (len(pixels), self.n_components),
            dtype=np.float32
        )

        for start in range(0, len(pixels), batch_size):
            batch = pixels[start:start + batch_size]
            result[start:start + len(batch)] = (
                self.model.transform(batch)
            )

        return result.reshape(n, h, w, self.n_components)


if __name__ == "__main__":
    with h5py.File("data/synthetic/synthetic_data.h5", "r") as f:
        train_images = f["images"][:20]
        test_images = f["images"][20:25]

    print("Original shape:", train_images.shape)

    normalizer = HyperspectralNormalizer()
    train_normalized = normalizer.fit_transform(train_images)
    test_normalized = normalizer.transform(test_images)

    pca = HyperspectralPCA(n_components=10)
    pca.fit(train_normalized)

    train_reduced = pca.transform(train_normalized)
    test_reduced = pca.transform(test_normalized)

    print("Reduced training shape:", train_reduced.shape)
    print("Reduced test shape:", test_reduced.shape)
    print(
        "Explained variance:",
        pca.model.explained_variance_ratio_.sum()
    )

    assert train_reduced.shape == (20, 64, 64, 10)
    assert test_reduced.shape == (5, 64, 64, 10)
    assert np.isfinite(train_reduced).all()
    assert np.isfinite(test_reduced).all()

    print("PCA test PASSED!")
