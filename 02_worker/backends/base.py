from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseBackend(ABC):
    def __init__(self, model_name: str, version: str = "v1"):
        self.model_name = model_name
        self.version = version

    @abstractmethod
    def infer(self, payload: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute inference.
        """
        pass
