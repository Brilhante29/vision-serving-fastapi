# Benchmark Plan

- Primary: successful HTTP requests per second.
- Secondary: nearest-rank p95 request latency.
- Workload: one deterministic 160x160 PNG, 3 warmups, 20 measured requests, concurrency 1.
- Failure rule: any non-200 response, transport error, or model identity change fails the run.
- Runtime: pinned CPU Docker image with `--network none`.
- Artifact: checkpoint SHA `41598b005401dab39969719bf0678b55415121911fa72c110b21b75bab9c2e96`.

The profile isolates single-request CPU serving. Higher concurrency and GPU batching are different comparability keys.
