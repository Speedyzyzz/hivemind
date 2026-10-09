from typing import Dict, List, Set
from app.fsm.states import TaskExecutionState, SessionEventType

ALLOWED_TRANSITIONS: Dict[TaskExecutionState, Set[TaskExecutionState]] = {
    TaskExecutionState.IDLE: {TaskExecutionState.PLANNING, TaskExecutionState.FAILED},
    TaskExecutionState.PLANNING: {TaskExecutionState.LEASED, TaskExecutionState.AWAITING_HUMAN, TaskExecutionState.FAILED},
    TaskExecutionState.LEASED: {TaskExecutionState.EXECUTING, TaskExecutionState.PAUSED, TaskExecutionState.FAILED},
    TaskExecutionState.EXECUTING: {TaskExecutionState.EXECUTING, TaskExecutionState.AWAITING_HUMAN, TaskExecutionState.COMMITTED, TaskExecutionState.PAUSED, TaskExecutionState.FAILED},
    TaskExecutionState.AWAITING_HUMAN: {TaskExecutionState.LEASED, TaskExecutionState.EXECUTING, TaskExecutionState.COMMITTED, TaskExecutionState.FAILED},
    TaskExecutionState.PAUSED: {TaskExecutionState.LEASED, TaskExecutionState.EXECUTING, TaskExecutionState.FAILED},
    TaskExecutionState.COMMITTED: set(),
    TaskExecutionState.FAILED: {TaskExecutionState.IDLE, TaskExecutionState.PLANNING} # Recovery allowed
}

def can_transition(current: TaskExecutionState, target: TaskExecutionState) -> bool:
    return target in ALLOWED_TRANSITIONS.get(current, set())
