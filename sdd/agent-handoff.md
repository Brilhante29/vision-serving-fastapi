# Agent Handoff

Project: `7 - vision-serving-fastapi`

## Principal Agent Summary

- Objective: Serve a mock CV model via FastAPI with measurable throughput/latency
- Portfolio program: applied-computer-vision
- Public proof claim: servir modelo CV (measure: throughput_rps, p95_latency_ms)
- Primary benchmark: throughput_rps
- Default runnable path: `docker build -t vision-serving-fastapi . && docker run --rm -p 8000:8000 vision-serving-fastapi`

## Subagent Decisions

| Role | Decision | Evidence Path | Status |
|---|---|---|---|
| `program-planner` | applied-computer-vision program; CV model serving demo | `project.yaml`, `sdd/spec.md` | completed |
| `architecture-selector` | modular-monolith; domain/app/benchmark boundaries | `sdd/architecture-decision.md` | completed |
| `engineering-principles-reviewer` | SRP via separate modules; no framework coupling in domain | `project.yaml`, `sdd/technical-decision.md` | completed |
| `stack-decision-agent` | FastAPI + Prometheus + httpx + numpy | `project.yaml`, `sdd/technical-decision.md` | completed |
| `api-style-agent` | REST over HTTP with JSON responses | API contract at /docs (OpenAPI) | completed |
| `cloud-local-first-agent` | No cloud dependencies; fully local with Docker | Dockerfile | completed |
| `messaging-agent` | None — synchronous request-response | `sdd/technical-decision.md` | completed |
| `language-profile-agent` | Python with fastapi-backend profile | repo layout, tests, tooling | completed |
| `benchmark-harness-agent` | httpx concurrent client; k6 script for CI | `sdd/benchmark-plan.md`, `benchmarks/results/` | completed |
| `design-system-agent` | README with benchmark table | `README.md` | completed |
| `security-reuse-reviewer` | No secrets, no credentials, no paid services | `REFERENCES.md`, release checklist | completed |
| `release-ci-publisher` | CI pipeline: test → benchmark → docker build | `.github/workflows/ci.yml` | completed |

## Local-First Runtime

- Docker command: `docker build -t vision-serving-fastapi . && docker run --rm -p 8000:8000 vision-serving-fastapi`
- Local services: none
- Kumo services: none
- Real cloud adapter target: none
- Config switch: CLOUD_PROVIDER=none
- Default path requires paid secret: no

## Architecture Boundaries

- Domain boundaries: `domain.py` — pure dataclasses with no imports
- Use-case boundaries: `app.py` — FastAPI routes, depends on domain and model
- Ports: `MockCVModel.predict(image: np.ndarray) -> tuple[int, str, float]`
- Adapters: `app.py` is the HTTP adapter; `benchmark.py` is the load test adapter
- Dependency direction rule: app/ depends on domain/; benchmark/ depends on domain/; domain/ depends on nothing

## Benchmark Handoff

- Metric: throughput_rps
- Unit: req/s
- Higher or lower is better: higher
- Command: `python -m vision_serving benchmark`
- Result path: `benchmarks/results/benchmark.json`
- Dataset or fixture: synthetic numpy random bytes (150528)

## Open Risks

None — all decisions made, implementation complete.

## Publication Gates

- [x] Docker path works
- [x] benchmark result exists
- [x] README starts with number, claim, and benchmark
- [x] references are documented
- [x] no secret in files or git remote
- [x] validation passes
