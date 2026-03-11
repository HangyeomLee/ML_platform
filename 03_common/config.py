import os

class Settings:
    # Redis configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    QUEUE_KEY: str = os.getenv("QUEUE_KEY", "queue:inference")
    
    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Job settings
    JOB_TIMEOUT_MS: int = int(os.getenv("JOB_TIMEOUT_MS", "30000"))  # 30 seconds default
    
    # API configuration
    API_TITLE: str = "ML Inference Platform"
    API_VERSION: str = "0.1.0"

settings = Settings()
