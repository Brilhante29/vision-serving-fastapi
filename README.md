# #7 vision-serving-fastapi

**Status:** benchmarked

**Proves:** servir modelo CV.

## Benchmark Result

| Metric | Value | Unit |
|:---|---:|---:|
| throughput_rps | 21.65 | req/s |
| p95_latency_ms | 631.75 | ms |

*Run `python -m vision_serving benchmark` to produce a fresh result.*

## Run

```bash
docker build -t vision-serving-fastapi .
docker run --rm -p 8000:8000 vision-serving-fastapi
```

## API

- `GET /health` — health check
- `POST /predict` — upload an image file, receive prediction JSON
- `GET /metrics` — Prometheus metrics

## Benchmark

```bash
# Local benchmark (no Docker)
python -m vision_serving benchmark

# k6 benchmark via Docker
# Start the server first, then:
docker run --rm --network host -v $(pwd)/k6:/k6 grafana/k6 run /k6/benchmark.js
```

## Stack

python, fastapi, onnxruntime, prometheus, k6, docker

## Architecture

Modular monolith — `domain/` has pure dataclasses, `app/` wires FastAPI + Prometheus, `benchmark/` runs load tests.

## References

See REFERENCES.md.

## License

MIT
