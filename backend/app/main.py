
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ml.preprocessing.dataset_loader import get_dataset_info
from backend.app.services.model_service import get_model_status


app = FastAPI(
    title="TerraSpectra API",
    description="Hyperspectral Crop Disease Forecasting Backend",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Welcome to TerraSpectra API",
        "project": "Hyperspectral Crop Disease Forecasting",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "TerraSpectra Backend",
    }


@app.get("/api/v1/dashboard/summary")
def dashboard_summary():
    dataset = get_dataset_info()

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


@app.get("/api/v1/dataset/info")
def dataset_information():
    return {
        "status": "success",
        "dataset": get_dataset_info(),
    }


@app.get("/api/v1/model/status")
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
