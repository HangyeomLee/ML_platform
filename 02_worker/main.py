import os, json, time, random
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

QUEUE_KEY = "queue:inference"

def dummy_infer(task: str, payload: dict) -> dict:
    # 50~150ms fake latency
    time.sleep(random.uniform(0.05, 0.15))
    if task == "llm":
        text = payload.get("input", {}).get("text", "")
        return {"output": f"echo: {text}"}
    if task == "cv":
        return {"output": "cv_result_dummy"}
    return {"output": "unknown_task_dummy"}

def run():
    print("worker started, waiting for jobs...")
    while True:
        _, job_id = r.brpop(QUEUE_KEY)  # blocks
        key = f"job:{job_id}"
        job = r.hgetall(key)
        if not job:
            continue

        r.hset(key, mapping={"status": "running", "started_at_ms": str(int(time.time()*1000))})

        try:
            req = json.loads(job["request"])
            task = req.get("task", "llm")
            result = dummy_infer(task, req)
            r.hset(key, mapping={
                "status": "done",
                "finished_at_ms": str(int(time.time()*1000)),
                "result": json.dumps(result),
            })
        except Exception as e:
            r.hset(key, mapping={
                "status": "failed",
                "finished_at_ms": str(int(time.time()*1000)),
                "error": str(e),
            })

if __name__ == "__main__":
    run()