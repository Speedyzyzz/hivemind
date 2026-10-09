from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.api.sessions import active_sessions

router = APIRouter(prefix="/interventions", tags=["Interventions"])

class InterventionRequest(BaseModel):
    action: str  # "pause", "steer", "takeover"
    new_instructions: Optional[str] = None

@router.post("/{session_id}")
async def apply_intervention(session_id: str, req: InterventionRequest):
    fsm = active_sessions.get(session_id)
    if not fsm:
        raise HTTPException(status_code=404, detail="Session not found.")
    ok = fsm.human_intervene(req.action, req.new_instructions)
    return {"session_id": session_id, "state": fsm.current_state.value, "applied": ok}
