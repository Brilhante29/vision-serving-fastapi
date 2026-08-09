from __future__ import annotations

import asyncio
import io
import math
import socket
import threading
import time

import httpx
from PIL import Image, ImageDraw

from vision_serving.domain import BenchmarkResult


def fixture_image_bytes(size: int = 160) -> bytes:
    image = Image.new("RGB", (size, size), (30, 35, 40))
    draw = ImageDraw.Draw(image)
    draw.rectangle((35, 45, 125, 115), fill=(230, 110, 45))
    stream = io.BytesIO()
    image.save(stream, format="PNG")
    return stream.getvalue()


async def run(
    url: str,
    *,
    num_requests: int,
    concurrency: int,
    warmup_requests: int,
) -> BenchmarkResult:
    if num_requests < 1 or concurrency < 1 or warmup_requests < 0:
        raise ValueError("invalid benchmark dimensions")
    image_bytes = fixture_image_bytes()
    latencies: list[float] = []
    errors = 0
    model_hashes: set[str] = set()
    semaphore = asyncio.Semaphore(concurrency)

    async with httpx.AsyncClient(timeout=60.0) as client:
        for _ in range(warmup_requests):
            response = await client.post(url + "/predict", files={"file": ("fixture.png", image_bytes, "image/png")})
            response.raise_for_status()
            model_hashes.add(response.json()["model_sha256"])

        async def send() -> None:
            nonlocal errors
            async with semaphore:
                started = time.perf_counter()
                try:
                    response = await client.post(
                        url + "/predict",
                        files={"file": ("fixture.png", image_bytes, "image/png")},
                    )
                    if response.status_code != 200:
                        errors += 1
                    else:
                        model_hashes.add(response.json()["model_sha256"])
                except httpx.HTTPError:
                    errors += 1
                latencies.append((time.perf_counter() - started) * 1000)

        wall_started = time.perf_counter()
        await asyncio.gather(*(send() for _ in range(num_requests)))
        duration = time.perf_counter() - wall_started

    ordered = sorted(latencies)
    p95_index = max(0, math.ceil(0.95 * len(ordered)) - 1)
    if len(model_hashes) != 1:
        raise RuntimeError("benchmark observed zero or multiple model identities")
    return BenchmarkResult(
        throughput_rps=(num_requests - errors) / duration,
        p95_latency_ms=ordered[p95_index],
        total_requests=num_requests,
        warmup_requests=warmup_requests,
        concurrency=concurrency,
        duration_seconds=duration,
        errors=errors,
        latency_samples_ms=tuple(latencies),
        model_sha256=model_hashes.pop(),
    )


def run_with_server(*, num_requests: int, concurrency: int, warmup_requests: int) -> BenchmarkResult:
    import uvicorn

    from vision_serving.app import create_app

    port = _find_free_port()
    url = f"http://127.0.0.1:{port}"
    server = uvicorn.Server(uvicorn.Config(create_app(), host="127.0.0.1", port=port, log_level="error"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    try:
        _wait_for_server(url)
        return asyncio.run(
            run(
                url,
                num_requests=num_requests,
                concurrency=concurrency,
                warmup_requests=warmup_requests,
            )
        )
    finally:
        server.should_exit = True
        thread.join(timeout=10)


def _wait_for_server(url: str, timeout_seconds: float = 60.0) -> None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        try:
            with httpx.Client(timeout=1.0) as client:
                if client.get(url + "/health").status_code == 200:
                    return
        except httpx.HTTPError:
            pass
        time.sleep(0.2)
    raise RuntimeError("inference server did not become ready")


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
        stream.bind(("127.0.0.1", 0))
        return int(stream.getsockname()[1])
