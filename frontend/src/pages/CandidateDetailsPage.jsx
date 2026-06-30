import React, { useMemo } from 'react'
import { Link, useParams } from 'react-router-dom'
import Card from '../components/ui/Card'
import Badge from '../components/ui/Badge'
import Spinner from '../components/ui/Spinner'
import ErrorState from '../components/ui/ErrorState'
import EmptyState from '../components/ui/EmptyState'
import EvidencePanel from '../components/evidence/EvidencePanel'
import useCandidateDetails from '../hooks/useCandidateDetails'

export default function CandidateDetailsPage() {
  const { candidateId } = useParams()
  const { data, error, loading } = useCandidateDetails(candidateId)

  const candidate = useMemo(() => {
    if (!data) return null
    return data.candidate ?? data
  }, [data])

  const evidencePreview = useMemo(() => {

    if (!candidate)
        return {}

    try {

        return typeof candidate.evidence === "string"
            ? JSON.parse(candidate.evidence)
            : (candidate.evidence || {})

    }

    catch {

        return {}

    }

  }, [candidate])

  if (loading) {
    return (
      <div className="p-2">
        <Spinner label="Loading candidate…" />
      </div>
    )
  }

  if (error) {
    return (
      <ErrorState message={String(error?.message ?? error)} />
    )
  }

  if (!candidate) {
    return <EmptyState title="Candidate not found" description="Try going back to rankings." />
  }

const score = candidate.hybrid_score

const match = Math.round(
    (candidate.semantic_similarity_score ?? 0) * 100
)

const risks =
    candidate.risk_flags
        ? (
            typeof candidate.risk_flags === "string"
                ? JSON.parse(candidate.risk_flags || "[]")
                : candidate.risk_flags
          )
        : []

const riskCount = risks.length

const evidence =
    typeof candidate.evidence === "string"
        ? JSON.parse(candidate.evidence)
        : (candidate.evidence || {})

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-zinc-900">Candidate Details</h1>
        <p className="mt-1 text-sm text-zinc-600">Evidence-backed view for recruiter decisions.</p>
      </div>

      <div className="grid gap-4 lg:grid-cols-[1fr_420px]">
        <div className="space-y-4">
          <Card className="p-5">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <div className="text-sm text-zinc-500">Name</div>
                <div className="mt-1 text-lg font-bold text-zinc-900">{candidate.name ?? candidate.profile?.name ?? `Candidate ${candidateId}`}</div>
                <div className="mt-1 text-sm text-zinc-600">{candidate.title ?? candidate.profile?.title ?? '—'}</div>
              </div>
              <div className="flex items-center gap-2">
                {riskCount > 0 ? <Badge variant="danger">{riskCount} risk flags</Badge> : <Badge variant="success">No risks</Badge>}
                <Badge variant="primary">Score: {score ?? '—'}</Badge>
              </div>
            </div>

            <div className="mt-4 grid gap-4 sm:grid-cols-2">
              <div>
                <div className="text-xs text-zinc-500">JD match</div>
                <div className="mt-1 text-sm font-semibold text-zinc-900">{match ?? '—'}</div>
              </div>
              <div>
                <div className="text-xs text-zinc-500">Experience</div>
                <div className="mt-1 text-sm font-semibold text-zinc-900">{candidate.years_of_experience ?? candidate.profile?.years_of_experience ?? '—'}</div>
              </div>
            </div>

            <div className="mt-4 rounded-xl border border-zinc-200 bg-zinc-50 p-4">
              <div className="text-sm font-semibold text-zinc-900">Recruiter summary</div>
              <div className="mt-1 text-sm text-zinc-600">
                {candidate.summary ?? candidate.recruiter_summary ?? 'Review evidence to understand why this candidate ranks highly/lowly.'}
              </div>
            </div>
          </Card>

          <Card className="p-5">

            <div className="text-lg font-semibold text-zinc-900">
              AI Feature Scores
            </div>

            <div className="mt-5 grid grid-cols-2 gap-4">

              <div className="rounded-lg border p-3">
                <div className="text-xs text-zinc-500">Hybrid Score</div>
                <div className="text-xl font-bold">
                  {candidate.hybrid_score?.toFixed(2)}
                </div>
              </div>

              <div className="rounded-lg border p-3">
                <div className="text-xs text-zinc-500">Experience Match</div>
                <div className="text-xl font-bold">
                  {(candidate.experience_match_score * 100).toFixed(0)}%
                </div>
              </div>

              <div className="rounded-lg border p-3">
                <div className="text-xs text-zinc-500">Skill Match</div>
                <div className="text-xl font-bold">
                  {(candidate.skill_match_score * 100).toFixed(0)}%
                </div>
              </div>

              <div className="rounded-lg border p-3">
                <div className="text-xs text-zinc-500">Semantic Similarity</div>
                <div className="text-xl font-bold">
                  {(candidate.semantic_similarity_score * 100).toFixed(0)}%
                </div>
              </div>

              <div className="rounded-lg border p-3">
                <div className="text-xs text-zinc-500">Production ML</div>
                <div className="text-xl font-bold">
                  {(candidate.production_ml_score * 100).toFixed(0)}%
                </div>
              </div>

              <div className="rounded-lg border p-3">
                <div className="text-xs text-zinc-500">Risk Score</div>
                <div className="text-xl font-bold text-red-600">
                  {candidate.risk_score}
                </div>
              </div>

            </div>

          </Card>
        </div>

        <div className="space-y-4">
          <Card className="p-5">
            <div className="flex items-center justify-between gap-3">
              <div>
                <div className="text-sm font-semibold text-zinc-900">Explainability</div>
                <div className="mt-1 text-sm text-zinc-600">Evidence snippets powering the score.</div>
              </div>
              <Link to={`/explainability/${candidateId}`} className="text-sm font-semibold text-zinc-900 hover:underline">
                Open evidence →
              </Link>

            </div>

            <div className="mt-4">
              <EvidencePanel title="Top Evidence" evidence={evidencePreview} />
            </div>
          </Card>

          <Card className="p-5">
            <div className="text-sm font-semibold text-zinc-900">Next steps</div>
            <div className="mt-2 space-y-3 text-sm text-zinc-600">
              <div>• Validate behavioral signals aligned with JD expectations.</div>
              <div>• Check risk flags and decide whether to request clarifications.</div>
              <div>• Use evidence items as recruiter talking points.</div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}

