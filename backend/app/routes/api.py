
from fastapi import APIRouter, HTTPException

from ml.preprocessing.dataset_loader import get_dataset_info

from backend.app.services.model_service import get_model_status
from backend.app.services.dataset_validation_service import validate_dataset


router = APIRouter()


def get_dataset_info_safely():
    """Retrieve dataset information with controlled error handling."""

    try:
        return get_dataset_info()

    except (OSError, KeyError, ValueError) as exc:
        raise HTTPException(
            status_code=503,
            detail="Dataset is unavailable or could not be read.",
        ) from exc


@router.get("/")
def home():
    return {
        "message": "Welcome to TerraSpectra API",
        "project": "Hyperspectral Crop Disease Forecasting",
        "status": "running",
    }


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "TerraSpectra Backend",
    }


@router.get("/api/v1/dashboard/summary")
def dashboard_summary():
    dataset = get_dataset_info_safely()

    return {
        "project": "TerraSpectra",
        "dataset_status": "available",
        "model_status": "integration_pending",
        "total_samples": dataset["total_samples"],
        "spectral_bands": dataset["spectral_bands"],
        "number_of_classes": len(dataset["classes"]),
        "diseases_detected": 0,
        "message": (
            "Dataset loaded successfully. "
            "ML model integration is pending."
        ),
    }


@router.get("/api/v1/dataset/info")
def dataset_information():
    return {
        "status": "success",
        "dataset": get_dataset_info_safely(),
    }


@router.get("/api/v1/dataset/validate")
def dataset_validation():
    return validate_dataset()


@router.get("/api/v1/model/status")
def model_status():
    model_information = get_model_status()

    return {
        **model_information,
        "framework": "PyTorch",
        "framework_version": "2.15.0",
        "device": "cpu",
        "input_specification": "awaiting_final_confirmation",
        "message": (
            "Model checkpoint availability checked successfully. "
            "Trained model loading and inference are not yet configured."
        ),
    }


@router.get("/api/v1/system/readiness")
def system_readiness():
    dataset = validate_dataset()
    models = get_model_status()

    return {
        "api_ready": True,
        "dataset_ready": dataset.get("valid", False),
        "model_checkpoints_available": (
            models.get("status") == "checkpoints_available"
        ),
        "ml_inference_configured": False,
        "message": (
            "Backend is running. ML inference integration is pending."
        ),
    }
