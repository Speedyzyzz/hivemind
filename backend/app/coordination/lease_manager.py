import time
import secrets
from typing import Dict, Optional
from pydantic import BaseModel, Field

class ExecutionLease(BaseModel):
    lease_id: str
    session_id: str
    holder_id: str
    resource_scope: str
    expires_at_epoch: float
    is_revoked: bool = False

class LeaseManager:
    def __init__(self, default_ttl_seconds: int = 15):
        self.default_ttl = default_ttl_seconds
        self.leases: Dict[str, ExecutionLease] = {}

    def acquire_lease(self, session_id: str, holder_id: str, scope: str = "*", ttl_seconds: Optional[int] = None) -> Optional[ExecutionLease]:
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        now = time.time()

        # Check existing active lease for this session
        for lease in self.leases.values():
            if lease.session_id == session_id and not lease.is_revoked and lease.expires_at_epoch > now:
                if lease.holder_id != holder_id:
                    return None # Resource locked by another holder!

        lease_id = f"lease_{secrets.token_hex(8)}"
        lease = ExecutionLease(
            lease_id=lease_id,
            session_id=session_id,
            holder_id=holder_id,
            resource_scope=scope,
            expires_at_epoch=now + ttl,
            is_revoked=False
        )
        self.leases[lease_id] = lease
        return lease

    def heartbeat(self, lease_id: str, additional_ttl_seconds: Optional[int] = None) -> bool:
        lease = self.leases.get(lease_id)
        if not lease or lease.is_revoked:
            return False
        now = time.time()
        if now > lease.expires_at_epoch:
            return False # Already expired

        ttl = additional_ttl_seconds if additional_ttl_seconds is not None else self.default_ttl
        lease.expires_at_epoch = now + ttl
        return True

    def revoke_lease(self, lease_id: str) -> bool:
        lease = self.leases.get(lease_id)
        if lease:
            lease.is_revoked = True
            return True
        return False

    def is_lease_valid(self, lease_id: str) -> bool:
        lease = self.leases.get(lease_id)
        if not lease or lease.is_revoked:
            return False
        return time.time() <= lease.expires_at_epoch
