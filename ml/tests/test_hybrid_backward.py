import sys
from pathlib import Path

import torch
import torch.nn as nn
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
    print("TERRASPECTRA HYBRID BACKWARD TEST")
    print("=" * 60)

    torch.manual_seed(42)

    device = torch.device(
        "mps" if torch.backends.mps.is_available()
        else "cpu"
    )

    print(f"Device: {device}")

    data_dir = ROOT / "data/real/kaggle_2026"

    dataset = RealHyperspectralDataset(
        manifest_path=data_dir / "train_manifest.csv",
        normalization="per_band",
        stats_path=data_dir / "band_normalization.npz",
    )

    loader = DataLoader(
        dataset,
        batch_size=4,
        shuffle=False,
        num_workers=0,
    )

    images, labels = next(iter(loader))

    images = images.to(device)
    labels = labels.to(device).long()

    model = HyperspectralHybridCNNViT()

    load_pretrained_cnn(model)

    model = model.to(device)
    model.train()

    criterion = nn.CrossEntropyLoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=0.0001,
    )

    components = {
        "CNN": model.cnn,
        "Token embedding": model.token_embedding,
        "Transformer": model.transformer,
        "Classifier": model.classifier,
    }

    original_parameters = {
        name: parameter.detach().clone()
        for name, parameter in model.named_parameters()
        if parameter.requires_grad
    }

    optimizer.zero_grad(set_to_none=True)

    logits = model(images)

    loss = criterion(logits, labels)

    assert torch.isfinite(logits).all()
    assert torch.isfinite(loss)

    print(f"\nInput shape: {images.shape}")
    print(f"Output shape: {logits.shape}")
    print(f"Actual labels: {labels.tolist()}")

    print(f"\nInitial loss: {loss.item():.6f}")

    print("\nRunning backward propagation...")

    loss.backward()

    print("\nGRADIENT VERIFICATION")

    for component_name, component in components.items():

        squared_norm = 0.0
        parameter_count = 0

        for name, parameter in component.named_parameters():

            if not parameter.requires_grad:
                continue

            assert parameter.grad is not None, (
                f"Missing gradient: "
                f"{component_name}.{name}"
            )

            assert torch.isfinite(parameter.grad).all(), (
                f"Invalid gradient: "
                f"{component_name}.{name}"
            )

            squared_norm += (
                parameter.grad.detach()
                .float()
                .square()
                .sum()
                .item()
            )

            parameter_count += 1

        gradient_norm = squared_norm ** 0.5

        assert parameter_count > 0

        assert gradient_norm > 0, (
            f"No gradient flow in {component_name}"
        )

        print(
            f"{component_name}: "
            f"gradient norm={gradient_norm:.6f} "
            f"- PASSED"
        )

    print("\nRunning optimizer step...")

    optimizer.step()

    print("\nPARAMETER UPDATE VERIFICATION")

    for component_name, component in components.items():

        updated_count = 0

        for name, parameter in model.named_parameters():

            if not parameter.requires_grad:
                continue

            if not any(
                parameter is p
                for p in component.parameters()
            ):
                continue

            assert torch.isfinite(parameter).all()

            if not torch.equal(
                parameter.detach(),
                original_parameters[name],
            ):
                updated_count += 1

        assert updated_count > 0, (
            f"No parameters updated in {component_name}"
        )

        print(
            f"{component_name}: "
            f"{updated_count} parameter tensors updated "
            f"- PASSED"
        )

    model.eval()

    with torch.no_grad():

        updated_logits = model(images)

        updated_loss = criterion(
            updated_logits, labels
        )

    assert torch.isfinite(updated_logits).all()
    assert torch.isfinite(updated_loss)

    print(
        f"\nPost-update evaluation loss: "
        f"{updated_loss.item():.6f}"
    )

    print("\nCrossEntropyLoss test: PASSED")
    print("End-to-end gradient flow test: PASSED")
    print("Optimizer update test: PASSED")
    print("Post-update numerical stability: PASSED")

    print("\n" + "=" * 60)
    print("ALL HYBRID BACKWARD TESTS PASSED!")
    print("=" * 60)

    print("No checkpoint was saved or modified.")


if __name__ == "__main__":
    main()
