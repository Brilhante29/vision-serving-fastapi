# #7 vision-serving-fastapi

**Status:** scaffold

**Proves:** servir modelo CV.

**Benchmark target:** throughput_rps, p95_latency_ms.

**Stack:** python, fastapi, onnxruntime, prometheus, k6, docker.

## Next milestone

Implement the smallest Docker-runnable version and produce the first JSON benchmark under enchmarks/results/.

## Run

`ash
docker build -t vision-serving-fastapi .
docker run --rm vision-serving-fastapi
`

## Benchmark

`ash
docker run --rm vision-serving-fastapi benchmark
`

| Metric | Value | Unit |
|---|---:|---|
| throughput_rps, p95_latency_ms | pending | pending |

## Architecture

Defined in sdd/spec.md before implementation.

## References

See REFERENCES.md.