
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Directory where trained model checkpoints will be stored
MODEL_DIRECTORY = PROJECT_ROOT / "ml" / "models"

# Expected model checkpoint paths
MODEL_PATHS = {
    "3d_cnn": MODEL_DIRECTORY / "cnn3d_best.pth",
    "vision_transformer": MODEL_DIRECTORY / "vit_best.pth",
}


def get_model_status():
    """
    Check whether trained model checkpoint files are available.

    This function does not load models or generate predictions.
    """

    models = {}

    for model_name, model_path in MODEL_PATHS.items():
        is_available = model_path.is_file()

        models[model_name] = {
            "filename": model_path.name,
            "available": is_available,
            "status": (
                "checkpoint_available"
                if is_available
                else "awaiting_model_files"
            ),
        }

    all_available = all(
        model["available"] for model in models.values()
    )

    return {
        "status": (
            "checkpoints_available"
            if all_available
            else "pending"
        ),
        "model_directory": str(MODEL_DIRECTORY),
        "models": models,
        "message": (
            "All model checkpoint files are available."
            if all_available
            else "One or more trained model checkpoints are missing."
        ),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(get_model_status(), indent=4))
