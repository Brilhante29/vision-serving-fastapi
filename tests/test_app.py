from __future__ import annotations

import io

from fastapi.testclient import TestClient
from PIL import Image

from vision_serving.app import create_app


class FakeModel:
    image_size = 160
    model_sha256 = "a" * 64

    def predict(self, image):
        assert image.shape[2] == 3
        return 0, "warm-rectangle", 0.75


def png_bytes() -> bytes:
    stream = io.BytesIO()
    Image.new("RGB", (32, 32), (10, 20, 30)).save(stream, format="PNG")
    return stream.getvalue()


def test_health_and_prediction_expose_model_identity() -> None:
    with TestClient(create_app(FakeModel())) as client:
        health = client.get("/health")
        assert health.status_code == 200
        assert health.json() == {"status": "ok", "model_sha256": "a" * 64}
        response = client.post(
            "/predict",
            files={"file": ("fixture.png", png_bytes(), "image/png")},
        )
        assert response.status_code == 200
        assert response.json()["class_name"] == "warm-rectangle"
        assert response.json()["model_sha256"] == "a" * 64


def test_invalid_images_fail_closed() -> None:
    with TestClient(create_app(FakeModel())) as client:
        assert client.post("/predict", files={"file": ("empty.png", b"")}).status_code == 400
        assert client.post("/predict", files={"file": ("bad.png", b"not-image")}).status_code == 422


def test_prometheus_endpoint_uses_text_wire_format() -> None:
    with TestClient(create_app(FakeModel())) as client:
        client.post("/predict", files={"file": ("fixture.png", png_bytes(), "image/png")})
        response = client.get("/metrics")
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/plain")
        assert 'vision_requests_total{status="ok"} 1.0' in response.text
