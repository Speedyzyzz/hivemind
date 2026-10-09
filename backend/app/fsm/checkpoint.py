import time
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from app.fsm.states import TaskExecutionState

class ExecutionCheckpoint(BaseModel):
    checkpoint_id: str
    session_id: str
    step_index: int
    state: TaskExecutionState
    context_variables: Dict[str, Any] = Field(default_factory=dict)
    active_lease_id: Optional[str] = None
    created_at_epoch: float = Field(default_factory=time.time)

class CheckpointJournal:
    def __init__(self):
        self._checkpoints: Dict[str, list[ExecutionCheckpoint]] = {}

    def save_checkpoint(self, checkpoint: ExecutionCheckpoint) -> None:
        if checkpoint.session_id not in self._checkpoints:
            self._checkpoints[checkpoint.session_id] = []
        self._checkpoints[checkpoint.session_id].append(checkpoint)

    def get_latest_checkpoint(self, session_id: str) -> Optional[ExecutionCheckpoint]:
        cps = self._checkpoints.get(session_id, [])
        if cps:
            return cps[-1]
        return None
