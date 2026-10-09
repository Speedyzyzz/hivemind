from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class LLMResponse(BaseModel):
    content: Optional[str] = None
    agent_id: str = "agent_primary"
    model: str = "offline"

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, messages: List[Dict[str, Any]], agent_id: str = "agent_primary", **kwargs: Any) -> LLMResponse:
        pass
