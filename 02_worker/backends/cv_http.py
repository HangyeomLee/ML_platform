import time, random
from typing import Any, Dict
from .base import BaseBackend

class CVHTTPBackend(BaseBackend):
    def infer(self, payload: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        # Simulated external API call (e.g., TorchServe or Triton)
        time.sleep(random.uniform(0.2, 0.5))
        
        image_id = payload.get("image_id", "unknown")
        # In a real scenario, this would call a CV model endpoint
        # For simulation, we'll return some hotel-related objects if no specific image_id is given
        detections = [
            {"class": "hotel_room", "score": 0.95, "bbox": [0, 0, 1000, 1000]},
            {"class": "bed", "score": 0.88, "bbox": [100, 200, 500, 600]},
            {"class": "window", "score": 0.75, "bbox": [600, 100, 900, 400]}
        ]
        
        return {
            "model": self.model_name,
            "version": self.version,
            "detections": detections,
            "image_id": image_id
        }
