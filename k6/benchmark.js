import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const failureRate = new Rate('failed_requests');
const latencyTrend = new Trend('latency_ms');

export const options = {
  stages: [
    { duration: '10s', target: 10 },
    { duration: '10s', target: 20 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    failed_requests: ['rate<0.1'],
    latency_ms: ['p(95)<500'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';
const dummyImage = new Uint8Array(150528).fill(42);

export default function () {
  const payload = {
    file: http.file(dummyImage, 'image.bin', 'application/octet-stream'),
  };

  const params = {
    tags: { name: 'predict' },
  };

  const res = http.post(`${BASE_URL}/predict`, payload, params);
  latencyTrend.add(res.timings.duration);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'has prediction': (r) => r.json('class_id') !== undefined,
  });

  failureRate.add(res.status !== 200);
  sleep(0.1);
}

export function handleSummary(data) {
  const metrics = data.metrics;
  return {
    'stdout': JSON.stringify({
      project: 'vision-serving-fastapi',
      metric: 'throughput_rps',
      value: Math.round(metrics.http_reqs.values.rate),
      p95_latency_ms: metrics.latency_ms ? metrics.latency_ms['p(95)'] : metrics.http_req_duration['p(95)'],
      total_requests: metrics.http_reqs.values.count,
      duration_seconds: metrics.http_reqs.values.rate > 0
        ? Math.round(metrics.http_reqs.values.count / metrics.http_reqs.values.rate)
        : 0,
      errors: Math.round(metrics.failed_requests ? metrics.failed_requests.values.count : 0),
    }),
  };
}
