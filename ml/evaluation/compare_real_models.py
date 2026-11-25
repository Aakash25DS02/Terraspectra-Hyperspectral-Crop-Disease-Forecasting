import csv
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = PROJECT_ROOT / "reports/real"

MODELS = {
    "Original CNN": "cnn3d_wheat_20epochs_best_report.txt",
    "Standardized CNN": "cnn3d_wheat_standardized_best_report.txt",
}


def read_metrics(report_path):
    if not report_path.exists():
        raise FileNotFoundError(
            f"Missing evaluation report: {report_path}\n"
            "Run ml/evaluate_real_cnn3d.py for this checkpoint first."
        )

    text = report_path.read_text()

    accuracy_match = re.search(
        r"^Accuracy:\s*([0-9.]+)",
        text,
        re.MULTILINE,
    )

    if not accuracy_match:
        raise ValueError(f"Accuracy missing: {report_path}")

    metrics = {
        "accuracy": float(accuracy_match.group(1))
    }

    for class_name in ("Healthy", "Rust", "Other"):
        match = re.search(
            rf"^\s*{class_name}\s+"
            r"([0-9.]+)\s+([0-9.]+)\s+"
            r"([0-9.]+)\s+(\d+)",
            text,
            re.MULTILINE,
        )

        if not match:
            raise ValueError(
                f"{class_name} metrics missing: {report_path}"
            )

        metrics[f"{class_name.lower()}_recall"] = float(
            match.group(2)
        )

    macro_match = re.search(
        r"^\s*macro avg\s+"
        r"([0-9.]+)\s+([0-9.]+)\s+"
        r"([0-9.]+)\s+(\d+)",
        text,
        re.MULTILINE,
    )

    if not macro_match:
        raise ValueError(
            f"Macro F1 missing: {report_path}"
        )

    metrics["macro_f1"] = float(macro_match.group(3))

    return metrics


def main():
    results = []

    for name, filename in MODELS.items():
        metrics = read_metrics(REPORT_DIR / filename)
        metrics["model"] = name
        results.append(metrics)

    print("\nTERRASPECTRA MODEL COMPARISON")
    print("-----------------------------")

    for result in results:
        print(f"\n{result['model']}")
        print(f"Accuracy: {result['accuracy']:.2%}")
        print(
            f"Healthy recall: "
            f"{result['healthy_recall']:.2%}"
        )
        print(f"Rust recall: {result['rust_recall']:.2%}")
        print(f"Other recall: {result['other_recall']:.2%}")
        print(f"Macro F1: {result['macro_f1']:.4f}")

    output = REPORT_DIR / "model_comparison.csv"

    fields = [
        "model",
        "accuracy",
        "healthy_recall",
        "rust_recall",
        "other_recall",
        "macro_f1",
    ]

    with output.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    print("\nComparison saved:", output)


if __name__ == "__main__":
    main()
