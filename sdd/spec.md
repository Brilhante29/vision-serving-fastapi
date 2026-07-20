# Spec: vision-serving-fastapi

## Number

#7

## Claim

servir modelo CV — serve a mock computer vision model via FastAPI and measure throughput/latency.

## Stack

python, fastapi, onnxruntime, prometheus, k6, docker

## User-visible output

- Docker command: `docker build -t vision-serving-fastapi . && docker run --rm -p 8000:8000 vision-serving-fastapi`
- README opens with: # #7 vision-serving-fastapi
- Benchmark table: throughput_rps, p95_latency_ms

## Scope

In:
- Mock CV model with synthetic latency (10-50ms sleep)
- FastAPI REST endpoint: POST /predict, GET /health, GET /metrics
- Python-based benchmark (httpx concurrent requests)
- k6 load test script for CI
- Prometheus metrics (request count, latency histogram)
- Docker image
- CI pipeline (test + benchmark)

Out:
- Real ONNX model weights
- GPU inference
- Image preprocessing beyond numpy resize
- Authentication/authorization
- Database persistence
- Distributed deployment

## Architecture

```
client -> FastAPI app -> MockCVModel -> InferenceResponse
                      -> Prometheus metrics
                      -> benchmark output (JSON)
```

## Benchmark

Primary metric:
- name: throughput_rps, p95_latency_ms
- target: first reproducible baseline
- command: `python -m vision_serving benchmark`
- result file: benchmarks/results/*.json

## Dataset or fixture

- source: synthetic (numpy random bytes)
- size: 150528 bytes (224x224x3 uint8)
- license: N/A (synthetic)
- deterministic seed: 42

## Definition of done

- [x] Docker command works from clean clone.
- [x] README starts with project number and benchmark result.
- [x] Benchmark command writes JSON result.
- [x] Tests cover core behavior.
- [x] REFERENCES.md explains reuse.
- [x] No secret or paid credential required for default demo.
