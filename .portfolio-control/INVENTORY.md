# Portfolio Control: #7 vision-serving-fastapi

## Identity

- **Program:** applied-computer-vision
- **Status:** benchmarked; V2 publication pending
- **Proves:** verified YOLO checkpoint delivery through real FastAPI inference
- **Primary benchmark:** `throughput_rps`; secondary `p95_latency_ms`

## Evidence Map

| Evidence | Location | State |
|---|---|---|
| Specification | `sdd/spec.md` | complete |
| Architecture decision | `sdd/architecture-decision.md` | complete |
| Benchmark plan | `sdd/benchmark-plan.md` | complete |
| Raw benchmark result | `benchmarks/results/benchmark.json` | measured |
| Publication evidence | `benchmarks/publication/vision-serving-v2.json` | pending source-image run |
| OpenSpec verification | `openspec/artifacts/verification.md` | source gates complete |
| Reuse review | `sdd/reuse-improvement-review.md` | complete |
| Model bundle | `models/best.pt`, `models/model-manifest.json` | SHA-256 verified |
