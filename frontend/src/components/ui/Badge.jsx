import React from "react";

export default function Badge({
  children,
  variant = "neutral",
  className = "",
  ...props
}) {
  const styles = {
    neutral: "bg-zinc-100 text-zinc-800 border-zinc-200",
    success: "bg-emerald-100 text-emerald-800 border-emerald-200",
    warning: "bg-amber-100 text-amber-800 border-amber-200",
    danger: "bg-rose-100 text-rose-800 border-rose-200",
    primary: "bg-zinc-900 text-white border-zinc-900",
  };

  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full border px-3 py-1 text-xs font-semibold transition-all duration-200 ${styles[variant]} ${className}`}
      {...props}
    >
      {children}
    </span>
  );
}

