import React, { useMemo } from 'react'
import { useParams } from 'react-router-dom'
import Card from '../components/ui/Card'
import Spinner from '../components/ui/Spinner'
import ErrorState from '../components/ui/ErrorState'
import EmptyState from '../components/ui/EmptyState'
import EvidencePanel from '../components/evidence/EvidencePanel'
import useExplainabilityEvidence from '../hooks/useExplainabilityEvidence'

export default function ExplainabilityPage() {

  const params = useParams()
  const candidateId = params.candidateId ?? params.id

  const safeCandidateId = candidateId ?? null

  const { data, error, loading } =
    useExplainabilityEvidence(safeCandidateId)

  const evidence = useMemo(() => {
    if (!data) return {}
    return data.evidence ?? {}
  }, [data])

  if (loading)
    return <Spinner label="Loading evidence..." />

  if (error)
    return <ErrorState message={String(error?.message ?? error)} />

  return (
    <div className="space-y-6">

      <div>
        <h1 className="text-2xl font-bold text-zinc-900">
          Explainability
        </h1>

        <p className="mt-1 text-sm text-zinc-600">
          AI-generated evidence explaining why this candidate received their final ranking.
        </p>
      </div>

      {/* Candidate Summary */}

      <Card className="p-5">

        <h2 className="text-xl font-bold text-zinc-900">
          Candidate Summary
        </h2>

        <div className="mt-5 grid grid-cols-1 gap-4 md:grid-cols-3">

          <div className="rounded-lg border border-zinc-200 p-4">

            <div className="text-xs text-zinc-500">
              Hybrid Score
            </div>

            <div className="mt-2 text-2xl font-bold text-blue-600">
              {data?.hybrid_score?.toFixed(2)}
            </div>

          </div>

          <div className="rounded-lg border border-zinc-200 p-4">

            <div className="text-xs text-zinc-500">
              Rank
            </div>

            <div className="mt-2 text-2xl font-bold text-zinc-900">
              #{data?.rank}
            </div>

          </div>

          <div className="rounded-lg border border-zinc-200 p-4">

            <div className="text-xs text-zinc-500">
              Risk Score
            </div>

            <div className="mt-2 text-2xl font-bold text-green-600">
              {data?.risk_score}
            </div>

          </div>

        </div>

      </Card>

      {/* Main Content */}

      <div className="grid gap-4 lg:grid-cols-[1fr_420px]">

        <Card className="p-5">

          <div className="text-lg font-semibold text-zinc-900">
            Evidence
          </div>

          <div className="mt-4">

            {Object.keys(evidence).length === 0 ? (

              <EmptyState
                title="No evidence available"
                description={
                  candidateId
                    ? "Backend returned no evidence."
                    : "Select a candidate to view evidence."
                }
              />

            ) : (

              <EvidencePanel
                title={`Candidate ${candidateId}`}
                evidence={evidence}
              />

            )}

          </div>

        </Card>

        <Card className="p-5">

          <div className="text-lg font-semibold text-zinc-900">
            Recruiter Tips
          </div>

          <div className="mt-4 space-y-3 text-sm text-zinc-600">

            <div>
              • Review each evidence category before making interview decisions.
            </div>

            <div>
              • Compare semantic similarity with skill matching to understand ranking quality.
            </div>

            <div>
              • High hybrid score with low risk indicates a strong candidate.
            </div>

            <div>
              • Use these evidence snippets as discussion points during technical interviews.
            </div>

          </div>

        </Card>

      </div>

    </div>
  )
}