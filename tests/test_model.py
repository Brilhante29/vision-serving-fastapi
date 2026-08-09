from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from vision_serving.model import ModelContractError, UltralyticsCVModel


class FakePredictor:
    def predict(self, **kwargs):
        assert kwargs["device"] == "cpu"
        boxes = SimpleNamespace(conf=np.array([0.3, 0.9]), cls=np.array([1, 0]))
        boxes.__len__ = lambda: 2
        return [SimpleNamespace(boxes=BoxCollection(boxes.conf, boxes.cls))]


class BoxCollection:
    def __init__(self, confidence, classes):
        self.conf = confidence
        self.cls = classes

    def __len__(self):
        return len(self.conf)


def artifact(tmp_path: Path) -> Path:
    checkpoint = tmp_path / "best.pt"
    checkpoint.write_bytes(b"real-checkpoint-bytes")
    digest = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
    manifest = {
        "schema_version": 1,
        "task": "detection",
        "format": "ultralytics-pt",
        "framework": {"name": "ultralytics", "version": "test"},
        "model": {"architecture": "test", "parameters": 1},
        "input": {"height": 160, "width": 160, "channels": 3, "color_space": "RGB", "dtype": "uint8", "batch": 1},
        "classes": [{"id": 0, "name": "warm-rectangle"}, {"id": 1, "name": "cool-ellipse"}],
        "checkpoint": {"file": "best.pt", "sha256": digest, "bytes": checkpoint.stat().st_size},
        "provenance": {"dataset_sha256": "a" * 64, "seed": 42},
        "metrics": {"map50_95": 0.1},
    }
    (tmp_path / "model-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return tmp_path


def test_model_validates_bundle_and_selects_best_detection(tmp_path: Path) -> None:
    model = UltralyticsCVModel(artifact(tmp_path), predictor=FakePredictor())
    class_id, class_name, confidence = model.predict(np.zeros((160, 160, 3), dtype=np.uint8))
    assert (class_id, class_name, confidence) == (0, "warm-rectangle", 0.9)


def test_model_rejects_tampered_checkpoint(tmp_path: Path) -> None:
    directory = artifact(tmp_path)
    (directory / "best.pt").write_bytes(b"tampered")
    with pytest.raises(ModelContractError, match="SHA-256"):
        UltralyticsCVModel(directory, predictor=FakePredictor())
