import React from 'react'
import Card from './Card'

export default function ErrorState({ title = 'Something went wrong', message, action }) {
  return (
    <Card className="border-rose-200">
      <div className="p-6">
        <div className="text-sm font-semibold text-rose-900">{title}</div>
        {message ? <div className="mt-1 text-sm text-rose-700">{message}</div> : null}
        {action ? <div className="mt-4">{action}</div> : null}
      </div>
    </Card>
  )
}

