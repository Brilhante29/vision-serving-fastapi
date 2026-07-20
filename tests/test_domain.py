from vision_serving.domain import InferenceRequest, InferenceResponse, BenchmarkResult


def test_inference_request_defaults():
    req = InferenceRequest(image_bytes=b"test")
    assert req.image_bytes == b"test"
    assert req.timestamp > 0


def test_inference_response():
    resp = InferenceResponse(class_id=1, class_name="car", confidence=0.95, latency_ms=12.3)
    assert resp.class_id == 1
    assert resp.class_name == "car"
    assert resp.confidence == 0.95
    assert resp.latency_ms == 12.3


def test_benchmark_result():
    br = BenchmarkResult(throughput_rps=100.5, p95_latency_ms=45.2, total_requests=100, duration_seconds=5.0)
    assert br.throughput_rps == 100.5
    assert br.p95_latency_ms == 45.2
    assert br.total_requests == 100
    assert br.duration_seconds == 5.0
    assert br.errors == 0
