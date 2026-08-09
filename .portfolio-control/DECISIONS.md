# Decision Register: #7 vision-serving-fastapi

| Decision | Selected option | Evidence or reason | Revisit trigger |
|---|---|---|---|
| Architecture | modular monolith | one process owns model startup, HTTP, metrics and benchmark | independent scaling boundary appears |
| API style | REST multipart HTTP | one bounded image produces one synchronous prediction; OpenAPI is useful | streaming or typed service-to-service callers dominate |
| Model runtime | native Ultralytics/PyTorch CPU | consumes the exact #1 checkpoint without an unproven export | ONNX export plus parity and performance evidence exists |
| Messaging | none | synchronous inference has no routing, replay or delivery semantics | async jobs or batching become measured requirements |
| Storage | committed immutable model bundle | one local artifact, verified before load | registry or object-store lifecycle becomes the claim |
| Local-first/cloud | offline Docker | default proof needs no cloud behavior or credentials | an object-storage contract requires Kumo parity |
| Benchmark | HTTPX against real PNG | exercises the public endpoint and checks stable model identity | a separate load profile requires k6 or distributed generation |

## Design Principles

- **SRP/DIP:** transport depends on the model prediction contract; Ultralytics stays in the adapter.
- **LSP:** injected test models and the real adapter preserve the same prediction contract.
- **ISP:** the API exposes health, predict and Prometheus metrics only.
- **KISS/YAGNI:** no broker, database, cloud, cache or dynamic batching without measured need.
