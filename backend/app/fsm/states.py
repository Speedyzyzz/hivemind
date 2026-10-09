from enum import Enum

class TaskExecutionState(str, Enum):
    IDLE = "idle"
    PLANNING = "planning"
    LEASED = "leased"
    EXECUTING = "executing"
    AWAITING_HUMAN = "awaiting_human"
    PAUSED = "paused"
    COMMITTED = "committed"
    FAILED = "failed"

class SessionEventType(str, Enum):
    START_PLAN = "start_plan"
    LEASE_ACQUIRED = "lease_acquired"
    EXECUTION_START = "execution_start"
    STEP_COMPLETED = "step_completed"
    HUMAN_INTERVENTION = "human_intervention"
    RESUME = "resume"
    COMMIT = "commit"
    FAIL = "fail"
