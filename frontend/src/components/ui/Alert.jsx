import React from 'react'

export default function Alert({ variant = 'info', title, children }) {
  const styles = {
    info: 'border-zinc-200 bg-white text-zinc-800',
    success: 'border-emerald-200 bg-emerald-50 text-emerald-800',
    warning: 'border-amber-200 bg-amber-50 text-amber-800',
    danger: 'border-rose-200 bg-rose-50 text-rose-800',
  }[variant]

  return (
    <div className={`rounded-xl border p-4 text-sm ${styles}`}>
      {title ? <div className="font-semibold">{title}</div> : null}
      {children ? <div className={title ? 'mt-1' : ''}>{children}</div> : null}
    </div>
  )
}

