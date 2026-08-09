# Architecture Record

## Decision

Use a modular monolith with four explicit edges: checkpoint integrity, native Ultralytics inference, FastAPI transport and HTTP benchmark. One process is the correct deployment boundary because model memory, synchronous inference and telemetry share one lifecycle.

## Rejected Alternatives

- ONNX Runtime is rejected until an exported artifact, numerical-parity check and performance comparison exist.
- k6 is rejected for this baseline because the in-container HTTPX harness executes the exact public route with a deterministic valid PNG and no second service.
- Broker, database, cache and cloud adapters are rejected because this synchronous local workload has no matching semantics.
