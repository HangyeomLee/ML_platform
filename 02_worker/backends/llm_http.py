import time, random
from typing import Any, Dict
from .base import BaseBackend

class LLMHTTPBackend(BaseBackend):
    def infer(self, payload: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        # Simulated external API call
        time.sleep(random.uniform(0.1, 0.3))
        
        text = payload.get("text", "")
        # In a real scenario, this would use httpx or requests to call an OpenAI-compatible API
        return {
            "model": self.model_name,
            "version": self.version,
            "response": f"Processed by {self.model_name}: {text[::-1]}",  # Just reverse text for dummy
            "usage": {"tokens": len(text)}
        }
