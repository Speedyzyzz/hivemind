from app.fsm.engine import DurableFSM
from app.fsm.states import TaskExecutionState
from app.coordination.lease_manager import LeaseManager

def test_checkpoint_recovery_after_simulated_crash():
    lease_mgr = LeaseManager()
    fsm = DurableFSM("sess_crash_recovery", lease_mgr)
    fsm.transition_to(TaskExecutionState.PLANNING)
    l1 = lease_mgr.acquire_lease("sess_crash_recovery", "worker_node_1")
    fsm.transition_to(TaskExecutionState.LEASED, l1.lease_id)
    fsm.transition_to(TaskExecutionState.EXECUTING)
    fsm.step({"op": "init_repo"})
    fsm.step({"op": "install_deps"})
    assert fsm.step_index == 2

    # Simulate worker crash: create fresh FSM instance and restore from journal
    crashed_fsm = DurableFSM("sess_crash_recovery", lease_mgr)
    crashed_fsm.journal = fsm.journal # Shared journal
    assert crashed_fsm.step_index == 0

    restored = crashed_fsm.restore_from_last_checkpoint()
    assert restored is True
    assert crashed_fsm.step_index == 2
    assert crashed_fsm.current_state == TaskExecutionState.EXECUTING
    assert crashed_fsm.context["step_2"] == {"op": "install_deps"}

def test_human_pause_and_takeover():
    lease_mgr = LeaseManager()
    fsm = DurableFSM("sess_intervene", lease_mgr)
    fsm.transition_to(TaskExecutionState.PLANNING)
    lease = lease_mgr.acquire_lease("sess_intervene", "agent_auto")
    fsm.transition_to(TaskExecutionState.LEASED, lease.lease_id)
    fsm.transition_to(TaskExecutionState.EXECUTING)

    # Human pauses execution
    fsm.human_intervene("pause")
    assert fsm.current_state == TaskExecutionState.PAUSED
    assert lease_mgr.is_lease_valid(lease.lease_id) is False  # Lease revoked!

    # Human steers with new instructions
    fsm.human_intervene("steer", new_instructions="Do not touch production database")
    assert fsm.current_state == TaskExecutionState.PLANNING
    assert fsm.context["human_steering"] == "Do not touch production database"
