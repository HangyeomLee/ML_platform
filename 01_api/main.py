import os, json, time, uuid
from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import redis

from common.schemas import JobRequest, JobCreateResponse, JobStatusResponse

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

QUEUE_KEY = "queue:inference"

jobs_created = Counter("jobs_created_total", "Jobs created", ["task", "model"])
jobs_get = Counter("jobs_get_total", "Job status fetched")
http_latency = Histogram("http_request_latency_seconds", "HTTP latency", ["path", "method"])

app = FastAPI(title="ML Inference Gateway (B-MVP)")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/v1/jobs", response_model=JobCreateResponse)
def create_job(req: JobRequest):
    job_id = f"j_{uuid.uuid4().hex[:16]}"
    now = int(time.time() * 1000)

    job = {
        "status": "queued",
        "task": req.task,
        "model": req.model or "default",
        "version": req.version or "v1",
        "created_at_ms": str(now),
        "request": req.model_dump_json(),
    }
    r.hset(f"job:{job_id}", mapping=job)
    r.lpush(QUEUE_KEY, job_id)

    jobs_created.labels(req.task, req.model or "default").inc()
    return JobCreateResponse(job_id=job_id, status="queued")

@app.get("/v1/jobs/{job_id}", response_model=JobStatusResponse)
def get_job(job_id: str):
    jobs_get.inc()
    data = r.hgetall(f"job:{job_id}")
    if not data:
        raise HTTPException(status_code=404, detail="Job not found")

    # Parse result if exists
    result = None
    if "result" in data and data["result"]:
        try:
            result = json.loads(data["result"])
        except Exception:
            result = {"raw": data["result"]}

    return JobStatusResponse(
        job_id=job_id,
        status=data.get("status", "unknown"),
        result=result,
        error=data.get("error"),
    )

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)