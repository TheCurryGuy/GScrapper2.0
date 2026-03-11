import asyncio
import logging
from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.response import Publication


class BaseAcademicService(ABC):
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.source_name = self.__class__.__name__.replace('Service', '')
    
    @abstractmethod
    async def search_by_name(self, name: str, email: Optional[str] = None) -> List[Publication]:
        pass
    
    @abstractmethod
    async def search_by_orcid(self, orcid_id: str) -> List[Publication]:
        pass
    
    async def health_check(self) -> bool:
        try:
            return True
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False
    
    def _handle_error(self, error: Exception, context: str = ""):
        self.logger.error(f"Error in {context}: {str(error)}", exc_info=True)
        return []
