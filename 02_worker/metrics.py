from prometheus_client import Counter, Histogram, Gauge

# Worker metrics
jobs_processed_total = Counter(
    "worker_jobs_processed_total", 
    "Total number of jobs processed", 
    ["task", "model", "status"]
)

job_processing_duration = Histogram(
    "worker_job_processing_duration_seconds", 
    "Time spent processing a job", 
    ["task", "model"]
)

active_jobs = Gauge(
    "worker_active_jobs", 
    "Number of jobs currently being processed"
)
