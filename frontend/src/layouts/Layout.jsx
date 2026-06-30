import React from 'react'
import { Outlet, useLocation } from 'react-router-dom'
import Sidebar from '../components/Sidebar'
import Topbar from '../components/Topbar'

export default function Layout() {
  const { pathname } = useLocation()

  return (
    <div className="min-h-screen bg-zinc-50">
      <div className="flex">
        <Sidebar activePath={pathname} />
        <div className="flex min-w-0 flex-1 flex-col">
          <Topbar />
          <main className="flex-1 p-4 sm:p-6 lg:p-8">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  )
}

