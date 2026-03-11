import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 10,
  duration: '30s',
};

const BASE_URL = 'http://localhost:8000';

export default function () {
  const payload = JSON.stringify({
    task: 'llm',
    model: 'gpt-dummy',
    input: { text: 'Hello, load test!' }
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  // 1. Create Job
  const createRes = http.post(`${BASE_URL}/v1/jobs`, payload, params);
  check(createRes, {
    'create job status is 200': (r) => r.status === 200,
  });

  const jobData = JSON.parse(createRes.body);
  const jobId = jobData.job_id;

  // 2. Poll for Job Status (simplified)
  let status = 'queued';
  let retries = 0;
  while (status !== 'done' && status !== 'failed' && retries < 5) {
    sleep(1);
    const statusRes = http.get(`${BASE_URL}/v1/jobs/${jobId}`);
    check(statusRes, {
      'get job status is 200': (r) => r.status === 200,
    });
    
    const statusData = JSON.parse(statusRes.body);
    status = statusData.status;
    retries++;
  }

  check(status, {
    'job completed successfully': (s) => s === 'done',
  });

  sleep(1);
}
