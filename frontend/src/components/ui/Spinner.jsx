import React from 'react'

export default function Spinner({ label = 'Loading…' }) {
  return (
    <div className="flex items-center gap-3 text-sm text-zinc-600">
      <span className="inline-block h-4 w-4 animate-spin rounded-full border-2 border-zinc-300 border-t-zinc-900" />
      <span>{label}</span>
    </div>
  )
}

