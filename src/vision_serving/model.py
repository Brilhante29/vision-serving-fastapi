from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np


class ModelContractError(ValueError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


class UltralyticsCVModel:
    def __init__(self, artifact_dir: Path, predictor: Any | None = None) -> None:
        self.artifact_dir = artifact_dir.resolve()
        manifest_path = self.artifact_dir / "model-manifest.json"
        if not manifest_path.is_file():
            raise ModelContractError("model-manifest.json is required")
        self.manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if self.manifest.get("schema_version") != 1:
            raise ModelContractError("unsupported model manifest schema")
        if self.manifest.get("task") != "detection":
            raise ModelContractError("only detection artifacts are supported")
        checkpoint = self.manifest.get("checkpoint", {})
        checkpoint_name = checkpoint.get("file")
        if not isinstance(checkpoint_name, str) or Path(checkpoint_name).name != checkpoint_name:
            raise ModelContractError("invalid checkpoint filename")
        self.checkpoint_path = self.artifact_dir / checkpoint_name
        if not self.checkpoint_path.is_file():
            raise ModelContractError("checkpoint file is missing")
        self.model_sha256 = sha256_file(self.checkpoint_path)
        if checkpoint.get("sha256") != self.model_sha256:
            raise ModelContractError("checkpoint SHA-256 does not match manifest")
        if checkpoint.get("bytes") != self.checkpoint_path.stat().st_size:
            raise ModelContractError("checkpoint size does not match manifest")
        input_contract = self.manifest.get("input", {})
        self.image_size = int(input_contract.get("height", 0))
        if self.image_size < 32 or input_contract.get("width") != self.image_size:
            raise ModelContractError("square positive input dimensions are required")
        classes = self.manifest.get("classes", [])
        self.class_names = {int(item["id"]): str(item["name"]) for item in classes}
        if not self.class_names:
            raise ModelContractError("at least one model class is required")
        if predictor is None:
            from ultralytics import YOLO

            predictor = YOLO(str(self.checkpoint_path))
        self._predictor = predictor

    def predict(self, image: np.ndarray) -> tuple[int, str, float]:
        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError("RGB image array is required")
        results = self._predictor.predict(
            source=image,
            imgsz=self.image_size,
            device="cpu",
            verbose=False,
        )
        if not results:
            return -1, "no_detection", 0.0
        boxes = results[0].boxes
        if boxes is None or len(boxes) == 0:
            return -1, "no_detection", 0.0
        confidences = _as_numpy(boxes.conf).astype(float)
        classes = _as_numpy(boxes.cls).astype(int)
        best = int(np.argmax(confidences))
        class_id = int(classes[best])
        return class_id, self.class_names.get(class_id, f"class_{class_id}"), float(confidences[best])


def _as_numpy(value: Any) -> np.ndarray:
    if hasattr(value, "detach"):
        value = value.detach()
    if hasattr(value, "cpu"):
        value = value.cpu()
    if hasattr(value, "numpy"):
        value = value.numpy()
    return np.asarray(value)
