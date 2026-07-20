from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import List


@dataclass
class InferenceRequest:
    image_bytes: bytes
    timestamp: float = field(default_factory=time.time)


@dataclass
class InferenceResponse:
    class_id: int
    class_name: str
    confidence: float
    latency_ms: float


@dataclass
class BenchmarkResult:
    throughput_rps: float
    p95_latency_ms: float
    total_requests: int
    duration_seconds: float
    errors: int = 0
