from typing import Any, Dict, List
from app.llm.provider import LLMProvider, LLMResponse

class OfflineMultiplayerLLM(LLMProvider):
    def __init__(self):
        self.model = "hivemind-multiplayer-offline"

    async def generate(self, messages: List[Dict[str, Any]], agent_id: str = "agent_primary", **kwargs: Any) -> LLMResponse:
        return LLMResponse(
            content=f"Collaborative proposal from {agent_id}",
            agent_id=agent_id,
            model=self.model
        )
