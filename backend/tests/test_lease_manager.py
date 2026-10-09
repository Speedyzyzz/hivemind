import time
from app.coordination.lease_manager import LeaseManager

def test_lease_acquisition_and_locking():
    mgr = LeaseManager(default_ttl_seconds=2)
    l1 = mgr.acquire_lease("sess_lock", "worker_1")
    assert l1 is not None

    # Worker 2 attempts to acquire lease for the same session while l1 is active
    l2 = mgr.acquire_lease("sess_lock", "worker_2")
    assert l2 is None  # Blocked!

    # Heartbeat works
    assert mgr.heartbeat(l1.lease_id, additional_ttl_seconds=5) is True

    # Revoke lease
    mgr.revoke_lease(l1.lease_id)
    assert mgr.is_lease_valid(l1.lease_id) is False

    # Now Worker 2 can acquire lease
    l2_retry = mgr.acquire_lease("sess_lock", "worker_2")
    assert l2_retry is not None
