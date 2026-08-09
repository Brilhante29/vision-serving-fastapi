from __future__ import annotations

import io
import os
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import numpy as np
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import Response
from PIL import Image, UnidentifiedImageError
from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, Counter, Histogram, generate_latest

from vision_serving.domain import InferenceResponse
from vision_serving.model import UltralyticsCVModel

MAX_IMAGE_BYTES = 5 * 1024 * 1024


def default_artifact_dir() -> Path:
    configured = os.environ.get("VISION_MODEL_DIR")
    if configured:
        return Path(configured)
    return Path(__file__).resolve().parents[2] / "models"


def create_app(model: Any | None = None) -> FastAPI:
    registry = CollectorRegistry()
    request_count = Counter(
        "vision_requests_total",
        "Total inference requests",
        ("status",),
        registry=registry,
    )
    latency = Histogram(
        "vision_inference_seconds",
        "End-to-end inference latency in seconds",
        buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5),
        registry=registry,
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if app.state.model is None:
            app.state.model = UltralyticsCVModel(default_artifact_dir())
        warmup = np.zeros(
            (app.state.model.image_size, app.state.model.image_size, 3),
            dtype=np.uint8,
        )
        app.state.model.predict(warmup)
        yield

    app = FastAPI(title="vision-serving-fastapi", version="0.2.0", lifespan=lifespan)
    app.state.model = model

    @app.get("/health")
    async def health() -> dict[str, str]:
        loaded = app.state.model
        return {
            "status": "ok" if loaded is not None else "starting",
            "model_sha256": getattr(loaded, "model_sha256", "unloaded"),
        }

    @app.get("/metrics")
    async def metrics() -> Response:
        return Response(content=generate_latest(registry), media_type=CONTENT_TYPE_LATEST)

    @app.post("/predict", response_model=InferenceResponse)
    async def predict(file: UploadFile) -> InferenceResponse:
        started = time.perf_counter()
        contents = await file.read(MAX_IMAGE_BYTES + 1)
        if not contents:
            request_count.labels(status="invalid").inc()
            raise HTTPException(status_code=400, detail="empty image")
        if len(contents) > MAX_IMAGE_BYTES:
            request_count.labels(status="invalid").inc()
            raise HTTPException(status_code=413, detail="image exceeds 5 MiB")
        try:
            with Image.open(io.BytesIO(contents)) as decoded:
                image = np.asarray(decoded.convert("RGB"))
        except (UnidentifiedImageError, OSError, ValueError) as error:
            request_count.labels(status="invalid").inc()
            raise HTTPException(status_code=422, detail="invalid image") from error
        class_id, class_name, confidence = app.state.model.predict(image)
        elapsed = time.perf_counter() - started
        request_count.labels(status="ok").inc()
        latency.observe(elapsed)
        return InferenceResponse(
            class_id=class_id,
            class_name=class_name,
            confidence=round(confidence, 6),
            latency_ms=round(elapsed * 1000, 6),
            model_sha256=app.state.model.model_sha256,
        )

    return app


app = create_app()
