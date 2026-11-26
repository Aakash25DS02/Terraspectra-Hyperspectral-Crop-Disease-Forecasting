import torch
import torch.nn as nn

from ml.cnn3d import HyperspectralCNN3D_Simplified

from ml.token_embedding import (
    SpatialSpectralTokenEmbedding,
)

from ml.transformer_encoder import (
    SpatialSpectralTransformerEncoder,
)


class HyperspectralHybridCNNViT(nn.Module):
    """
    Hybrid 3D-CNN and Transformer architecture
    for hyperspectral crop disease classification.

    Input:  (B, 1, 125, 32, 32)
    Output: (B, 3)
    """

    def __init__(
        self,
        num_classes=3,
        num_bands=125,
        patch_size=32,
        embed_dim=256,
        num_heads=4,
        num_layers=2,
        feedforward_dim=512,
        transformer_dropout=0.1,
        classifier_dropout=0.3,
    ):
        super().__init__()

        if num_bands < 8 or patch_size < 8:
            raise ValueError(
                "Input dimensions must be at least 8."
            )

        self.num_classes = num_classes
        self.num_bands = num_bands
        self.patch_size = patch_size
        self.embed_dim = embed_dim

        self.num_tokens = (
            (num_bands // 8)
            * (patch_size // 8)
            * (patch_size // 8)
        )

        self.cnn = HyperspectralCNN3D_Simplified(
            num_classes=num_classes,
            num_bands=num_bands,
            patch_size=patch_size,
        )

        del self.cnn.fc1
        del self.cnn.fc2
        del self.cnn.dropout

        self.token_embedding = (
            SpatialSpectralTokenEmbedding(
                in_channels=64,
                embed_dim=embed_dim,
                max_tokens=self.num_tokens,
            )
        )

        self.transformer = (
            SpatialSpectralTransformerEncoder(
                embed_dim=embed_dim,
                num_heads=num_heads,
                num_layers=num_layers,
                feedforward_dim=feedforward_dim,
                dropout=transformer_dropout,
            )
        )

        self.classifier = nn.Sequential(
            nn.LayerNorm(embed_dim),
            nn.Linear(embed_dim, 128),
            nn.GELU(),
            nn.Dropout(classifier_dropout),
            nn.Linear(128, num_classes),
        )

    def forward_features(self, x):

        expected_shape = (
            1,
            self.num_bands,
            self.patch_size,
            self.patch_size,
        )

        if (
            x.ndim != 5
            or tuple(x.shape[1:]) != expected_shape
        ):
            raise ValueError(
                f"Expected input shape "
                f"(B, {expected_shape}), "
                f"received {tuple(x.shape)}."
            )

        cnn_features = self.cnn.extract_features(x)

        tokens = self.token_embedding(cnn_features)

        encoded_tokens = self.transformer(tokens)

        pooled_features = encoded_tokens.mean(dim=1)

        return pooled_features

    def forward(self, x):

        features = self.forward_features(x)

        logits = self.classifier(features)

        return logits


def test_hybrid_model():

    print("=" * 60)
    print("TERRASPECTRA HYBRID CNN-VIT MODEL TEST")
    print("=" * 60)

    torch.manual_seed(42)

    device = torch.device(
        "mps" if torch.backends.mps.is_available()
        else "cpu"
    )

    print(f"Device: {device}")

    model = HyperspectralHybridCNNViT().to(device)

    model.eval()

    images = torch.randn(
        2, 1, 125, 32, 32,
        device=device,
    )

    with torch.no_grad():

        features = model.cnn.extract_features(images)

        tokens = model.token_embedding(features)

        encoded = model.transformer(tokens)

        pooled = encoded.mean(dim=1)

        logits = model(images)

        probabilities = torch.softmax(logits, dim=1)

    print(f"\nInput shape: {images.shape}")
    print(f"CNN features: {features.shape}")
    print(f"Token sequence: {tokens.shape}")
    print(f"Encoded tokens: {encoded.shape}")
    print(f"Pooled features: {pooled.shape}")
    print(f"Output logits: {logits.shape}")

    assert features.shape == (2, 64, 15, 4, 4)
    assert tokens.shape == (2, 240, 256)
    assert encoded.shape == (2, 240, 256)
    assert pooled.shape == (2, 256)
    assert logits.shape == (2, 3)

    for tensor in (
        features,
        tokens,
        encoded,
        pooled,
        logits,
        probabilities,
    ):
        assert torch.isfinite(tensor).all()

    torch.testing.assert_close(
        probabilities.sum(dim=1),
        torch.ones(2, device=device),
    )

    print("\nPredicted probabilities:")
    print(probabilities.cpu())

    print("\nArchitecture shape test: PASSED")
    print("Numerical stability test: PASSED")
    print("Probability normalization test: PASSED")

    print("\nHYBRID CNN-VIT MODEL TEST PASSED!")


if __name__ == "__main__":
    test_hybrid_model()
