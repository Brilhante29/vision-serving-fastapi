# Reuse Improvement Review

Project: `7 - vision-serving-fastapi`

## Review Points

- [x] after scaffold
- [x] after architecture decision
- [x] after first working slice
- [x] after benchmark result
- [x] before publication

## Findings

| Finding | Classification | Kit Area | Action | Status |
|---|---|---|---|---|
| A model consumer must verify manifest schema, checkpoint bytes and SHA-256 before framework load. | `patch_now` | model artifact contract | Reuse the producer/consumer integrity gate and add it to the publication validation pattern. | implemented locally; kit patch queued in this macro |
| HTTP benchmarks need real requests, explicit warmup/concurrency and response-content stability checks. | `patch_now` | benchmark harness | Generalize publication metadata and validation; keep the FastAPI request driver project-local until a second serving repository proves duplication. | generic evidence patched; driver retained locally |
| Prometheus exposition must preserve the library content type and text wire format. | `backlog` | FastAPI profile | Record a focused integration pattern after a second service needs the same adapter. | recorded |

## Patch Now Decisions

- The reusable change is the provenance and integrity contract, not the Ultralytics adapter.
- Publication validation now rejects unverifiable source, image, fixture, configuration, lock or raw-result provenance.

## Backlog Decisions

- Promote the FastAPI/Prometheus adapter only after a second repository demonstrates stable duplication.
- Promote the HTTP load driver only after another synchronous inference API needs the same contract.

## Rejected Improvements

- The YOLO loader, image limits and endpoint schema stay here because they are product and workload specific.
- Dynamic batching, queues, cloud storage and a model registry are rejected until a benchmark requires them.

## Final Gate

- [x] Reusable improvements were patched or recorded.
- [x] Project-specific implementation was not moved into the kit.
- [x] Validation reflects the mock-serving and provenance mistakes discovered here.
