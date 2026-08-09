# Technical Decision

Use native Ultralytics with the exact version that produced `best.pt`. ONNX was rejected because no exported artifact or parity measurement exists; calling an unexecuted format part of the stack would be false. FastAPI is appropriate for multipart image upload and OpenAPI. Prometheus client owns the wire format. HTTPX drives the same public route a consumer uses.

The Docker image is larger than an ONNX-only runtime, but it closes the actual #1 -> #7 artifact path. ONNX becomes valid after repository #1 exports it and this repository measures numerical parity, size, startup, and throughput.
