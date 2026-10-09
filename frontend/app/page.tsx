import React from "react";
import Link from "next/link";
import { Users, Bot, Layers, ArrowRight } from "lucide-react";

export default function HiveMindDashboard() {
  const rooms = [
    {
      id: "room_alpha_squad",
      title: "Full-Stack Refactor & API Migration Squad",
      humans_online: 2,
      agents_active: 3,
      current_stage: "executing",
      leases_granted: 1,
    },
    {
      id: "room_qa_stress",
      title: "HiveBench Concurrency Stress Room",
      humans_online: 1,
      agents_active: 4,
      current_stage: "leased",
      leases_granted: 1,
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">Multiplayer Agent Workspaces</h1>
          <p className="text-sm text-slate-400 mt-1">
            Real-time human-agent collaboration backed by distributed leases and event-sourced FSM.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {rooms.map((r) => (
          <div
            key={r.id}
            className="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-xl p-5 space-y-4 transition-all"
          >
            <div className="flex items-center justify-between">
              <span className="font-mono text-sm font-bold text-slate-100">{r.id}</span>
              <span className="text-xs px-2.5 py-0.5 rounded-full font-mono uppercase bg-amber-950 border border-amber-800 text-amber-400 font-bold">
                {r.current_stage}
              </span>
            </div>

            <h3 className="font-semibold text-slate-200 text-sm">{r.title}</h3>

            <div className="flex items-center gap-5 text-xs text-slate-400 font-mono">
              <span className="flex items-center gap-1.5 text-cyan-400">
                <Users className="w-3.5 h-3.5" />
                <span>{r.humans_online} Humans</span>
              </span>
              <span className="flex items-center gap-1.5 text-amber-400">
                <Bot className="w-3.5 h-3.5" />
                <span>{r.agents_active} Agents</span>
              </span>
              <span className="flex items-center gap-1.5 text-emerald-400">
                <Layers className="w-3.5 h-3.5" />
                <span>{r.leases_granted} Lease Active</span>
              </span>
            </div>

            <div className="pt-2">
              <Link
                href={`/canvas/${r.id}`}
                className="w-full py-2 bg-amber-600 hover:bg-amber-500 text-white rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors shadow-sm"
              >
                <span>Enter Collaborative Canvas</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
