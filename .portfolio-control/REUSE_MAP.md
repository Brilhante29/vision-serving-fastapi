# Reuse Map: #7 vision-serving-fastapi

## Kit Inputs

| Concern | Source of truth | Project use |
|---|---|---|
| Agent graph | `.portfolio/decision-brain/agent-graph.yaml` | architecture, stack, benchmark and release sequence |
| Architecture | `.portfolio/architecture/decision-matrix.yaml` | select modular monolith from problem forces |
| Python profiles | `.portfolio/language-profiles/` | FastAPI and computer-vision conventions |
| Artifact contract | `.portfolio/contracts/vision-model-artifact.schema.json` | verify producer checkpoint before load |
| Benchmark contract | `benchmarks/publication-spec.json` | bind source, OCI image, workload and raw evidence |

## Project Delta

| Delta | Why it is project-specific or reusable | Action |
|---|---|---|
| checkpoint manifest and SHA gate | reusable between model producers and consumers | `patch_now` in kit publication guidance |
| real HTTP image benchmark | candidate; only one serving project proves it today | keep local until second use |
| Ultralytics adapter and image limits | tied to this model bundle and API | reject from kit |

## Coupling Rule

FastAPI and Ultralytics sit at composition edges. HTTP tests may inject a contract-compatible model; production must validate the immutable bundle before native framework load.
