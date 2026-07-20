from __future__ import annotations

import asyncio
import time

import httpx
import numpy as np

from vision_serving.domain import BenchmarkResult


def _dummy_image_bytes(size: int = 150528) -> bytes:
    return np.random.randint(0, 256, size=size, dtype=np.uint8).tobytes()


def _wait_for_server(url: str, timeout: float = 15.0) -> bool:
    import urllib.request
    from urllib.error import URLError

    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            resp = urllib.request.urlopen(f"{url}/health", timeout=2)
            if resp.status == 200:
                return True
        except (URLError, ConnectionError, OSError):
            pass
        time.sleep(0.3)
    return False


async def _run_benchmark(
    url: str,
    num_requests: int = 100,
    concurrency: int = 10,
) -> BenchmarkResult:
    image_bytes = _dummy_image_bytes()
    latencies: list[float] = []
    errors = 0
    sem = asyncio.Semaphore(concurrency)

    async def _send(client: httpx.AsyncClient) -> None:
        nonlocal errors
        async with sem:
            start = time.time()
            try:
                resp = await client.post(
                    f"{url}/predict",
                    files={"file": ("image.bin", image_bytes)},
                    timeout=30.0,
                )
                if resp.status_code != 200:
                    errors += 1
            except Exception:
                errors += 1
            elapsed = (time.time() - start) * 1000
            latencies.append(elapsed)

    async with httpx.AsyncClient() as client:
        wall_start = time.time()
        tasks = [asyncio.create_task(_send(client)) for _ in range(num_requests)]
        await asyncio.gather(*tasks)
        wall_duration = time.time() - wall_start

    latencies.sort()
    n = len(latencies)
    p95_idx = max(0, min(n - 1, int(n * 0.95)))
    p95_latency = latencies[p95_idx]

    return BenchmarkResult(
        throughput_rps=num_requests / wall_duration if wall_duration > 0 else 0,
        p95_latency_ms=p95_latency,
        total_requests=num_requests,
        duration_seconds=round(wall_duration, 3),
        errors=errors,
    )


def run(url: str = "http://localhost:8000", num_requests: int = 100, concurrency: int = 10) -> BenchmarkResult:
    result = asyncio.run(_run_benchmark(url, num_requests, concurrency))
    return result


def run_with_server() -> BenchmarkResult:
    import uvicorn
    import threading

    from vision_serving.app import app

    port = _find_free_port()
    url = f"http://localhost:{port}"

    server_config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="error")
    server = uvicorn.Server(server_config)
    thread = threading.Thread(target=server.run)
    thread.daemon = True
    thread.start()

    if not _wait_for_server(url):
        raise RuntimeError("Server did not start in time")

    result = run(url)
    return result


def _find_free_port() -> int:
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]
