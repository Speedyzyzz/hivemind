# HiveMind: Collaborative Multiplayer Durable-Agent Runtime

A collaborative control-plane runtime where multiple humans and multiple agents share a live, permissioned task state—reconciling concurrent intent edits without corrupting execution authority.

## Architecture

- **`gateway/`**: Node.js / TypeScript WebSocket gateway managing collaborative rooms, presence awareness, and live CRDT synchronization.
- **`backend/app/fsm/`**: Event-sourced durable session coordinator in FastAPI + PostgreSQL/SQLite managing authoritative task states, worker execution leases, and human/agent turn ownership.
- **`backend/app/coordination/`**: Distributed lease manager with TTL heartbeats and watchdog crash eviction, plus human intervention arbitration (pause, steer, takeover).
- **`frontend/`**: Next.js 15 App Router collaborative canvas with cursor presence, live task plan graph, intervention bar, and live execution diffs.
- **`benchmark/`**: `HiveBench` simulating 50+ concurrent virtual actors, network partitions, worker crashes during active tool execution, and permission revocations during in-flight plans.

## Quick Start (Offline Verification)

```bash
# 1. Run backend unit tests (100% offline)
pytest backend/tests -v

# 2. Run HiveBench concurrency and fault-injection benchmark
python3 benchmark/hive_bench.py
```

## Running Full Stack

```bash
# Start backend API (FastAPI)
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8003

# Start WebSocket gateway
cd gateway && npm start

# Start frontend (Next.js 15)
cd frontend && npm install && npm run dev
```
