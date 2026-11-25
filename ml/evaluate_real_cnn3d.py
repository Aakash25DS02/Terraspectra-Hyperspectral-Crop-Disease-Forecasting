from pathlib import Path
import argparse
import sys

import numpy as np
import torch
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from torch.utils.data import DataLoader

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cnn3d import HyperspectralCNN3D_Simplified
from dataset.real_data_loader import RealHyperspectralDataset


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = PROJECT_ROOT / "data/real/kaggle_2026"
CHECKPOINT_ROOT = PROJECT_ROOT / "checkpoints/real"
REPORT_ROOT = PROJECT_ROOT / "reports/real"

CLASS_NAMES = ["Healthy", "Rust", "Other"]


def evaluate_model(checkpoint_name):
    checkpoint_path = CHECKPOINT_ROOT / checkpoint_name

    if not checkpoint_path.exists():
        raise FileNotFoundError(
            f"Checkpoint not found: {checkpoint_path}"
        )

    device = torch.device(
        "mps" if torch.backends.mps.is_available() else "cpu"
    )

    # Only use weights_only=False for checkpoints you trust.
    checkpoint = torch.load(
        checkpoint_path,
        map_location="cpu",
        weights_only=False,
    )

    normalization = checkpoint.get(
        "normalization", "divide_by_65535"
    )

    if normalization == "per_band":
        loader_normalization = "per_band"
        stats_path = DATA_ROOT / "band_normalization.npz"

        if not stats_path.exists():
            raise FileNotFoundError(
                f"Normalization statistics missing: {stats_path}"
            )

        # Ensure the external statistics match the trained model.
        with np.load(stats_path, allow_pickle=False) as stats:
            for key, saved_key in [
                ("mean", "band_mean"),
                ("std", "band_std"),
            ]:
                expected = checkpoint[saved_key]

                if isinstance(expected, torch.Tensor):
                    expected = expected.cpu().numpy()

                if not np.array_equal(stats[key], expected):
                    raise ValueError(
                        f"Normalization mismatch: {key}"
                    )

    elif normalization == "divide_by_65535":
        loader_normalization = "fixed"
        stats_path = None

    else:
        raise ValueError(
            f"Unsupported normalization: {normalization}"
        )

    dataset = RealHyperspectralDataset(
        DATA_ROOT / "val_manifest.csv",
        normalization=loader_normalization,
        stats_path=stats_path,
    )

    loader = DataLoader(
        dataset,
        batch_size=4,
        shuffle=False,
        num_workers=0,
    )

    model = HyperspectralCNN3D_Simplified(
        num_classes=3,
        num_bands=125,
        patch_size=32,
    ).to(device)

    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    true_labels = []
    predicted_labels = []

    with torch.no_grad():
        for images, labels in loader:
            outputs = model(images.to(device))
            predictions = outputs.argmax(dim=1).cpu()

            true_labels.extend(labels.tolist())
            predicted_labels.extend(predictions.tolist())

    accuracy = accuracy_score(
        true_labels, predicted_labels
    )

    report = classification_report(
        true_labels,
        predicted_labels,
        labels=[0, 1, 2],
        target_names=CLASS_NAMES,
        digits=4,
        zero_division=0,
    )

    matrix = confusion_matrix(
        true_labels,
        predicted_labels,
        labels=[0, 1, 2],
    )

    print("\nTERRASPECTRA REAL 3D-CNN EVALUATION")
    print("----------------------------------")
    print("Checkpoint:", checkpoint_name)
    print("Device:", device)
    print("Normalization:", normalization)
    print("Best epoch:", checkpoint.get("epoch"))
    print("Validation images:", len(dataset))
    print("Accuracy:", f"{accuracy:.4f}")

    print("\nClassification report:")
    print(report)

    print("Confusion matrix:")
    print(matrix)

    REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    model_name = Path(checkpoint_name).stem

    report_path = REPORT_ROOT / f"{model_name}_report.txt"
    matrix_path = REPORT_ROOT / f"{model_name}_confusion.csv"

    report_text = (
        "TERRASPECTRA MODEL EVALUATION\n"
        f"Checkpoint: {checkpoint_name}\n"
        f"Normalization: {normalization}\n"
        f"Validation images: {len(dataset)}\n"
        f"Accuracy: {accuracy:.4f}\n\n"
        f"{report}\n"
        f"Confusion matrix:\n{matrix}\n"
    )

    report_path.write_text(report_text)

    np.savetxt(
        matrix_path,
        matrix,
        delimiter=",",
        fmt="%d",
        header="Predicted Healthy,Predicted Rust,Predicted Other",
        comments="",
    )

    print("\nEvaluation files saved:")
    print("Report:", report_path)
    print("Confusion matrix:", matrix_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluate TerraSpectra real wheat 3D-CNN"
    )

    parser.add_argument(
        "--checkpoint",
        default="cnn3d_wheat_standardized_best.pth",
        help="Checkpoint filename in checkpoints/real/",
    )

    args = parser.parse_args()

    evaluate_model(args.checkpoint)
