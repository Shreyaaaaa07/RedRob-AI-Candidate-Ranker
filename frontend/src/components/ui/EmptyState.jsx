import React from 'react'

export default function EmptyState({ title, description, action }) {
  return (
    <div className="rounded-xl border border-dashed border-zinc-300 bg-zinc-50 p-6 text-center">
      <div className="text-sm font-semibold text-zinc-900">{title}</div>
      {description ? <div className="mt-1 text-sm text-zinc-600">{description}</div> : null}
      {action ? <div className="mt-4">{action}</div> : null}
    </div>
  )
}

