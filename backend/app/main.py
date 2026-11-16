from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    return {
        "project": "TerraSpectra",
        "dataset_status": "awaiting_dataset",
        "model_status": "integration_pending",
        "total_samples": 0,
        "diseases_detected": 0,
        "message": "Backend is ready for dataset and model integration.",
    }