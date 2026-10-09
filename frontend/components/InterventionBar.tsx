import React from "react";
import { Pause, Compass, UserCheck, ShieldAlert } from "lucide-react";

interface InterventionBarProps {
  currentState: string;
  onIntervene: (action: "pause" | "steer" | "takeover") => void;
  leaseId?: string | null;
}

export function InterventionBar({
  currentState,
  onIntervene,
  leaseId,
}: InterventionBarProps) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center justify-between shadow-lg">
      <div className="flex items-center gap-3">
        <span className="text-xs text-slate-400 font-medium">Authoritative FSM State:</span>
        <span className="text-xs px-2.5 py-0.5 rounded-full font-mono uppercase bg-amber-950 border border-amber-800 text-amber-400 font-bold">
          {currentState}
        </span>
        {leaseId && (
          <span className="text-[11px] text-slate-500 font-mono hidden md:inline">
            Active Lease: <strong className="text-slate-300">{leaseId}</strong>
          </span>
        )}
      </div>

      <div className="flex items-center gap-2.5">
        <button
          onClick={() => onIntervene("pause")}
          className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-colors border border-slate-700"
        >
          <Pause className="w-3.5 h-3.5 text-amber-400" />
          <span>Pause Agents</span>
        </button>

        <button
          onClick={() => onIntervene("steer")}
          className="px-3 py-1.5 bg-indigo-900/60 hover:bg-indigo-900 border border-indigo-700 text-indigo-200 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-colors"
        >
          <Compass className="w-3.5 h-3.5 text-indigo-400" />
          <span>Steer Instructions</span>
        </button>

        <button
          onClick={() => onIntervene("takeover")}
          className="px-3 py-1.5 bg-rose-900/60 hover:bg-rose-900 border border-rose-700 text-rose-200 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-colors"
        >
          <UserCheck className="w-3.5 h-3.5 text-rose-400" />
          <span>Emergency Takeover</span>
        </button>
      </div>
    </div>
  );
}
