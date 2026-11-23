
import h5py
import numpy as np

from ml.preprocessing.dataset_loader import (
    DATASET_PATH,
    CLASS_NAMES_PATH,
    load_class_names,
)


def validate_dataset():
    """
    Validate the structure and metadata of the hyperspectral dataset.
    Does not modify the original dataset.
    """

    checks = {}
    errors = []
    details = {}

    # Check dataset file
    checks["dataset_file_exists"] = DATASET_PATH.is_file()

    if not checks["dataset_file_exists"]:
        errors.append("Hyperspectral dataset file is missing.")

    # Check class names file
    checks["class_names_file_exists"] = CLASS_NAMES_PATH.is_file()

    if not checks["class_names_file_exists"]:
        errors.append("Class names file is missing.")

    if errors:
        return {
            "status": "invalid",
            "valid": False,
            "checks": checks,
            "details": details,
            "errors": errors,
        }

    # Load class names
    try:
        class_names = load_class_names()
    except Exception as exc:
        errors.append(f"Unable to load class names: {exc}")

        return {
            "status": "invalid",
            "valid": False,
            "checks": checks,
            "details": details,
            "errors": errors,
        }

    # Inspect HDF5 structure
    try:
        with h5py.File(DATASET_PATH, "r") as file:

            required_datasets = [
                "images",
                "labels",
                "wavelengths",
            ]

            missing_datasets = [
                name for name in required_datasets
                if name not in file
            ]

            checks["required_datasets_present"] = (
                len(missing_datasets) == 0
            )

            if missing_datasets:
                errors.append(
                    "Missing HDF5 datasets: "
                    + ", ".join(missing_datasets)
                )

                return {
                    "status": "invalid",
                    "valid": False,
                    "checks": checks,
                    "details": details,
                    "errors": errors,
                }

            images = file["images"]
            labels = file["labels"]
            wavelengths = file["wavelengths"]

            image_shape = images.shape
            label_shape = labels.shape
            wavelength_shape = wavelengths.shape

            details = {
                "image_shape": list(image_shape),
                "label_shape": list(label_shape),
                "wavelength_shape": list(wavelength_shape),
                "image_dtype": str(images.dtype),
                "label_dtype": str(labels.dtype),
                "wavelength_dtype": str(wavelengths.dtype),
            }

            # Check image dimensions
            checks["image_dimensions_valid"] = (
                len(image_shape) == 4
                and all(dimension > 0 for dimension in image_shape)
            )

            if not checks["image_dimensions_valid"]:
                errors.append(
                    "Images must have four positive dimensions."
                )

            # Check label dimensions
            checks["label_dimensions_valid"] = (
                len(label_shape) == 1
                and label_shape[0] == image_shape[0]
            )

            if not checks["label_dimensions_valid"]:
                errors.append(
                    "Label count must match the number of images."
                )

            # Check wavelength dimensions
            checks["wavelength_dimensions_valid"] = (
                len(wavelength_shape) == 1
                and len(image_shape) == 4
                and wavelength_shape[0] == image_shape[3]
            )

            if not checks["wavelength_dimensions_valid"]:
                errors.append(
                    "Wavelength count must match spectral bands."
                )

            # Check integer labels and class mapping
            labels_are_integer = np.issubdtype(
                labels.dtype, np.integer
            )

            checks["labels_are_integer"] = bool(labels_are_integer)

            if not labels_are_integer:
                errors.append("Labels must contain integer values.")
            elif len(label_shape) == 1:
                unique_labels = sorted(
                    set(labels[:].tolist())
                )

                unknown_labels = [
                    int(label)
                    for label in unique_labels
                    if int(label) not in class_names
                ]

                checks["all_labels_have_class_names"] = (
                    len(unknown_labels) == 0
                )

                details["class_names"] = class_names
                details["unique_labels"] = [
                    int(label) for label in unique_labels
                ]

                if unknown_labels:
                    errors.append(
                        "Class names missing for labels: "
                        + ", ".join(map(str, unknown_labels))
                    )
            else:
                checks["all_labels_have_class_names"] = False

    except Exception as exc:
        errors.append(f"Unable to inspect HDF5 dataset: {exc}")

    is_valid = (
        len(errors) == 0
        and all(checks.values())
    )

    return {
        "status": "valid" if is_valid else "invalid",
        "valid": is_valid,
        "checks": checks,
        "details": details,
        "errors": errors,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(validate_dataset(), indent=4))
