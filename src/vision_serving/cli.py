from __future__ import annotations

import argparse
import json
import os
import sys


def cmd_serve(args: argparse.Namespace) -> None:
    import uvicorn

    uvicorn.run(
        "vision_serving.app:app",
        host=args.host,
        port=args.port,
        log_level=args.log_level,
    )


def cmd_benchmark(args: argparse.Namespace) -> None:
    from vision_serving.benchmark import run_with_server

    result = run_with_server()
    output = {
        "project": "vision-serving-fastapi",
        "metric": "throughput_rps",
        "value": round(result.throughput_rps, 2),
        "p95_latency_ms": round(result.p95_latency_ms, 2),
        "total_requests": result.total_requests,
        "duration_seconds": result.duration_seconds,
        "errors": result.errors,
    }

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(output, f, indent=2)
        print(f"Benchmark result written to {args.output}")
    else:
        print(json.dumps(output, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(prog="vision-serving-fastapi")
    sub = parser.add_subparsers(dest="command", required=True)

    serve_parser = sub.add_parser("serve", help="Start the FastAPI inference server")
    serve_parser.add_argument("--host", default="0.0.0.0")
    serve_parser.add_argument("--port", type=int, default=8000)
    serve_parser.add_argument("--log-level", default="info")
    serve_parser.set_defaults(func=cmd_serve)

    bench_parser = sub.add_parser("benchmark", help="Run benchmark")
    bench_parser.add_argument("--num-requests", type=int, default=100)
    bench_parser.add_argument("--concurrency", type=int, default=10)
    bench_parser.add_argument("--output", default="benchmarks/results/benchmark.json")
    bench_parser.set_defaults(func=cmd_benchmark)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
