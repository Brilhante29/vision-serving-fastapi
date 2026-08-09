from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InferenceResponse:
    class_id: int
    class_name: str
    confidence: float
    latency_ms: float
    model_sha256: str


@dataclass(frozen=True)
class BenchmarkResult:
    throughput_rps: float
    p95_latency_ms: float
    total_requests: int
    warmup_requests: int
    concurrency: int
    duration_seconds: float
    errors: int
    latency_samples_ms: tuple[float, ...]
    model_sha256: str
