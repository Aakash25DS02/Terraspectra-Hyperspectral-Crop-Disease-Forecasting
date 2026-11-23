
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

        data = response.json()

        self.assertEqual(data["dataset_status"], "available")
        self.assertEqual(data["model_status"], "integration_pending")
        self.assertEqual(data["total_samples"], 500)
        self.assertEqual(data["spectral_bands"], 100)
        self.assertEqual(data["number_of_classes"], 5)

    def test_dataset_information(self):
        response = client.get("/api/v1/dataset/info")

        self.assertEqual(response.status_code, 200)

        data = response.json()["dataset"]

        self.assertEqual(data["total_samples"], 500)
        self.assertEqual(data["spectral_bands"], 100)

    def test_dataset_validation(self):
        response = client.get("/api/v1/dataset/validate")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["status"], "valid")
        self.assertTrue(data["valid"])
        self.assertEqual(data["errors"], [])

        self.assertTrue(
            all(data["checks"].values())
        )

    def test_dataset_validation_endpoint_structure(self):
        response = client.get("/api/v1/dataset/validate")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIn("status", data)
        self.assertIn("valid", data)
        self.assertIn("checks", data)
        self.assertIn("details", data)
        self.assertIn("errors", data)

        self.assertEqual(
            data["details"]["image_shape"],
            [500, 64, 64, 100]
        )

    def test_model_status(self):
        response = client.get("/api/v1/model/status")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["framework"], "PyTorch")
        self.assertEqual(data["framework_version"], "2.15.0")
        self.assertEqual(data["device"], "cpu")

        self.assertIn("3d_cnn", data["models"])
        self.assertIn("vision_transformer", data["models"])

    def test_home_endpoint(self):
        response = client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "running")


class TestModelService(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.model_directory = Path(self.temp_directory.name)

        self.cnn_path = self.model_directory / "cnn3d_best.pth"
        self.vit_path = self.model_directory / "vit_best.pth"

        self.model_paths = {
            "3d_cnn": self.cnn_path,
            "vision_transformer": self.vit_path,
        }

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_both_models_missing(self):
        with patch(
            "backend.app.services.model_service.MODEL_PATHS",
            self.model_paths,
        ):
            result = get_model_status()

        self.assertEqual(result["status"], "pending")
        self.assertFalse(result["models"]["3d_cnn"]["available"])
        self.assertFalse(
            result["models"]["vision_transformer"]["available"]
        )

    def test_only_cnn_model_available(self):
        self.cnn_path.touch()

        with patch(
            "backend.app.services.model_service.MODEL_PATHS",
            self.model_paths,
        ):
            result = get_model_status()

        self.assertEqual(result["status"], "pending")
        self.assertTrue(result["models"]["3d_cnn"]["available"])
        self.assertFalse(
            result["models"]["vision_transformer"]["available"]
        )

    def test_both_models_available(self):
        self.cnn_path.touch()
        self.vit_path.touch()

        with patch(
            "backend.app.services.model_service.MODEL_PATHS",
            self.model_paths,
        ):
            result = get_model_status()

        self.assertEqual(result["status"], "checkpoints_available")
        self.assertTrue(result["models"]["3d_cnn"]["available"])
        self.assertTrue(
            result["models"]["vision_transformer"]["available"]
        )


class TestDatasetValidationService(unittest.TestCase):

    def test_dataset_validation(self):
        result = validate_dataset()

        self.assertEqual(result["status"], "valid")
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

        self.assertTrue(
            all(result["checks"].values())
        )

    def test_dataset_dimensions(self):
        result = validate_dataset()

        self.assertEqual(
            result["details"]["image_shape"],
            [500, 64, 64, 100]
        )

        self.assertEqual(
            result["details"]["label_shape"],
            [500]
        )

        self.assertEqual(
            result["details"]["wavelength_shape"],
            [100]
        )


if __name__ == "__main__":
    unittest.main()
