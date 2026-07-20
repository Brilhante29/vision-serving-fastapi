# Benchmark Plan: vision-serving-fastapi

## Hypothesis

servir modelo CV, measured by throughput_rps and p95_latency_ms. Expected ~50-100 req/s with ~50-200ms p95 latency.

## Command

```bash
python -m vision_serving benchmark
```

Or via Docker:
```bash
docker build -t vision-serving-fastapi . && python -m vision_serving benchmark
```

## Environment

- OS: Windows 11 / Ubuntu 22.04
- CPU: any x86_64
- RAM: >= 2GB
- GPU: none (mock model)
- Docker version: any recent
- Date: 2026-07-20

## Inputs

- fixture: synthetic numpy random bytes (150528 = 224x224x3)
- dataset size: 1 fixture used repeatedly
- repetitions: 100 requests
- warmup: 0 (first request triggers model init)

## Metrics

| Metric | Unit | Source | Why it matters |
|---|---:|---|---|
| throughput_rps | req/s | benchmark script | proves the repo claim — how fast can we serve predictions |
| p95_latency_ms | ms | benchmark script | tail latency for the worst 5% of requests |

## Result schema

Output is JSON with project, metric, value, unit, total_requests, duration_seconds, and errors.

```json
{
  "project": "vision-serving-fastapi",
  "metric": "throughput_rps",
  "value": 85.42,
  "p95_latency_ms": 120.5,
  "total_requests": 100,
  "duration_seconds": 1.17,
  "errors": 0
}
```

## Post angle

#7 vision-serving-fastapi: throughput_rps and p95_latency_ms as a reproducible portfolio benchmark for CV model serving with FastAPI.
