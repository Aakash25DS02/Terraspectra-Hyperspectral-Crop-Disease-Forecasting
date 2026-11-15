import rasterio
import numpy as np
import os

class RasterHyperspectralLoader:
    """
    Utility for loading geospatial raster images (GeoTIFF) using Rasterio.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Raster file not found: {filepath}")

    def inspect_metadata(self):
        """Inspect geospatial reference system, dimensions, transform, and band count."""
        with rasterio.open(self.filepath) as src:
            print(f"\n--- Raster Metadata: {self.filepath} ---")
            print(f"Driver: {src.driver}")
            print(f"Width x Height: {src.width} x {src.height}")
            print(f"Bands: {src.count}")
            print(f"CRS: {src.crs}")
            print(f"NoData Value: {src.nodatavals}")
            print(f"Data Type: {src.dtypes[0]}")
            print(f"Transform (Affine):\n{src.transform}")

    def load_as_numpy(self):
        """Reads bands into a NumPy array with shape (Height, Width, Bands)."""
        with rasterio.open(self.filepath) as src:
            # Rasterio reads as (Bands, Height, Width)
            data = src.read()
            # Permute to (Height, Width, Bands)
            data_hwc = np.transpose(data, (1, 2, 0))
            return data_hwc, src.meta

if __name__ == "__main__":
    print("RasterLoader class ready for GeoTIFF processing.")