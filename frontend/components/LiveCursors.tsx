import React from "react";
import { MousePointer2, Bot } from "lucide-react";

export interface CursorInfo {
  userId: string;
  role: "human" | "agent";
  cursor: { x: number; y: number };
  color: string;
}

interface LiveCursorsProps {
  cursors: CursorInfo[];
}

export function LiveCursors({ cursors }: LiveCursorsProps) {
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden z-20">
      {cursors.map((c) => (
        <div
          key={c.userId}
          className="absolute transition-all duration-100 ease-out flex items-center gap-1.5"
          style={{
            transform: `translate(${c.cursor.x}px, ${c.cursor.y}px)`,
          }}
        >
          {c.role === "agent" ? (
            <Bot className="w-4 h-4 text-amber-400 drop-shadow" />
          ) : (
            <MousePointer2 className="w-4 h-4 text-cyan-400 drop-shadow fill-cyan-400/20" />
          )}
          <span
            className="text-[10px] px-1.5 py-0.5 rounded font-mono font-medium shadow text-white"
            style={{ backgroundColor: c.color }}
          >
            {c.userId}
          </span>
        </div>
      ))}
    </div>
  );
}
