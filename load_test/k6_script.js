import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 50,          // 50 virtual users
  duration: '30s',  // for 30 seconds
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests must complete below 500ms
    'http_req_failed': ['rate<0.01'], // less than 1% errors
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';

export default function () {
  const payload = JSON.stringify({
    recent_prices: [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
    sma_20: [102, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    rsi_14: [50, 52, 54, 53, 55, 57, 56, 58, 60, 62],
    atr_14: [1.2, 1.3, 1.1, 1.4, 1.5, 1.6, 1.4, 1.3, 1.2, 1.1],
  });

  const params = {
    headers: { 'Content-Type': 'application/json' },
  };

  const res = http.post(`${BASE_URL}/signal`, payload, params);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response has tf_signal': (r) => JSON.parse(r.body).tf_signal !== undefined,
    'response has rl_signal': (r) => JSON.parse(r.body).rl_signal !== undefined,
  });

  sleep(1);
}

mkdir -p load_test
git add load_test/k6_script.js
git commit -m "Add k6 load testing script for /signal endpoint"
git push
