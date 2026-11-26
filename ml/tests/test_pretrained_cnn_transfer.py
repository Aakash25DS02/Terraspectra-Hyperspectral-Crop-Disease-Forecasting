import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.cnn3d import HyperspectralCNN3D_Simplified

from ml.hybrid_cnn_vit import (
    HyperspectralHybridCNNViT,
)

from ml.utils.load_pretrained_cnn import (
    load_pretrained_cnn,
)


def main():

    print("=" * 60)
    print("TERRASPECTRA PRETRAINED CNN TRANSFER TEST")
    print("=" * 60)

    torch.manual_seed(42)

    device = torch.device(
        "mps" if torch.backends.mps.is_available()
        else "cpu"
    )

    print(f"Device: {device}\n")

    hybrid = HyperspectralHybridCNNViT()

    original_weights = (
        hybrid.cnn.conv1.weight.detach().clone()
    )

    checkpoint = load_pretrained_cnn(hybrid)

    assert not torch.equal(
        original_weights,
        hybrid.cnn.conv1.weight.detach(),
    ), "CNN weights did not change."

    print("Weight transfer test: PASSED")

    original_cnn = HyperspectralCNN3D_Simplified(
        num_classes=3,
        num_bands=125,
        patch_size=32,
    )

    original_cnn.load_state_dict(
        checkpoint["model_state_dict"],
        strict=True,
    )

    original_cnn = original_cnn.to(device)
    hybrid = hybrid.to(device)

    original_cnn.eval()
    hybrid.eval()

    images = torch.randn(
        2, 1, 125, 32, 32,
        device=device,
    )

    with torch.no_grad():

        original_features = (
            original_cnn.extract_features(images)
        )

        hybrid_features = (
            hybrid.cnn.extract_features(images)
        )

    torch.testing.assert_close(
        original_features,
        hybrid_features,
    )

    print(
        f"\nOriginal CNN features: "
        f"{original_features.shape}"
    )

    print(
        f"Hybrid CNN features: "
        f"{hybrid_features.shape}"
    )

    difference = (
        original_features - hybrid_features
    ).abs().max().item()

    print(
        f"Maximum feature difference: "
        f"{difference:.10f}"
    )

    print("Feature equivalence test: PASSED")

    print("\n" + "=" * 60)
    print("ALL PRETRAINED TRANSFER TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    main()
