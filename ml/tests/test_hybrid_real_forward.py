import sys
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.dataset.real_data_loader import (
    RealHyperspectralDataset,
)

from ml.hybrid_cnn_vit import (
    HyperspectralHybridCNNViT,
)

from ml.utils.load_pretrained_cnn import (
    load_pretrained_cnn,
)


def main():

    print("=" * 60)
    print("TERRASPECTRA HYBRID REAL-DATA FORWARD TEST")
    print("=" * 60)

    torch.manual_seed(42)

    device = torch.device(
        "mps" if torch.backends.mps.is_available()
        else "cpu"
    )

    print(f"Device: {device}")

    data_dir = ROOT / "data/real/kaggle_2026"

    stats_path = data_dir / "band_normalization.npz"

    model = HyperspectralHybridCNNViT()

    checkpoint = load_pretrained_cnn(model)

    with np.load(stats_path) as stats:

        for key, checkpoint_key in (
            ("mean", "band_mean"),
            ("std", "band_std"),
        ):

            expected = checkpoint[checkpoint_key]

            if isinstance(expected, torch.Tensor):
                expected = expected.cpu().numpy()

            np.testing.assert_array_equal(
                stats[key],
                expected,
            )

    print("\nNormalization compatibility: PASSED")

    dataset = RealHyperspectralDataset(
        manifest_path=data_dir / "train_manifest.csv",
        normalization="per_band",
        stats_path=stats_path,
    )

    loader = DataLoader(
        dataset,
        batch_size=4,
        shuffle=False,
        num_workers=0,
    )

    images, labels = next(iter(loader))

    images = images.to(device)

    model = model.to(device)
    model.eval()

    print(f"\nInput image shape: {images.shape}")
    print(f"Actual labels: {labels.tolist()}")

    with torch.no_grad():

        cnn_features = model.cnn.extract_features(
            images
        )

        tokens = model.token_embedding(
            cnn_features
        )

        encoded_tokens = model.transformer(
            tokens
        )

        pooled_features = encoded_tokens.mean(dim=1)

        logits = model(images)

        probabilities = torch.softmax(
            logits, dim=1
        )

        predictions = probabilities.argmax(dim=1)

    print("\nINTERMEDIATE TENSOR SHAPES")

    print(f"CNN features: {cnn_features.shape}")
    print(f"Tokens: {tokens.shape}")
    print(f"Encoded tokens: {encoded_tokens.shape}")
    print(f"Pooled features: {pooled_features.shape}")
    print(f"Output logits: {logits.shape}")

    assert images.shape == (4, 1, 125, 32, 32)

    assert cnn_features.shape == (4, 64, 15, 4, 4)

    assert tokens.shape == (4, 240, 256)

    assert encoded_tokens.shape == (4, 240, 256)

    assert pooled_features.shape == (4, 256)

    assert logits.shape == (4, 3)

    for tensor in (
        images,
        cnn_features,
        tokens,
        encoded_tokens,
        pooled_features,
        logits,
        probabilities,
    ):
        assert torch.isfinite(tensor).all()

    torch.testing.assert_close(
        probabilities.sum(dim=1),
        torch.ones(4, device=device),
    )

    assert set(labels.tolist()) == {0, 1, 2}

    class_names = ["Healthy", "Rust", "Other"]

    print("\nSAMPLE PREDICTIONS")

    for index in range(len(labels)):

        actual = class_names[labels[index].item()]

        predicted = class_names[
            predictions[index].item()
        ]

        confidence = probabilities[
            index
        ].max().item()

        print(
            f"Sample {index + 1}: "
            f"Actual={actual}, "
            f"Predicted={predicted}, "
            f"Probability={confidence:.4f}"
        )

    print("\nReal-data input test: PASSED")
    print("CNN feature extraction test: PASSED")
    print("Token embedding test: PASSED")
    print("Transformer encoding test: PASSED")
    print("Classification output test: PASSED")
    print("Numerical stability test: PASSED")
    print("Probability normalization test: PASSED")
    print("All three classes represented: PASSED")

    print("\n" + "=" * 60)
    print("ALL REAL-DATA FORWARD TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    main()
