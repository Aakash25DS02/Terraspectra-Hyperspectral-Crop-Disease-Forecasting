import torch
import torch.nn as nn


class SpatialSpectralTransformerEncoder(nn.Module):
    """
    Transformer encoder for hyperspectral
    spatial-spectral token sequences.

    Input:  (B, N, E)
    Output: (B, N, E)

    B = batch size
    N = number of tokens
    E = embedding dimension
    """

    def __init__(
        self,
        embed_dim=256,
        num_heads=4,
        num_layers=2,
        feedforward_dim=512,
        dropout=0.1,
    ):
        super().__init__()

        if embed_dim <= 0 or num_heads <= 0:
            raise ValueError(
                "Embedding dimension and heads must be positive."
            )

        if embed_dim % num_heads != 0:
            raise ValueError(
                "Embedding dimension must be divisible "
                "by the number of attention heads."
            )

        if num_layers <= 0 or feedforward_dim <= 0:
            raise ValueError(
                "Layer count and feedforward dimension "
                "must be positive."
            )

        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.num_layers = num_layers

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim,
            nhead=num_heads,
            dim_feedforward=feedforward_dim,
            dropout=dropout,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )

        self.encoder = nn.TransformerEncoder(
            encoder_layer=encoder_layer,
            num_layers=num_layers,
            norm=nn.LayerNorm(embed_dim),
            enable_nested_tensor=False,
        )

        self._initialize_weights()

    def _initialize_weights(self):
        for parameter in self.encoder.parameters():
            if parameter.dim() > 1:
                nn.init.xavier_uniform_(parameter)

    def forward(self, tokens):

        if tokens.ndim != 3:
            raise ValueError(
                "Expected input shape (B, N, E)."
            )

        if tokens.shape[-1] != self.embed_dim:
            raise ValueError(
                f"Expected embedding dimension "
                f"{self.embed_dim}, "
                f"received {tokens.shape[-1]}."
            )

        if tokens.shape[1] == 0:
            raise ValueError(
                "Token sequence cannot be empty."
            )

        encoded_tokens = self.encoder(tokens)

        return encoded_tokens


def test_transformer_encoder():

    print("=" * 60)
    print("TERRASPECTRA TRANSFORMER ENCODER TEST")
    print("=" * 60)

    torch.manual_seed(42)

    device = torch.device(
        "mps" if torch.backends.mps.is_available()
        else "cpu"
    )

    print(f"Device: {device}")

    model = SpatialSpectralTransformerEncoder(
        embed_dim=256,
        num_heads=4,
        num_layers=2,
        feedforward_dim=512,
        dropout=0.1,
    ).to(device)

    model.eval()

    tokens = torch.randn(
        2, 240, 256, device=device
    )

    with torch.no_grad():
        output = model(tokens)

    print(f"\nInput token shape: {tokens.shape}")
    print(f"Output token shape: {output.shape}")

    assert output.shape == (2, 240, 256), (
        "Transformer output shape mismatch."
    )

    assert torch.isfinite(output).all(), (
        "Non-finite values detected."
    )

    total_parameters = sum(
        p.numel() for p in model.parameters()
    )

    trainable_parameters = sum(
        p.numel()
        for p in model.parameters()
        if p.requires_grad
    )

    print(f"\nEmbedding dimension: {model.embed_dim}")
    print(f"Attention heads: {model.num_heads}")
    print(f"Transformer layers: {model.num_layers}")

    print(f"Total parameters: {total_parameters:,}")
    print(f"Trainable parameters: {trainable_parameters:,}")

    print("\nOutput shape test: PASSED")
    print("Numerical stability test: PASSED")

    print("\nTRANSFORMER ENCODER TEST PASSED!")


if __name__ == "__main__":
    test_transformer_encoder()
