import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.transformer_encoder import (
    SpatialSpectralTransformerEncoder,
)


def main():

    print("=" * 60)
    print("TERRASPECTRA SELF-ATTENTION TEST")
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

    first_layer = model.encoder.layers[0]

    with torch.no_grad():

        normalized_tokens = first_layer.norm1(tokens)

        attention_output, attention_weights = (
            first_layer.self_attn(
                normalized_tokens,
                normalized_tokens,
                normalized_tokens,
                need_weights=True,
                average_attn_weights=False,
            )
        )

        original_output = model(tokens)

        modified_tokens = tokens.clone()
        modified_tokens[:, 0, :128] += 5.0

        modified_output = model(modified_tokens)

    print(f"\nInput shape: {tokens.shape}")

    print(
        f"Attention output shape: "
        f"{attention_output.shape}"
    )

    print(
        f"Attention weights shape: "
        f"{attention_weights.shape}"
    )

    assert attention_output.shape == (2, 240, 256)

    assert attention_weights.shape == (
        2, 4, 240, 240
    )

    assert torch.isfinite(attention_output).all()

    assert torch.isfinite(attention_weights).all()

    assert (attention_weights >= 0).all()

    row_sums = attention_weights.sum(dim=-1)

    torch.testing.assert_close(
        row_sums,
        torch.ones_like(row_sums),
        atol=1e-5,
        rtol=1e-5,
    )

    print("\nAttention output shape test: PASSED")
    print("Attention weight shape test: PASSED")
    print("Numerical stability test: PASSED")
    print("Attention normalization test: PASSED")

    context_difference = (
        original_output[:, 1:, :]
        - modified_output[:, 1:, :]
    ).abs().mean().item()

    print(
        f"\nMean contextual change: "
        f"{context_difference:.8f}"
    )

    assert context_difference > 1e-6

    print("Cross-token interaction test: PASSED")

    print("\nTesting backward propagation...")

    model.train()
    model.zero_grad(set_to_none=True)

    train_tokens = (
        tokens.detach().clone().requires_grad_(True)
    )

    output = model(train_tokens)

    target = torch.randn_like(output)

    loss = (output - target).square().mean()

    loss.backward()

    assert torch.isfinite(loss)

    assert train_tokens.grad is not None

    assert torch.isfinite(train_tokens.grad).all()

    assert train_tokens.grad.abs().sum().item() > 0

    for name, parameter in model.named_parameters():

        if parameter.requires_grad:

            assert parameter.grad is not None, (
                f"Missing gradient: {name}"
            )

            assert torch.isfinite(
                parameter.grad
            ).all(), f"Invalid gradient: {name}"

    for index, layer in enumerate(model.encoder.layers):

        attention_grad = (
            layer.self_attn.in_proj_weight.grad
        )

        assert attention_grad.abs().sum().item() > 0, (
            f"No attention gradient in layer {index}"
        )

    print(f"Test loss: {loss.item():.6f}")

    print("Input gradient test: PASSED")
    print("Parameter gradient test: PASSED")
    print("Attention gradient test: PASSED")
    print("Backward propagation test: PASSED")

    print("\n" + "=" * 60)
    print("ALL SELF-ATTENTION TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    main()
