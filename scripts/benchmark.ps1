param(
    [string]$ImageName = "vision-serving-fastapi",
    [int]$Port = 8000,
    [string]$ResultDir = "benchmarks/results"
)

$ErrorActionPreference = "Stop"
$containerName = "vision-serving-bench-$([System.Guid]::NewGuid().ToString().Substring(0,8))"

Write-Host "Building Docker image..." -ForegroundColor Cyan
docker build -t $ImageName .

Write-Host "Starting container..." -ForegroundColor Cyan
docker run -d --name $containerName -p ${Port}:8000 $ImageName

try {
    Start-Sleep -Seconds 3

    Write-Host "Waiting for server..." -ForegroundColor Cyan
    $maxRetries = 15
    $retry = 0
    do {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:${Port}/health" -UseBasicParsing -TimeoutSec 2
            if ($response.StatusCode -eq 200) { break }
        } catch {}
        $retry++
        Start-Sleep -Seconds 1
    } while ($retry -lt $maxRetries)

    if ($retry -eq $maxRetries) {
        throw "Server did not start in time"
    }

    Write-Host "Running k6 benchmark..." -ForegroundColor Cyan
    docker run --rm --network host `
        -e BASE_URL="http://host.docker.internal:${Port}" `
        -v "${PWD}/k6:/k6" `
        grafana/k6 run /k6/benchmark.js

    if (-not (Test-Path $ResultDir)) {
        New-Item -ItemType Directory -Path $ResultDir -Force
    }
} finally {
    Write-Host "Cleaning up..." -ForegroundColor Cyan
    docker stop $containerName 2>$null
    docker rm $containerName 2>$null
}
