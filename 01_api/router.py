import json, time, uuid
from fastapi import APIRouter, HTTPException
from prometheus_client import Counter, Histogram
import redis

from common.schemas import JobRequest, JobCreateResponse, JobStatusResponse
from common.config import settings

# Redis setup
r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

# Metrics
jobs_created = Counter("jobs_created_total", "Jobs created", ["task", "model"])
jobs_get = Counter("jobs_get_total", "Job status fetched")

router = APIRouter(prefix="/v1/jobs", tags=["jobs"])

@router.post("", response_model=JobCreateResponse)
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
    r.lpush(settings.QUEUE_KEY, job_id)

    jobs_created.labels(req.task, req.model or "default").inc()
    return JobCreateResponse(job_id=job_id, status="queued")

@router.get("/{job_id}", response_model=JobStatusResponse)
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
