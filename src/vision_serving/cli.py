from __future__ import annotations

import argparse
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path


def serve(args: argparse.Namespace) -> None:
    import uvicorn

    uvicorn.run(
        "vision_serving.app:app",
        host=args.host,
        port=args.port,
        log_level=args.log_level,
    )


def benchmark(args: argparse.Namespace) -> None:
    from vision_serving.benchmark import run_with_server

    result = run_with_server(
        num_requests=args.num_requests,
        concurrency=args.concurrency,
        warmup_requests=args.warmup_requests,
    )
    payload = {
        "project": "vision-serving-fastapi",
        "metric": "throughput_rps",
        "value": round(result.throughput_rps, 6),
        "unit": "req/s",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "command": " ".join(sys.argv),
        "repeat": 1,
        "measured_iterations": result.total_requests,
        "samples": [round(result.throughput_rps, 6)],
        "failures": result.errors,
        "summary": {
            "p95_latency_ms": round(result.p95_latency_ms, 6),
            "total_requests": result.total_requests,
            "warmup_requests": result.warmup_requests,
            "concurrency": result.concurrency,
            "duration_seconds": round(result.duration_seconds, 6),
            "errors": result.errors,
            "model_sha256": result.model_sha256,
            "latency_samples_ms": [round(value, 6) for value in result.latency_samples_ms],
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "machine": platform.machine(),
        },
    }
    if result.errors:
        raise SystemExit(f"benchmark observed {result.errors} request errors")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(prog="vision-serving-fastapi")
    commands = parser.add_subparsers(dest="command", required=True)
    serve_parser = commands.add_parser("serve")
    serve_parser.add_argument("--host", default="0.0.0.0")
    serve_parser.add_argument("--port", type=int, default=8000)
    serve_parser.add_argument("--log-level", default="info")
    serve_parser.set_defaults(func=serve)
    benchmark_parser = commands.add_parser("benchmark")
    benchmark_parser.add_argument("--num-requests", type=int, default=20)
    benchmark_parser.add_argument("--concurrency", type=int, default=1)
    benchmark_parser.add_argument("--warmup-requests", type=int, default=3)
    benchmark_parser.add_argument("--output", default="benchmarks/results/benchmark.json")
    benchmark_parser.set_defaults(func=benchmark)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
