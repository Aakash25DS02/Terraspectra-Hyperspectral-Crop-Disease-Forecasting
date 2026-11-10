# TerraSpectra: Hyperspectral Crop Disease Forecasting

##  About the Project

TerraSpectra is an AI-based precision agriculture project for **early crop disease and crop stress detection using hyperspectral satellite images**.

Unlike normal RGB images, hyperspectral images contain hundreds of spectral bands. TerraSpectra uses these spectral features to identify changes in crops before visible disease symptoms appear.

The project combines **3D-CNN, Vision Transformer, FastAPI, React, and Deck.gl**.

##  Problem Statement

Traditional crop monitoring mainly uses RGB or simple infrared images. These methods may detect diseases only after visible symptoms appear.

TerraSpectra aims to detect early crop stress and disease by analyzing the spectral information available in hyperspectral images.

##  Proposed Solution

```text
Hyperspectral Data
       ↓
Data Preprocessing
       ↓
PCA
       ↓
3D-CNN
       ↓
Vision Transformer
       ↓
Disease Prediction
       ↓
FastAPI
       ↓
GIS Dashboard
```

##  Main Modules

### 1. Hyperspectral Data Processing

- Rasterio
- GDAL
- HDF5
- Data normalization
- PCA
- Spectral analysis

### 2. 3D-CNN + Vision Transformer

The deep learning model analyzes the spatial and spectral information of hyperspectral images.

```text
Hyperspectral Image
        ↓
      3D-CNN
        ↓
   Feature Extraction
        ↓
 Vision Transformer
        ↓
 Disease Prediction
```

### 3. FastAPI Backend

FastAPI will be used to:

- Process uploaded data
- Run model predictions
- Handle large raster tiles
- Send prediction results to the frontend

### 4. GIS Dashboard

The React dashboard will use Deck.gl and Mapbox to display:

- Farm boundaries
- Disease-risk heatmaps
- Crop health information
- Risk statistics
- Historical crop health

##  Technologies

| Category | Technologies |
|---|---|
| Programming | Python, JavaScript |
| Data Processing | NumPy, Pandas, Scikit-learn |
| Geospatial | Rasterio, GDAL |
| Deep Learning | PyTorch |
| Model | 3D-CNN, Vision Transformer |
| Backend | FastAPI |
| Frontend | React |
| GIS | Deck.gl, Mapbox |
| Version Control | Git, GitHub |

## 📊 Expected Output

TerraSpectra will provide an interactive platform that can:

- Process hyperspectral satellite data
- Analyze crop spectral information
- Predict crop disease/stress
- Display affected areas on a GIS map
- Show crop-risk statistics
- View historical crop health
