#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="${1:-vision-serving-fastapi}"
PORT="${2:-8000}"
RESULT_DIR="benchmarks/results"
CONTAINER_NAME="vision-serving-bench-$(uuidgen | cut -d- -f1)"

echo "Building Docker image..."
docker build -t "$IMAGE_NAME" .

echo "Starting container..."
docker run -d --name "$CONTAINER_NAME" -p "$PORT:8000" "$IMAGE_NAME"

cleanup() {
    echo "Cleaning up..."
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
}
trap cleanup EXIT

sleep 3

echo "Waiting for server..."
for i in $(seq 1 15); do
    if curl -sf "http://localhost:${PORT}/health" > /dev/null 2>&1; then
        echo "Server is ready"
        break
    fi
    sleep 1
done

echo "Running k6 benchmark..."
docker run --rm --network host \
    -e "BASE_URL=http://host.docker.internal:${PORT}" \
    -v "$(pwd)/k6:/k6" \
    grafana/k6 run /k6/benchmark.js

mkdir -p "$RESULT_DIR"
