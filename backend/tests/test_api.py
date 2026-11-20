
import unittest

from fastapi.testclient import TestClient

from backend.app.main import app


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

    def test_model_status(self):
        response = client.get("/api/v1/model/status")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["framework"], "PyTorch")
        self.assertEqual(data["framework_version"], "2.15.0")
        self.assertEqual(data["device"], "cpu")
        self.assertEqual(
            data["models"]["3d_cnn"]["status"],
            "awaiting_model_files",
        )
        self.assertEqual(
            data["models"]["vision_transformer"]["status"],
            "awaiting_model_files",
        )

    def test_home_endpoint(self):
        response = client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "running")


if __name__ == "__main__":
    unittest.main()
