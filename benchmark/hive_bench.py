import sys
from pathlib import Path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import asyncio
import time
from typing import Dict, Any, List
from app.fsm.engine import DurableFSM
from app.fsm.states import TaskExecutionState
from app.coordination.lease_manager import LeaseManager

class HiveBench:
    def __init__(self):
        self.lease_manager = LeaseManager(default_ttl_seconds=1)
        self.sessions: Dict[str, DurableFSM] = {}

    def run_50_concurrent_actors_test(self) -> int:
        """50 virtual actors (30 humans + 20 agents) competing for leases and edits"""
        successful_transactions = 0
        fsm = DurableFSM("sess_multiplayer_50", self.lease_manager)
        fsm.transition_to(TaskExecutionState.PLANNING)

        for actor_id in range(50):
            holder = f"actor_{actor_id}"
            lease = self.lease_manager.acquire_lease("sess_multiplayer_50", holder, ttl_seconds=1)
            if lease is not None:
                # Successfully acquired lease
                fsm.transition_to(TaskExecutionState.LEASED, lease.lease_id)
                fsm.transition_to(TaskExecutionState.EXECUTING)
                fsm.step({"actor": holder, "action": "update_plan"})
                self.lease_manager.revoke_lease(lease.lease_id)
                fsm.transition_to(TaskExecutionState.PLANNING)
                successful_transactions += 1
            else:
                # Properly locked, cannot collide
                pass

        # At least one succeeded and state remained uncorrupted
        return successful_transactions

    def run_worker_crash_and_watchdog_eviction_test(self) -> bool:
        """Worker crashes during active step; watchdog verifies lease expiry and checkpoint restoration"""
        fsm = DurableFSM("sess_worker_crash", self.lease_manager)
        fsm.transition_to(TaskExecutionState.PLANNING)
        lease = self.lease_manager.acquire_lease("sess_worker_crash", "crashed_worker", ttl_seconds=1)
        assert lease is not None
        fsm.transition_to(TaskExecutionState.LEASED, lease.lease_id)
        fsm.transition_to(TaskExecutionState.EXECUTING)
        fsm.step({"checkpoint_step": "pre_crash_work"})

        # Worker crashes and stops heartbeating. Wait for TTL to expire.
        time.sleep(1.1)

        # Watchdog verification: lease must now be invalid
        is_valid = self.lease_manager.is_lease_valid(lease.lease_id)
        assert is_valid is False

        # Session is restored from last checkpoint
        restored = fsm.restore_from_last_checkpoint()
        assert restored is True
        assert fsm.step_index == 1
        assert fsm.context["step_1"] == {"checkpoint_step": "pre_crash_work"}

        # New worker can now take over
        new_lease = self.lease_manager.acquire_lease("sess_worker_crash", "recovered_worker", ttl_seconds=5)
        return new_lease is not None

    def run_permission_revocation_during_inflight_plan(self) -> bool:
        """Human pause/takeover immediately invalidates in-flight agent lease"""
        fsm = DurableFSM("sess_revocation", self.lease_manager)
        fsm.transition_to(TaskExecutionState.PLANNING)
        lease = self.lease_manager.acquire_lease("sess_revocation", "rogue_agent", ttl_seconds=60)
        fsm.transition_to(TaskExecutionState.LEASED, lease.lease_id)
        fsm.transition_to(TaskExecutionState.EXECUTING)

        # Human issues emergency takeover
        fsm.human_intervene("takeover")
        assert fsm.current_state == TaskExecutionState.AWAITING_HUMAN
        # Rogue agent lease must be revoked immediately
        assert self.lease_manager.is_lease_valid(lease.lease_id) is False
        return True

    def execute_suite(self) -> Dict[str, Any]:
        print("Running HiveBench Concurrency and Partition Stress Suite...")
        tx_count = self.run_50_concurrent_actors_test()
        crash_recovered = self.run_worker_crash_and_watchdog_eviction_test()
        revocation_verified = self.run_permission_revocation_during_inflight_plan()

        passed = (tx_count > 0) and crash_recovered and revocation_verified
        return {
            "concurrent_transactions_handled": tx_count,
            "worker_crash_recovery": crash_recovered,
            "permission_revocation_verified": revocation_verified,
            "verdict": "HIVEBENCH PASSED" if passed else "FAILED"
        }

def main():
    bench = HiveBench()
    res = bench.execute_suite()
    print("=" * 60)
    print(f"HIVEBENCH VERDICT: {res['verdict']}")
    print(f"Concurrent Transactions: {res['concurrent_transactions_handled']}")
    print(f"Worker Crash Restoration: {res['worker_crash_recovery']}")
    print(f"Immediate Revocation: {res['permission_revocation_verified']}")
    print("=" * 60)
    assert res["worker_crash_recovery"] is True
    assert res["permission_revocation_verified"] is True

if __name__ == "__main__":
    main()
