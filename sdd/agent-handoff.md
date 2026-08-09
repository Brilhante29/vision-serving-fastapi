# Agent Handoff

This file stores observable state, not private reasoning.

- Project: `7 - vision-serving-fastapi`.
- Program: `applied-computer-vision`.
- Status: published.
- Model: `models/best.pt`, 5,333,317 bytes, SHA-256 `41598b005401dab39969719bf0678b55415121911fa72c110b21b75bab9c2e96`.
- Raw result: `39.200466 req/s`, p95 `27.342735 ms`, 20 requests, 0 errors.
- V2: source `d630c381d077d2212d949c59d6343360f537fa52`, image `sha256:77664c4a738e54a7ae72936cc34d7f32681e0c5ce3433c1fdb15a4ba9bdf5974`.
- Source CI: run `31341451764` passed.
- Limitation: this proves verified model delivery, not real-domain detection quality.

Do not restore a mock, random sleep, invalid image bytes, JSON-wrapped Prometheus response or unproven ONNX claim. The central registry records final publication CI.
