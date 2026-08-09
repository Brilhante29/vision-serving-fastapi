from __future__ import annotations

from vision_serving.benchmark import fixture_image_bytes


def test_benchmark_fixture_is_a_real_png() -> None:
    payload = fixture_image_bytes()
    assert payload.startswith(b"\x89PNG\r\n\x1a\n")
