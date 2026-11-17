import h5py
import numpy as np
import os

class HDF5HyperspectralLoader:
    """
    Utility for loading and inspecting hyperspectral datasets stored in HDF5 format.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
            
    def inspect(self):
        """Inspect datasets, metadata keys, shapes, and data types."""
        print(f"\n--- Inspecting HDF5 File: {self.filepath} ---")
        with h5py.File(self.filepath, 'r') as f:
            print("Keys available:", list(f.keys()))
            for key in f.keys():
                ds = f[key]
                print(f"  - Key '{key}': shape={ds.shape}, dtype={ds.dtype}")
                
    def load_cube_and_metadata(self, image_key='images', label_key='labels', wavelength_key='wavelengths'):
        """Load arrays from the HDF5 file."""
        with h5py.File(self.filepath, 'r') as f:
            images = f[image_key][:]
            labels = f[label_key][:] if label_key in f else None
            wavelengths = f[wavelength_key][:] if wavelength_key in f else None
            
        print(f"\nLoaded Cube Shape: {images.shape}")
        if wavelengths is not None:
            print(f"Spectral Bands Count: {len(wavelengths)} ({wavelengths[0]:.1f}nm to {wavelengths[-1]:.1f}nm)")
            
        return images, labels, wavelengths

if __name__ == "__main__":
    # Test on synthetic data
    sample_file = "./data/synthetic/synthetic_data.h5"
    if os.path.exists(sample_file):
        loader = HDF5HyperspectralLoader(sample_file)
        loader.inspect()
        images, labels, wavelengths = loader.load_cube_and_metadata()
    else:
        print("Sample synthetic file not found. Generate data first.")