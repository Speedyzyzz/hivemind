from app.fsm.engine import DurableFSM
from app.fsm.states import TaskExecutionState
from app.coordination.lease_manager import LeaseManager

def test_fsm_transition_lifecycle():
    lease_mgr = LeaseManager()
    fsm = DurableFSM("sess_fsm_01", lease_mgr)
    assert fsm.current_state == TaskExecutionState.IDLE

    # 1. Idle -> Planning
    ok, msg = fsm.transition_to(TaskExecutionState.PLANNING)
    assert ok is True
    assert fsm.current_state == TaskExecutionState.PLANNING

    # 2. Acquire Lease
    lease = lease_mgr.acquire_lease("sess_fsm_01", "worker_alpha")
    assert lease is not None

    # 3. Planning -> Leased
    ok, _ = fsm.transition_to(TaskExecutionState.LEASED, lease.lease_id)
    assert ok is True

    # 4. Leased -> Executing
    ok, _ = fsm.transition_to(TaskExecutionState.EXECUTING)
    assert ok is True

    # 5. Step in Executing
    assert fsm.step({"file_created": "index.ts"}) is True
    assert fsm.step_index == 1

    # 6. Executing -> Committed
    ok, _ = fsm.transition_to(TaskExecutionState.COMMITTED)
    assert ok is True

def test_fsm_blocks_execution_without_lease():
    lease_mgr = LeaseManager()
    fsm = DurableFSM("sess_fsm_02", lease_mgr)
    fsm.transition_to(TaskExecutionState.PLANNING)
    
    # Try transitioning directly to EXECUTING without a lease
    ok, msg = fsm.transition_to(TaskExecutionState.EXECUTING)
    assert ok is False
    assert "without a valid unexpired lease" in msg
