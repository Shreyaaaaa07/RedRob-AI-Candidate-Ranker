import React from 'react'

export default function Button({
  children,
  onClick,
  className = '',
  variant = 'primary',
  type = 'button',
  disabled,
}) {
  const styles = {
    primary: 'bg-zinc-900 text-white hover:bg-zinc-800',
    secondary: 'bg-white text-zinc-800 border border-zinc-200 hover:bg-zinc-50',
    danger: 'bg-rose-600 text-white hover:bg-rose-500',
  }[variant]

  return (
    <button
      type={type}
      disabled={disabled}
      onClick={onClick}
      className={`inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2 text-sm font-semibold transition disabled:cursor-not-allowed disabled:opacity-60 ${styles} ${className}`}
    >
      {children}
    </button>
  )
}

