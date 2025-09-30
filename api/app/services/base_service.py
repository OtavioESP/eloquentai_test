from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseService(ABC):
    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> bool:
        pass
    
    @abstractmethod
    def process_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass
