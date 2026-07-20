# Architecture Decision

## Status

Accepted

## Context

Project: vision-serving-fastapi
Claim: servir modelo CV (server a computer vision model with measurable throughput/latency)
Benchmark: throughput_rps, p95_latency_ms

Problem forces:
- Domain complexity: low — single inference endpoint with mock model
- Integration pressure: low — no external services, databases, or queues
- UI state complexity: none — pure API
- Data/ML reproducibility: low — synthetic data, deterministic seed
- Auditability: low — no events or audit trail needed
- Throughput/async pressure: low — mock model with 10-50ms latency
- Independent deployability need: low — single Docker container

## Decision

Chosen architecture: modular-monolith

Reason:
A modular monolith with clear boundaries (domain/ → app/ → benchmark/) is the simplest architecture that proves the claim. FastAPI handles HTTP, Prometheus tracks metrics, and the mock model provides reproducible latency. No distributed components, event buses, or databases are needed.

Dependency rule:
- domain/ depends on nothing (pure Python dataclasses)
- app/ depends on domain/ (uses InferenceRequest/Response)
- benchmark/ depends on httpx (external) and domain/ (BenchmarkResult)

## Rejected Alternatives

| Alternative | Why rejected |
|---|---|
| hexagonal / clean architecture | Overkill — no ports/adapters needed when there is only one adapter (HTTP) |
| microservices | Single-function API does not justify network overhead |
| serverless | Benchmark reproducibility requires consistent runtime environment |

## Folder Layout

```
src/vision_serving/
  __init__.py     # version
  __main__.py     # entry point
  domain.py       # dataclasses
  model.py        # MockCVModel
  app.py          # FastAPI app
  benchmark.py    # load test
  cli.py          # argparse
tests/
  test_domain.py
  test_app.py
k6/
  benchmark.js
scripts/
  benchmark.ps1
  benchmark.sh
```

## Testing Strategy

- Unit tests: domain dataclasses (pure, no server needed)
- Integration tests: FastAPI TestClient for /predict and /health
- Benchmark: httpx-based concurrent load test, writes JSON result

## Consequences

Positive:
- Minimal code — proves the claim in under 500 lines
- Every component is independently testable
- Docker build + run in seconds

Tradeoffs:
- Mock model does not reflect real CV inference characteristics
- No GPU or ONNX optimization path

Migration path:
- Replace MockCVModel.predict() with ONNX Runtime inference
- Add image preprocessing pipeline
- Scale with Gunicorn workers or Kubernetes
