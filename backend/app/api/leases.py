from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.api.sessions import lease_manager

router = APIRouter(prefix="/leases", tags=["Leases"])

class AcquireLeaseRequest(BaseModel):
    session_id: str
    holder_id: str
    scope: str = "*"
    ttl_seconds: Optional[int] = None

@router.post("/acquire")
async def acquire_lease(req: AcquireLeaseRequest):
    lease = lease_manager.acquire_lease(req.session_id, req.holder_id, req.scope, req.ttl_seconds)
    if not lease:
        raise HTTPException(status_code=423, detail="Resource locked by another worker lease.")
    return lease.model_dump()

@router.post("/{lease_id}/heartbeat")
async def heartbeat_lease(lease_id: str):
    ok = lease_manager.heartbeat(lease_id)
    if not ok:
        raise HTTPException(status_code=410, detail="Lease expired or revoked.")
    return {"status": "renewed"}

@router.post("/{lease_id}/revoke")
async def revoke_lease(lease_id: str):
    ok = lease_manager.revoke_lease(lease_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Lease not found.")
    return {"status": "revoked"}
