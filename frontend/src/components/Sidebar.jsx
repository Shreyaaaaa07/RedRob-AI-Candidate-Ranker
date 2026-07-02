import React from 'react'
import { NavLink } from 'react-router-dom'

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function Sidebar({ activePath }) {
  
  
  const nav = [
    { to: "/dashboard", label: "Dashboard", icon: "📊" },
    { to: "/job-description", label: "Job Description", icon: "🧾" },
    { to: "/candidate-rankings", label: "Candidate Rankings", icon: "🏅" },
    { to: "/compare", label: "Compare Candidates", icon: "⚖️" },
    { to: "/analytics", label: "Analytics", icon: "📈" },
  ];

  return (
    <aside className="hidden w-64 shrink-0 border-r bg-white lg:block">
      <div className="flex h-full flex-col">
        <div className="p-5">
          <div className="text-lg font-semibold text-zinc-900">Redrob AI Ranker</div>
          <div className="mt-1 text-sm text-zinc-500">Recruiter dashboard</div>
        </div>

        <nav className="flex-1 px-3 pb-6">
          <div className="space-y-1">
            {nav.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  classNames(
                    'group flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition',
                    isActive
                      ? 'bg-zinc-900 text-white'
                      : 'text-zinc-700 hover:bg-zinc-100 hover:text-zinc-900'
                  )
                }
                end
              >
                <span className="text-base">{item.icon}</span>
                <span>{item.label}</span>
              </NavLink>
            ))}
          </div>
        </nav>

        <div className="border-t px-4 py-4">
          <div className="text-xs text-zinc-500">Environment</div>
          <div className="mt-1 rounded-md bg-zinc-50 px-2 py-1 text-xs font-medium text-zinc-700">
            {import.meta.env.VITE_API_BASE_URL ? 'API configured' : 'Set VITE_API_BASE_URL'}
          </div>
          <div className="mt-2 text-xs text-zinc-500">Use recruiter workflows to upload JD, review ranked candidates, and inspect evidence.</div>
        </div>
      </div>
    </aside>
  )
}

