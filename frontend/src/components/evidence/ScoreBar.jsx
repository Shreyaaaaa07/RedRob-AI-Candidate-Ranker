import React from 'react'

export default function ScoreBar({ label, value, min = 0, max = 100 }) {
  const pct = Math.max(0, Math.min(100, ((value - min) / (max - min)) * 100 || 0))

  return (
    <div>
      <div className="flex items-center justify-between text-sm">
        <div className="font-medium text-zinc-700">{label}</div>
        <div className="font-semibold text-zinc-900">{value}</div>
      </div>
      <div className="mt-2 h-2 w-full rounded-full bg-zinc-100">
        <div
          className="h-2 rounded-full bg-zinc-900"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}

