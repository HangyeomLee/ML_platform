from fastapi import FastAPI
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from router import router as jobs_router
from common.config import settings

app = FastAPI(title=settings.API_TITLE, version=settings.API_VERSION)

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

app.include_router(jobs_router)
