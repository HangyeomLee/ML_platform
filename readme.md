# ML Inference Platform

A scalable, asynchronous ML inference platform built with FastAPI, Redis, and Python workers.

## Architecture

1.  **API Gateway (`01_api`)**: FastAPI application that receives inference requests and manages job status.
2.  **Message Broker (Redis)**: Stores job metadata (Hash) and the task queue (List).
3.  **Worker (`02_worker`)**: Consumes jobs from Redis and executes inference using a modular backend strategy.
4.  **Common (`03_common`)**: Shared schemas and configuration.
5.  **Monitoring**: Prometheus scrapes metrics from both API and Worker.

## Getting Started

### Prerequisites

- Docker and Docker Compose

### Run the platform

```bash
cd 04_infra
docker-compose up --build
```

### Usage

1.  **Submit a job**:
    ```bash
    curl -X POST http://localhost:8000/v1/jobs \
      -H "Content-Type: application/json" \
      -d '{"task": "llm", "input": {"text": "Hello world"}}'
    ```
    Response: `{"job_id": "j_...", "status": "queued"}`

2.  **Check status**:
    ```bash
    curl http://localhost:8000/v1/jobs/{job_id}
    ```

### Monitoring

- **Prometheus**: http://localhost:9090
- **API Metrics**: http://localhost:8000/metrics
- **Worker Metrics**: http://localhost:9091 (accessible within Docker network)

## Development

### Adding a new backend

1.  Implement a new class inheriting from `BaseBackend` in `02_worker/backends/`.
2.  Register the backend in `02_worker/main.py` inside `get_backend()`.
