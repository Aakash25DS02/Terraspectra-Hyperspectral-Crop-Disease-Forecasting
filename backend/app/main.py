
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes.api import router


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

app.include_router(router)
