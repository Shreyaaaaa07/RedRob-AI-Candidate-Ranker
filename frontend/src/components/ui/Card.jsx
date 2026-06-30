import React from 'react'

export default function Card({ children, className = '' }) {
  return (
    <div className={`rounded-xl border border-zinc-200 bg-white shadow-sm ${className}`}>
      {children}
    </div>
  )
}

