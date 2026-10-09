"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { ArrowLeft, Users, Bot } from "lucide-react";
import { InterventionBar } from "@/components/InterventionBar";
import { LiveCursors, CursorInfo } from "@/components/LiveCursors";
import { ExecutionDiff } from "@/components/ExecutionDiff";

export default function CollaborativeCanvasPage() {
  const params = useParams();
  const roomId = (params?.roomId as string) || "room_alpha_squad";

  const [state, setState] = useState("executing");
  const [stepIndex, setStepIndex] = useState(3);
  const [leaseId, setLeaseId] = useState<string | null>("lease_9f1a02");

  const [cursors] = useState<CursorInfo[]>([
    {
      userId: "Architect (Human)",
      role: "human",
      cursor: { x: 320, y: 180 },
      color: "#06b6d4",
    },
    {
      userId: "Worker-Agent-1",
      role: "agent",
      cursor: { x: 620, y: 260 },
      color: "#f59e0b",
    },
  ]);

  const handleIntervene = (action: "pause" | "steer" | "takeover") => {
    if (action === "pause") {
      setState("paused");
      setLeaseId(null);
    } else if (action === "steer") {
      setState("planning");
    } else if (action === "takeover") {
      setState("awaiting_human");
      setLeaseId(null);
    }
  };

  return (
    <div className="space-y-6 relative min-h-[700px]">
      <LiveCursors cursors={cursors} />

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link
            href="/"
            className="p-2 bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-lg text-slate-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
          </Link>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-white font-mono">{roomId}</h1>
            <p className="text-xs text-slate-400 mt-0.5">Multiplayer Shared Task Canvas & Intervention Control</p>
          </div>
        </div>

        <div className="flex items-center gap-3 text-xs font-mono">
          <span className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-cyan-950/60 border border-cyan-800 text-cyan-300">
            <Users className="w-3.5 h-3.5" />
            <span>2 Humans Connected</span>
          </span>
          <span className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-amber-950/60 border border-amber-800 text-amber-300">
            <Bot className="w-3.5 h-3.5" />
            <span>3 Agents Sandboxed</span>
          </span>
        </div>
      </div>

      <InterventionBar
        currentState={state}
        onIntervene={handleIntervene}
        leaseId={leaseId}
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6 min-h-[400px] flex flex-col justify-between">
          <div className="space-y-3">
            <span className="text-xs text-slate-500 font-mono">Collaborative Intent Node Graph (CRDT Synchronized)</span>
            <div className="p-4 rounded-lg bg-slate-950 border border-slate-800 text-xs font-mono space-y-2">
              <div className="text-amber-400 font-bold">Goal: Refactor Auth Middleware to OAuth 2.1</div>
              <ul className="space-y-1.5 text-slate-300 list-disc list-inside">
                <li>Extract token validator into micro-module (Status: COMPLETED)</li>
                <li>Add PKCE challenge verification (Status: IN_PROGRESS — Leased to Worker-Agent-1)</li>
                <li>Update contract test suite (Status: PENDING)</li>
              </ul>
            </div>
          </div>
          <div className="text-[11px] text-slate-500 font-mono italic">
            * Intent state is synchronized via Yjs CRDTs; tool execution is strictly gated by the authoritative FSM lease manager.
          </div>
        </div>

        <div>
          <ExecutionDiff
            stepIndex={stepIndex}
            context={{
              "step_1": { action: "parse_tokens", status: "success" },
              "step_2": { action: "generate_pkce_verifier", status: "success" },
              "step_3": { action: "apply_patch", file: "auth/validator.py", status: "executing" },
            }}
          />
        </div>
      </div>
    </div>
  );
}
