from vision_serving.domain import BenchmarkResult, InferenceResponse


def test_inference_response_is_model_identified() -> None:
    response = InferenceResponse(
        class_id=1,
        class_name="cool-ellipse",
        confidence=0.95,
        latency_ms=12.3,
        model_sha256="a" * 64,
    )
    assert response.class_name == "cool-ellipse"
    assert response.model_sha256 == "a" * 64


def test_benchmark_result_keeps_workload_and_samples() -> None:
    result = BenchmarkResult(
        throughput_rps=3.5,
        p95_latency_ms=40.2,
        total_requests=20,
        warmup_requests=3,
        concurrency=1,
        duration_seconds=5.7,
        errors=0,
        latency_samples_ms=(31.0, 40.2),
        model_sha256="b" * 64,
    )
    assert result.total_requests == 20
    assert result.errors == 0
    assert result.latency_samples_ms[-1] == 40.2
