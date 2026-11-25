import sys
from pathlib import Path

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.cnn3d import HyperspectralCNN3D_Simplified
from ml.token_embedding import SpatialSpectralTokenEmbedding
from ml.dataset.real_data_loader import RealHyperspectralDataset


def main():

    print("=" * 60)
    print("TERRASPECTRA REAL TOKEN EMBEDDING TEST")
    print("=" * 60)

    torch.manual_seed(42)

    device = torch.device(
        "mps" if torch.backends.mps.is_available() else "cpu"
    )

    print(f"Device: {device}")

    data_dir = ROOT / "data/real/kaggle_2026"

    checkpoint_path = (
        ROOT / "checkpoints/real/"
        "cnn3d_wheat_standardized_best.pth"
    )

    dataset = RealHyperspectralDataset(
        manifest_path=data_dir / "train_manifest.csv",
        normalization="per_band",
        stats_path=data_dir / "band_normalization.npz",
    )

    loader = DataLoader(
        dataset,
        batch_size=2,
        shuffle=False,
        num_workers=0,
    )

    images, labels = next(iter(loader))

    images = images.to(device)

    print(f"\nInput image shape: {images.shape}")
    print(f"Actual labels: {labels.tolist()}")

    model = HyperspectralCNN3D_Simplified(
        num_classes=3,
        num_bands=125,
        patch_size=32,
    )

    checkpoint = torch.load(
        checkpoint_path,
        map_location="cpu",
        weights_only=False,
    )

    model.load_state_dict(
        checkpoint["model_state_dict"],
        strict=True,
    )

    model = model.to(device)
    model.eval()

    print("\nExisting checkpoint loaded successfully!")

    embedder = SpatialSpectralTokenEmbedding(
        in_channels=64,
        embed_dim=256,
        max_tokens=240,
    ).to(device)

    embedder.eval()

    with torch.no_grad():

        features = model.extract_features(images)

        tokens = embedder(features)

        predictions = model(images)

        original = model.pool1(
            F.relu(model.bn1(model.conv1(images)))
        )

        original = model.pool2(
            F.relu(model.bn2(model.conv2(original)))
        )

        original = model.pool3(
            F.relu(model.bn3(model.conv3(original)))
        )

        original = original.view(original.size(0), -1)
        original = F.relu(model.fc1(original))
        original = model.dropout(original)
        original = model.fc2(original)

    print(f"\nCNN feature map shape: {features.shape}")
    print(f"Token sequence shape: {tokens.shape}")
    print(f"Classification output shape: {predictions.shape}")

    assert features.shape == (2, 64, 15, 4, 4), (
        "Unexpected CNN feature dimensions"
    )

    assert tokens.shape == (2, 240, 256), (
        "Unexpected token dimensions"
    )

    assert predictions.shape == (2, 3), (
        "Unexpected classification dimensions"
    )

    assert torch.isfinite(features).all(), (
        "Invalid CNN feature values"
    )

    assert torch.isfinite(tokens).all(), (
        "Invalid token values"
    )

    assert torch.isfinite(predictions).all(), (
        "Invalid classification values"
    )

    torch.testing.assert_close(predictions, original)

    print("\nFeature extraction test: PASSED")
    print("Token embedding test: PASSED")
    print("Numerical stability test: PASSED")
    print("Checkpoint compatibility test: PASSED")
    print("Original classification behavior test: PASSED")

    print("\n" + "=" * 60)
    print("ALL INTEGRATION TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    main()
