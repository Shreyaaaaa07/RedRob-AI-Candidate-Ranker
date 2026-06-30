import React from 'react'

export default function Input({ value, onChange, placeholder, className = '' }) {
  return (
    <input
      className={`w-full rounded-lg border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-900 placeholder:text-zinc-400 focus:border-zinc-300 focus:outline-none ${className}`}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
    />
  )
}

