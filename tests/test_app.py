import numpy as np
from fastapi.testclient import TestClient

from vision_serving.app import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_predict_valid():
    image_bytes = np.random.randint(0, 256, size=150528, dtype=np.uint8).tobytes()
    resp = client.post("/predict", files={"file": ("image.bin", image_bytes)})
    assert resp.status_code == 200
    data = resp.json()
    assert "class_id" in data
    assert "class_name" in data
    assert "confidence" in data
    assert "latency_ms" in data
    assert isinstance(data["class_id"], int)
    assert isinstance(data["confidence"], float)
    assert data["latency_ms"] > 0


def test_predict_empty_file():
    resp = client.post("/predict", files={"file": ("empty.bin", b"")})
    assert resp.status_code == 400


def test_predict_no_file():
    resp = client.post("/predict")
    assert resp.status_code == 422


def test_metrics():
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert "vision_requests_total" in resp.text
