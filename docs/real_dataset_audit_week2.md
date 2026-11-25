# TerraSpectra - Week 2 Real Dataset Audit

## Dataset
Beyond Visible Spectrum: AI for Agriculture 2026
Source: Kaggle
Crop: Wheat
Format: Hyperspectral GeoTIFF

## Dataset Structure
Training images: 600
Validation images: 300
Image dimensions: 32 x 32 pixels
Typical spectral bands: 125
Data type: uint16

## Training Labels
Healthy: 200
Rust: 200
Other: 200

## Quality Audit

Training:
- Usable images: 575
- All-zero images: 20
- Unexpected extra-band images: 5
- Images with removable 65535 extra band: 106

Validation:
- Usable images: 289
- All-zero images: 11
- Unexpected extra-band images: 0
- Images with removable 65535 extra band: 48

Total provisionally usable images: 864

## Important Findings
- Some images contain 126 bands instead of 125.
- Certain 126th bands contain only 65535 and appear to be placeholders.
- Five training files have unexpected extra-band values and are excluded pending investigation.
- Validation images have no class labels identifiable from filenames.
- No geographic coordinate reference system was found in inspected images.
- Original dataset files remain unchanged.

## Next Steps
1. Check for official validation labels.
2. Create a cleaned dataset manifest.
3. Create a stratified train/validation split from labeled training images.
4. Adapt the PyTorch 3D-CNN data loader.
5. Train and evaluate the model on real hyperspectral data.
