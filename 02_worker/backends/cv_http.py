import time, random
from typing import Any, Dict
from .base import BaseBackend

class CVHTTPBackend(BaseBackend):
    def infer(self, payload: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        # Simulated external API call (e.g., TorchServe or Triton)
        time.sleep(random.uniform(0.2, 0.5))
        
        image_id = payload.get("image_id", "unknown")
        # In a real scenario, this would call a CV model endpoint
        return {
            "model": self.model_name,
            "version": self.version,
            "detections": [
                {"class": "cat", "score": 0.98, "bbox": [10, 20, 100, 120]},
                {"class": "dog", "score": 0.02, "bbox": [50, 60, 200, 250]}
            ],
            "image_id": image_id
        }
