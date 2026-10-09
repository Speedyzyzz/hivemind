from typing import Any, Dict, Optional, Tuple
from app.fsm.states import TaskExecutionState
from app.fsm.transitions import can_transition
from app.fsm.checkpoint import ExecutionCheckpoint, CheckpointJournal
from app.coordination.lease_manager import LeaseManager, ExecutionLease

class DurableFSM:
    def __init__(self, session_id: str, lease_manager: Optional[LeaseManager] = None):
        self.session_id = session_id
        self.current_state = TaskExecutionState.IDLE
        self.step_index = 0
        self.context: Dict[str, Any] = {}
        self.active_lease_id: Optional[str] = None
        self.lease_manager = lease_manager or LeaseManager()
        self.journal = CheckpointJournal()

    def transition_to(self, new_state: TaskExecutionState, lease_id: Optional[str] = None) -> Tuple[bool, str]:
        # If moving to EXECUTING, lease must be valid
        if new_state == TaskExecutionState.EXECUTING:
            check_lease = lease_id or self.active_lease_id
            if not check_lease or not self.lease_manager.is_lease_valid(check_lease):
                return False, "Cannot enter EXECUTING state without a valid unexpired lease."

        if not can_transition(self.current_state, new_state):
            return False, f"Illegal transition from {self.current_state.value} to {new_state.value}"

        self.current_state = new_state
        if lease_id:
            self.active_lease_id = lease_id

        # Save checkpoint
        self.save_checkpoint()
        return True, f"Transitioned to {new_state.value}"

    def step(self, result: Dict[str, Any]) -> bool:
        if self.current_state != TaskExecutionState.EXECUTING:
            return False
        self.step_index += 1
        self.context[f"step_{self.step_index}"] = result
        self.save_checkpoint()
        return True

    def save_checkpoint(self) -> ExecutionCheckpoint:
        cp = ExecutionCheckpoint(
            checkpoint_id=f"cp_{self.session_id}_{self.step_index}",
            session_id=self.session_id,
            step_index=self.step_index,
            state=self.current_state,
            context_variables=dict(self.context),
            active_lease_id=self.active_lease_id
        )
        self.journal.save_checkpoint(cp)
        return cp

    def restore_from_last_checkpoint(self) -> bool:
        cp = self.journal.get_latest_checkpoint(self.session_id)
        if not cp:
            return False
        self.step_index = cp.step_index
        self.current_state = cp.state
        self.context = dict(cp.context_variables)
        self.active_lease_id = cp.active_lease_id
        return True

    def human_intervene(self, action: str, new_instructions: Optional[str] = None) -> bool:
        """Human pause, steer, or takeover"""
        if action == "pause":
            self.current_state = TaskExecutionState.PAUSED
            if self.active_lease_id:
                self.lease_manager.revoke_lease(self.active_lease_id)
                self.active_lease_id = None
        elif action == "steer":
            if new_instructions:
                self.context["human_steering"] = new_instructions
            self.current_state = TaskExecutionState.PLANNING
        elif action == "takeover":
            self.current_state = TaskExecutionState.AWAITING_HUMAN
            if self.active_lease_id:
                self.lease_manager.revoke_lease(self.active_lease_id)
                self.active_lease_id = None
        self.save_checkpoint()
        return True
