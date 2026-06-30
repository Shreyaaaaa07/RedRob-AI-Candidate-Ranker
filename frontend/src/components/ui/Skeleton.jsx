import React from 'react'

export default function Skeleton({ className = '' }) {
  return <div className={`animate-pulse rounded bg-zinc-200 ${className}`} />
}

