import React from 'react'
import { useLocation, Link } from 'react-router-dom'

export default function Topbar() {
  const { pathname } = useLocation()

  const pageLabel = (() => {
    if (pathname.startsWith('/dashboard')) return 'Dashboard'
    if (pathname.startsWith('/job-description')) return 'Job Description'
    if (pathname.startsWith('/candidate-rankings')) return 'Candidate Rankings'
    if (pathname.startsWith('/candidate/')) return 'Candidate Details'
    if (pathname.startsWith('/explainability')) return 'Explainability'
    if (pathname.startsWith('/analytics')) return 'Analytics'
    return 'Recruiter Dashboard'
  })()

  return (
    <header className="flex items-center justify-between gap-4 border-b bg-white px-2 py-3 sm:px-4">
      <div className="min-w-0">
        <div className="truncate text-sm font-semibold text-zinc-900">{pageLabel}</div>
        <div className="truncate text-xs text-zinc-500">Evidence-backed AI ranking for recruiters</div>
      </div>

      <div className="flex items-center gap-2">
        <Link
          to="/dashboard"
          className="hidden rounded-md border border-zinc-200 bg-white px-3 py-2 text-sm font-medium text-zinc-700 hover:bg-zinc-50 sm:block"
        >
          Home
        </Link>
        <div className="rounded-full bg-zinc-900 px-3 py-1 text-xs font-semibold text-white">Recruiter</div>
      </div>
    </header>
  )
}

