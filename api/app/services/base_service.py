from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseService(ABC):
    """Base service class for all services."""
    
    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate input data."""
        pass
    
    @abstractmethod
    def process_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the request and return response."""
        pass
