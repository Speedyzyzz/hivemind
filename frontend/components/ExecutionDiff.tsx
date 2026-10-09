import React from "react";
import { Activity, Clock } from "lucide-react";

interface ExecutionDiffProps {
  stepIndex: number;
  context: Record<string, any>;
}

export function ExecutionDiff({ stepIndex, context }: ExecutionDiffProps) {
  const steps = Object.entries(context);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-amber-400" />
          <span className="font-semibold text-slate-200 text-sm">Live Resumable Execution Stream</span>
        </div>
        <span className="text-xs text-slate-400 font-mono">Step {stepIndex}</span>
      </div>

      <div className="space-y-3 max-h-80 overflow-y-auto pr-1">
        {steps.length === 0 ? (
          <div className="text-xs text-slate-500 py-6 text-center italic">
            Waiting for worker lease activation...
          </div>
        ) : (
          steps.map(([k, val]) => (
            <div
              key={k}
              className="p-3 bg-slate-950 border border-slate-800 rounded-lg text-xs font-mono space-y-1"
            >
              <div className="flex items-center justify-between text-slate-400">
                <span className="text-amber-400 font-bold">{k}</span>
                <span className="text-[10px] text-slate-600 flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  <span>checkpoint verified</span>
                </span>
              </div>
              <pre className="text-slate-300 text-[11px] overflow-x-auto">
                {JSON.stringify(val, null, 2)}
              </pre>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
