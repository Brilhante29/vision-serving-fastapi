from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "benchmarks" / "results" / "benchmark.json"
CHECKPOINT = ROOT / "models" / "best.pt"


def main() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["project"] == "vision-serving-fastapi"
    assert result["metric"] == "throughput_rps"
    assert result["value"] > 0
    assert result["unit"] == "req/s"
    assert result["failures"] == 0
    assert result["measured_iterations"] == 20
    assert result["repeat"] == 1
    summary = result["summary"]
    assert summary["total_requests"] == 20
    assert summary["warmup_requests"] == 3
    assert summary["concurrency"] == 1
    assert summary["errors"] == 0
    assert len(summary["latency_samples_ms"]) == 20
    assert summary["p95_latency_ms"] > 0
    digest = hashlib.sha256(CHECKPOINT.read_bytes()).hexdigest()
    assert summary["model_sha256"] == digest
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert f"{result['value']:.3f}" in readme
    assert f"{summary['p95_latency_ms']:.3f}" in readme
    print("benchmark_contract=passed")


if __name__ == "__main__":
    main()
