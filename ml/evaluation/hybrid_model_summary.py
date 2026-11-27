import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.hybrid_cnn_vit import HyperspectralHybridCNNViT


def main():

    model = HyperspectralHybridCNNViT()

    print("=" * 60)
    print("TERRASPECTRA HYBRID MODEL SUMMARY")
    print("=" * 60)

    components = {
        "CNN": model.cnn,
        "Token embedding": model.token_embedding,
        "Transformer": model.transformer,
        "Classifier": model.classifier,
    }

    for name, component in components.items():

        count = sum(
            p.numel() for p in component.parameters()
        )

        print(f"{name}: {count:,} parameters")

    total = sum(
        p.numel() for p in model.parameters()
    )

    trainable = sum(
        p.numel()
        for p in model.parameters()
        if p.requires_grad
    )

    print("-" * 60)
    print(f"Total parameters: {total:,}")
    print(f"Trainable parameters: {trainable:,}")
    print(f"Non-trainable parameters: {total - trainable:,}")
    print("=" * 60)

    print("MODEL SUMMARY COMPLETED!")


if __name__ == "__main__":
    main()
