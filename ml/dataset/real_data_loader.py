from pathlib import Path
import csv
import warnings

import numpy as np
import rasterio
import torch
from torch.utils.data import Dataset, DataLoader


class RealHyperspectralDataset(Dataset):
    def __init__(self, manifest_path):
        self.manifest_path = Path(manifest_path)

        with self.manifest_path.open(newline="") as f:
            self.rows = list(csv.DictReader(f))

        if not self.rows:
            raise ValueError("Manifest is empty")

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, index):
        row = self.rows[index]
        path = Path(row["filepath"])

        with warnings.catch_warnings():
            warnings.simplefilter(
                "ignore",
                rasterio.errors.NotGeoreferencedWarning
            )

            with rasterio.open(path) as src:
                if src.count == 125:
                    image = src.read()
                elif src.count == 126:
                    extra = src.read(126)

                    if not np.all(extra == 65535):
                        raise ValueError(f"Unexpected extra band: {path}")

                    image = src.read(indexes=list(range(1, 126)))
                else:
                    raise ValueError(f"Unexpected band count: {src.count}")

        if image.shape != (125, 32, 32):
            raise ValueError(f"Unexpected shape: {image.shape}")

        image = image.astype(np.float32)

        if not np.isfinite(image).all() or not np.any(image):
            raise ValueError(f"Invalid image: {path}")

        image = image / 65535.0

        image = torch.from_numpy(image).unsqueeze(0)
        label = torch.tensor(int(row["class_id"]), dtype=torch.long)

        return image, label


def main():
    root = Path("data/real/kaggle_2026")
    train = RealHyperspectralDataset(root / "train_manifest.csv")
    val = RealHyperspectralDataset(root / "val_manifest.csv")

    train_loader = DataLoader(train, batch_size=4, shuffle=True, num_workers=0)
    val_loader = DataLoader(val, batch_size=4, shuffle=False, num_workers=0)

    images, labels = next(iter(train_loader))

    print("TERRASPECTRA REAL DATA LOADER TEST")
    print("---------------------------------")
    print("Training images:", len(train))
    print("Validation images:", len(val))
    print("Batch shape:", tuple(images.shape))
    print("Labels:", labels.tolist())
    print("Data type:", images.dtype)
    print("Minimum value:", images.min().item())
    print("Maximum value:", images.max().item())

    assert images.shape == (4, 1, 125, 32, 32)
    assert torch.isfinite(images).all()
    assert images.min() >= 0
    assert images.max() <= 1

    print("\nReal data loader PASSED!")


if __name__ == "__main__":
    main()
