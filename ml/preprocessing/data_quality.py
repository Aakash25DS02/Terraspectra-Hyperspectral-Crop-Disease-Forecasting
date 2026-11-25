
import numpy as np


def check_data_quality(cube):
    """Check a hyperspectral cube for common data issues."""
    cube = np.asarray(cube)

    if cube.ndim != 3:
        raise ValueError(
            f"Expected a 3D cube (H, W, Bands), got {cube.shape}"
        )

    print("\n--- Hyperspectral Data Quality Report ---")
    print(f"Cube shape: {cube.shape}")
    print(f"Data type: {cube.dtype}")
    print(f"NaN values: {np.isnan(cube).sum()}")
    print(f"Infinite values: {np.isinf(cube).sum()}")

    valid = cube[np.isfinite(cube)]

    if valid.size:
        print(f"Minimum value: {valid.min():.4f}")
        print(f"Maximum value: {valid.max():.4f}")
        print(f"Mean value: {valid.mean():.4f}")
    else:
        print("Warning: No valid numerical values found!")


if __name__ == "__main__":
    sample_cube = np.random.default_rng(42).random(
        (32, 32, 20)
    ).astype(np.float32)

    check_data_quality(sample_cube)
