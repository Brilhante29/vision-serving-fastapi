# Spec: real YOLO serving

## Claim

Load a versioned YOLO checkpoint, reject tampering, serve actual inference over FastAPI, expose Prometheus metrics, and measure HTTP throughput plus p95 latency.

## Acceptance

- The default Docker image contains a non-empty checkpoint and manifest from #1.
- Startup fails when checkpoint SHA-256 or size differs from the manifest.
- `/predict` decodes a bounded real image and executes the model.
- `/metrics` uses Prometheus text exposition, not JSON encoding.
- Benchmark arguments control request count, warmup, and concurrency.
- The benchmark fails on request errors or inconsistent model identity.
- Tests replace the model boundary; Docker proves real integration.

## Non-Goals

- Claiming domain accuracy from the synthetic training fixture.
- GPU, batching, autoscaling, cache, database, broker, or cloud storage.
