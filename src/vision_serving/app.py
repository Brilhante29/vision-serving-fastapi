from __future__ import annotations

import time
from contextlib import asynccontextmanager

import numpy as np
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, generate_latest

from vision_serving.domain import InferenceResponse
from vision_serving.model import MockCVModel

model = MockCVModel()

REQUEST_COUNT = Counter("vision_requests_total", "Total inference requests")
LATENCY_HISTOGRAM = Histogram(
    "vision_latency_seconds",
    "Inference latency in seconds",
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0),
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _ = model.predict(np.zeros((224, 224, 3), dtype=np.uint8))
    yield


app = FastAPI(title="vision-serving-fastapi", version="0.1.0", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/metrics")
async def metrics():
    return JSONResponse(content=generate_latest().decode("utf-8"), media_type="text/plain")


@app.post("/predict", response_model=InferenceResponse)
async def predict(file: UploadFile):
    start = time.time()
    REQUEST_COUNT.inc()

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        image = np.frombuffer(contents, dtype=np.uint8)
        image = np.resize(image, (224, 224, 3))
    except Exception:
        image = np.zeros((224, 224, 3), dtype=np.uint8)

    class_id, class_name, confidence = model.predict(image)
    latency = (time.time() - start) * 1000
    LATENCY_HISTOGRAM.observe(latency / 1000)

    return InferenceResponse(
        class_id=class_id,
        class_name=class_name,
        confidence=confidence,
        latency_ms=round(latency, 2),
    )
