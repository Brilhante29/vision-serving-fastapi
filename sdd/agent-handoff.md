# Agent Handoff

This file stores observable state, not private reasoning.

- Project: `7 - vision-serving-fastapi`.
- Program: `applied-computer-vision`.
- Status: benchmarked; V2 publication is pending.
- Real artifact: `models/best.pt`, 5,333,317 bytes, SHA-256 `41598b005401dab39969719bf0678b55415121911fa72c110b21b75bab9c2e96`.
- Source: YOLO26n trained by #1 from architecture-only initialization on its synthetic fixture.
- Raw baseline: `45.553395 req/s`, p95 `28.662271 ms`, 20 requests, 0 errors.
- Limitation: this proves serving mechanics, not real-domain detection quality.

Continue by running tests, benchmark validator, publication validator, Docker build, and the exact offline benchmark. Do not restore a mock, random sleep, invalid image resize, or JSON-wrapped Prometheus response.
