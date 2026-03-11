import json, time, logging, functools
import redis
from prometheus_client import start_http_server

from common.config import settings
from backends.llm_http import LLMHTTPBackend
from backends.cv_http import CVHTTPBackend
from metrics import jobs_processed_total, job_processing_duration, active_jobs

# Setup logging
logging.basicConfig(level=settings.LOG_LEVEL, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("worker")

# Redis setup
r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

def retry(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == retries - 1:
                        raise
                    logger.warning(f"Retry {i+1}/{retries} for {func.__name__} due to {str(e)}")
                    time.sleep(delay * (2 ** i))  # exponential backoff
        return wrapper
    return decorator

def get_backend(task: str, model: str, version: str):
    if task == "llm":
        return LLMHTTPBackend(model, version)
    elif task == "cv":
        return CVHTTPBackend(model, version)
    else:
        raise ValueError(f"Unknown task: {task}")

@retry(retries=3, delay=2)
def process_job(backend, req_data):
    return backend.infer(req_data.get("input", {}), req_data.get("params"))

def run():
    # Start metrics server (e.g., on port 9091)
    metrics_port = 9091
    start_http_server(metrics_port)
    logger.info(f"Worker metrics server started on port {metrics_port}")
    
    logger.info(f"Worker started, listening on queue: {settings.QUEUE_KEY}")
    while True:
        try:
            # BRPOP returns (list_name, item)
            res = r.brpop(settings.QUEUE_KEY, timeout=5)
            if not res:
                continue
            
            _, job_id = res
            key = f"job:{job_id}"
            job_data = r.hgetall(key)
            if not job_data:
                logger.warning(f"Job {job_id} not found in Redis.")
                continue

            # Update status to running
            r.hset(key, mapping={"status": "running", "started_at_ms": str(int(time.time()*1000))})
            logger.info(f"Processing job {job_id} (task: {job_data.get('task')})")

            # Parse request
            req_data = json.loads(job_data["request"])
            task = job_data.get("task", "llm")
            model = job_data.get("model", "default")
            version = job_data.get("version", "v1")

            # Select backend
            backend = get_backend(task, model, version)
            
            # Start tracking metrics
            active_jobs.inc()
            start_time = time.time()
            
            try:
                # Infer with retries
                result = process_job(backend, req_data)

                # Update result
                r.hset(key, mapping={
                    "status": "done",
                    "finished_at_ms": str(int(time.time()*1000)),
                    "result": json.dumps(result),
                })
                jobs_processed_total.labels(task, model, "success").inc()
                logger.info(f"Job {job_id} completed successfully.")
            
            except Exception as e:
                logger.error(f"Execution failed for job {job_id}: {str(e)}")
                r.hset(key, mapping={
                    "status": "failed",
                    "finished_at_ms": str(int(time.time()*1000)),
                    "error": str(e),
                })
                jobs_processed_total.labels(task, model, "failed").inc()
            
            finally:
                duration = time.time() - start_time
                job_processing_duration.labels(task, model).observe(duration)
                active_jobs.dec()

        except Exception as e:
            logger.error(f"Critical error in worker loop: {str(e)}")
            time.sleep(1)  # avoid tight error loop

if __name__ == "__main__":
    run()
