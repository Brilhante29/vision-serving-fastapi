# Benchmark Proof

- Primary metric: `throughput_rps`.
- Secondary metric: `latency_ms_p95`.
- Workload: 20 measured POST requests after 3 warmups, concurrency 1.
- Input: deterministic valid PNG decoded through the public multipart endpoint.
- Model: `models/best.pt`, verified against `models/model-manifest.json` before load.
- Raw result: `benchmarks/results/benchmark.json`.
- Publication result: `benchmarks/publication/vision-serving-v2.json`.
- Measured baseline: `39.200 req/s`, p95 `27.343 ms`, 20 successes and zero errors.

The benchmark fails on HTTP errors, changing model identity or invalid response content.
