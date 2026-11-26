
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.model_service import get_model_status
from backend.app.services.dataset_validation_service import validate_dataset


client = TestClient(app)


class TestTerraSpectraAPI(unittest.TestCase):

    def test_health_endpoint(self):
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_dashboard_summary(self):
        response = client.get("/api/v1/dashboard/summary")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total_samples"], 500)

    def test_dashboard_summary_when_dataset_missing(self):
        with patch(
            "backend.app.routes.api.get_dataset_info",
            side_effect=FileNotFoundError("Dataset missing"),
        ):
            response = client.get("/api/v1/dashboard/summary")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json()["detail"],
            "Dataset is unavailable or could not be read.",
        )

    def test_dataset_information(self):
        response = client.get("/api/v1/dataset/info")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

    def test_dataset_information_when_dataset_missing(self):
        with patch(
            "backend.app.routes.api.get_dataset_info",
            side_effect=FileNotFoundError("Dataset missing"),
        ):
            response = client.get("/api/v1/dataset/info")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json()["detail"],
            "Dataset is unavailable or could not be read.",
        )

    def test_dataset_validation(self):
        response = client.get("/api/v1/dataset/validate")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["valid"])

    def test_dataset_validation_endpoint_structure(self):
        response = client.get("/api/v1/dataset/validate")
        data = response.json()

        self.assertIn("checks", data)
        self.assertIn("details", data)
        self.assertIn("errors", data)

    def test_dataset_statistics(self):
        response = client.get("/api/v1/dataset/statistics")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["status"], "success")
        self.assertEqual(data["total_samples"], 500)
        self.assertEqual(data["image_dimensions"]["height"], 64)
        self.assertEqual(data["image_dimensions"]["width"], 64)
        self.assertEqual(data["spectral_bands"], 100)
        self.assertEqual(data["number_of_classes"], 5)

        self.assertIn("class_statistics", data)

        total_class_samples = sum(
            item["samples"]
            for item in data["class_statistics"].values()
        )

        self.assertEqual(total_class_samples, 500)

    def test_model_status(self):
        response = client.get("/api/v1/model/status")
        self.assertEqual(response.status_code, 200)
        self.assertIn("models", response.json())

    def test_home_endpoint(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "running")

    def test_system_readiness(self):
        response = client.get("/api/v1/system/readiness")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertTrue(data["api_ready"])
        self.assertTrue(data["dataset_ready"])
        self.assertFalse(data["ml_inference_configured"])
        self.assertIn("model_checkpoints_available", data)


class TestModelService(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.model_directory = Path(self.temp_dir.name)

        self.model_paths = {
            "3d_cnn": self.model_directory / "cnn3d_best.pth",
            "vision_transformer": self.model_directory / "vit_best.pth",
        }

        self.patcher = patch(
            "backend.app.services.model_service.MODEL_PATHS",
            self.model_paths,
        )
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.temp_dir.cleanup()

    def test_both_models_missing(self):
        result = get_model_status()
        self.assertEqual(result["status"], "pending")

    def test_only_cnn_model_available(self):
        self.model_paths["3d_cnn"].touch()

        result = get_model_status()

        self.assertEqual(result["status"], "pending")
        self.assertTrue(result["models"]["3d_cnn"]["available"])
        self.assertFalse(
            result["models"]["vision_transformer"]["available"]
        )

    def test_both_models_available(self):
        self.model_paths["3d_cnn"].touch()
        self.model_paths["vision_transformer"].touch()

        result = get_model_status()

        self.assertEqual(result["status"], "checkpoints_available")


class TestDatasetValidationService(unittest.TestCase):

    def test_dataset_validation(self):
        result = validate_dataset()
        self.assertTrue(result["valid"])
        self.assertEqual(result["status"], "valid")

    def test_dataset_dimensions(self):
        result = validate_dataset()
        details = result["details"]

        self.assertEqual(details["image_shape"], [500, 64, 64, 100])
        self.assertEqual(details["label_shape"], [500])
        self.assertEqual(details["wavelength_shape"], [100])


if __name__ == "__main__":
    unittest.main()
