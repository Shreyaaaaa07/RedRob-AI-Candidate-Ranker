import React, { useMemo, useState } from 'react'
import Card from '../components/ui/Card'
import Input from '../components/ui/Input'
import Button from '../components/ui/Button'
import Spinner from '../components/ui/Spinner'
import EmptyState from '../components/ui/EmptyState'
import useJobDescription from '../hooks/useJobDescription'
import { uploadJobDescription } from '../services/jobDescriptionService'

export default function JobDescriptionPage() {
  const [text, setText] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const { error } = useJobDescription()

  const [parsed, setParsed] = useState(null)

  async function onSubmit(e) {
  e.preventDefault()
  setSubmitting(true)

  try {
    const response = await uploadJobDescription({ text })

    setParsed(response.parsed_signals)
  } finally {
    setSubmitting(false)
  }
}

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-zinc-900">Job Description</h1>
        <p className="mt-1 text-sm text-zinc-600">Upload/paste a JD. The system will parse recruiter-critical signals.</p>
      </div>

      <form onSubmit={onSubmit} className="grid gap-4 md:grid-cols-[1fr_420px]">
        <Card className="p-5">
          <div className="text-sm font-semibold text-zinc-900">JD input</div>
          <div className="mt-2 text-sm text-zinc-600">Paste description text. (Endpoint support depends on backend.)</div>

          <div className="mt-4">
            <textarea
              className="min-h-[260px] w-full resize-none rounded-lg border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-900 placeholder:text-zinc-400 focus:border-zinc-300 focus:outline-none"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Paste job description here..."
            />
          </div>

          <div className="mt-4 flex items-center gap-3">
            <Button type="submit" disabled={submitting || !text.trim()}>
              {submitting ? <Spinner label="Parsing JD…" /> : 'Parse JD'}
            </Button>
            {text.trim() ? <div className="text-xs text-zinc-500">Characters: {text.trim().length}</div> : null}
          </div>

          {error ? <div className="mt-4 text-sm text-rose-700">{String(error?.message ?? error)}</div> : null}
        </Card>

        <Card className="p-5">
          <div className="text-sm font-semibold text-zinc-900">Parsed signals</div>
          {submitting ? (
            <div className="mt-4">
              <Spinner label="Loading parsed JD…" />
            </div>
          ) : parsed ? (
            <div className="mt-4 space-y-3">
              <div>
            <div className="text-xs text-zinc-500">Required Skills</div>

            <div className="mt-1 text-sm font-semibold text-zinc-900">
              {parsed.skills.join(", ")}
            </div>
          </div>

          <div>
            <div className="text-xs text-zinc-500">Experience</div>

            <div className="mt-1 text-sm font-semibold text-zinc-900">
              {parsed.experience}
            </div>
          </div>

          <div>
            <div className="text-xs text-zinc-500">Education</div>

            <div className="mt-1 text-sm font-semibold text-zinc-900">
              {parsed.education}
            </div>
</div>
              <div className="rounded-lg border border-zinc-200 bg-zinc-50 p-3 text-xs text-zinc-600">
                Backend may return additional parsed fields: weights, evidence hints, and normalization tokens.
              </div>
            </div>
          ) : (
            <EmptyState title="No parsed JD yet" description="Upload a JD to see extracted signals." />
          )}
        </Card>
      </form>
    </div>
  )
}

