from pydantic import BaseModel
from typing import Optional, Any, Dict

class JobRequest(BaseModel):
    task: str  # "marketing_pipeline" | "llm" | "cv"
    model: Optional[str] = None
    version: Optional[str] = None
    language: Optional[str] = "ko"  # "ko", "en", "jp"
    platform: Optional[str] = "instagram"  # "instagram", "twitter", "blog"
    tone: Optional[str] = "friendly"  # "professional", "friendly", "emotional"
    input: Dict[str, Any]
    params: Optional[Dict[str, Any]] = None

class JobCreateResponse(BaseModel):
    job_id: str
    status: str

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    result: Optional[Any] = None
    error: Optional[str] = None