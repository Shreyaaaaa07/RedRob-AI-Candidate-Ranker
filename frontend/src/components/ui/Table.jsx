import React from 'react'

export default function Table({ children, className = '' }) {
  return (
    <div className={`overflow-x-auto rounded-xl border border-zinc-200 bg-white ${className}`}>
      <table className="min-w-full table-auto">{children}</table>
    </div>
  )
}

