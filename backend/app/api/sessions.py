from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.fsm.engine import DurableFSM
from app.fsm.states import TaskExecutionState
from app.coordination.lease_manager import LeaseManager

router = APIRouter(prefix="/sessions", tags=["Sessions"])

# Global in-memory registry of sessions & shared lease manager
lease_manager = LeaseManager()
active_sessions: Dict[str, DurableFSM] = {}

class CreateSessionRequest(BaseModel):
    session_id: str

class TransitionRequest(BaseModel):
    target_state: TaskExecutionState
    lease_id: Optional[str] = None

class StepRequest(BaseModel):
    result: Dict[str, Any]

@router.post("")
async def create_session(req: CreateSessionRequest):
    if req.session_id in active_sessions:
        raise HTTPException(status_code=409, detail="Session already exists.")
    fsm = DurableFSM(req.session_id, lease_manager)
    active_sessions[req.session_id] = fsm
    return {"session_id": req.session_id, "state": fsm.current_state.value}

@router.get("/{session_id}")
async def get_session(session_id: str):
    fsm = active_sessions.get(session_id)
    if not fsm:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {
        "session_id": fsm.session_id,
        "state": fsm.current_state.value,
        "step_index": fsm.step_index,
        "active_lease_id": fsm.active_lease_id,
        "context": fsm.context
    }

@router.post("/{session_id}/transition")
async def transition_session(session_id: str, req: TransitionRequest):
    fsm = active_sessions.get(session_id)
    if not fsm:
        raise HTTPException(status_code=404, detail="Session not found.")
    ok, msg = fsm.transition_to(req.target_state, req.lease_id)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    return {"session_id": session_id, "state": fsm.current_state.value, "message": msg}

@router.post("/{session_id}/step")
async def execute_step(session_id: str, req: StepRequest):
    fsm = active_sessions.get(session_id)
    if not fsm:
        raise HTTPException(status_code=404, detail="Session not found.")
    ok = fsm.step(req.result)
    if not ok:
        raise HTTPException(status_code=400, detail="Cannot step while not in EXECUTING state.")
    return {"session_id": session_id, "step_index": fsm.step_index}
