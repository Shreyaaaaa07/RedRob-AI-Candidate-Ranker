import React, { useMemo } from 'react'
import { Link, useParams } from 'react-router-dom'
import Card from '../components/ui/Card'
import Badge from '../components/ui/Badge'
import Spinner from '../components/ui/Spinner'
import ErrorState from '../components/ui/ErrorState'
import EmptyState from '../components/ui/EmptyState'
import EvidencePanel from '../components/evidence/EvidencePanel'
import useCandidateDetails from '../hooks/useCandidateDetails'
import ScoreCard from "../components/ui/ScoreCard";

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

let recommendation = "Needs Further Review";
let confidence = 70;
const strengths = [];
const concerns = [];

if (candidate.experience_match_score >= 0.8) {
  strengths.push("Excellent experience match");
}

if (candidate.semantic_similarity_score >= 0.7) {
  strengths.push("Strong semantic alignment");
} else {
  concerns.push("Moderate semantic alignment");
}

if (candidate.retrieval_score >= 0.8) {
  strengths.push("Excellent retrieval expertise");
}

if (candidate.ranking_system_score >= 0.8) {
  strengths.push("Strong ranking system experience");
}

if (candidate.production_ml_score >= 0.7) {
  strengths.push("Production ML experience");
}

if (candidate.vector_database_score < 0.5) {
  concerns.push("Limited vector database experience");
}

if (candidate.startup_fit_score < 0.6) {
  concerns.push("Moderate startup fit");
}

if (candidate.risk_score === 0) {
  strengths.push("No risk flags detected");
}

if (
  candidate.hybrid_score >= 70 &&
  candidate.risk_score === 0
) {
  recommendation = "Proceed to Technical Interview";
  confidence = 95;
}
else if (candidate.hybrid_score >= 55) {
  recommendation = "Proceed to Recruiter Screening";
  confidence = 82;
}
else {
  recommendation = "Keep as Backup Candidate";
  confidence = 65;
}

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
                <Badge variant="primary"> Score: {candidate.hybrid_score?.toFixed(2) ?? '—'}</Badge>
              </div>
            </div>

            <div className="mt-4 grid grid-cols-2 gap-4 lg:grid-cols-5">

              <div className="rounded-xl border bg-white p-4">
                <div className="text-xs text-zinc-500">
                  Rank
                </div>

                <div className="mt-2 text-2xl font-bold">
                  #{candidate.rank}
                </div>
              </div>

              <div className="rounded-xl border bg-white p-4">
                <div className="text-xs text-zinc-500">
                  Hybrid Score
                </div>

                <div className="mt-2 text-2xl font-bold text-blue-600">
                  {candidate.hybrid_score.toFixed(2)}
                </div>
              </div>

              <div className="rounded-xl border bg-white p-4">
                <div className="text-xs text-zinc-500">
                  Semantic Match
                </div>

                <div className="mt-2 text-2xl font-bold">
                  {(candidate.semantic_similarity_score * 100).toFixed(0)}%
                </div>
              </div>

              <div className="rounded-xl border bg-white p-4">
                <div className="text-xs text-zinc-500">
                  Experience Match
                </div>

                <div className="mt-2 text-2xl font-bold">
                  {(candidate.experience_match_score * 100).toFixed(0)}%
                </div>
              </div>

              <div className="rounded-xl border bg-white p-4">
                <div className="text-xs text-zinc-500">
                  Risk Score
                </div>

                <div className="mt-2 text-2xl font-bold text-red-600">
                  {candidate.risk_score}
                </div>
              </div>

            </div>

          </Card>

          <Card className="p-5">

            <div className="text-lg font-semibold text-zinc-900">
              Technical Evaluation
            </div>

            <div className="mt-5 grid grid-cols-2 gap-4">

              <ScoreCard
                title="Experience Match"
                score={candidate.experience_match_score}
              />

              <ScoreCard
                title="Skill Match"
                score={candidate.skill_match_score}
              />

              <ScoreCard
                title="Semantic Similarity"
                score={candidate.semantic_similarity_score}
              />

              <ScoreCard
                title="Production ML"
                score={candidate.production_ml_score}
              />

              <ScoreCard
                title="Retrieval"
                score={candidate.retrieval_score}
              />

              <ScoreCard
                title="Vector Database"
                score={candidate.vector_database_score}
              />

              <ScoreCard
                title="Ranking Systems"
                score={candidate.ranking_system_score}
              />

              <ScoreCard
                title="Evaluation Framework"
                score={candidate.evaluation_framework_score}
              />

            </div>

          </Card>

          <Card className="p-5">

            <div className="text-lg font-semibold text-zinc-900">
              Behavior & Career Evaluation
            </div>

            <div className="mt-5 grid grid-cols-2 gap-4">

              <ScoreCard
                title="Activity"
                score={candidate.activity_score}
              />

              <ScoreCard
                title="Engagement"
                score={candidate.engagement_score}
              />

              <ScoreCard
                title="Availability"
                score={candidate.availability_score}
              />

              <ScoreCard
                title="Recruiter Interest"
                score={candidate.recruiter_interest_score}
              />

              <ScoreCard
                title="Career Stability"
                score={candidate.career_stability_score}
              />

              <ScoreCard
                title="Experience Consistency"
                score={candidate.experience_consistency_score}
              />

              <ScoreCard
                title="Education"
                score={candidate.education_score}
              />

              <ScoreCard
                title="Startup Fit"
                score={candidate.startup_fit_score}
              />

            </div>

          </Card>

          </div>

          <div className="space-y-4">

            <Card className="p-5">

              <div className="flex items-center justify-between">

                <h2 className="text-lg font-semibold text-zinc-900">
                  🤖 AI Recruiter Recommendation
                </h2>

                <Badge variant="primary">
                  {confidence}% Confidence
                </Badge>

              </div>

              <div className="mt-5">

                <div className="text-sm text-zinc-500">
                  Recommendation
                </div>

                <div className="mt-1 text-2xl font-bold text-green-600">
                  {recommendation}
                </div>

              </div>

              <div className="mt-6">

                <h3 className="font-semibold text-zinc-900">
                  Strengths
                </h3>

                <ul className="mt-2 space-y-2">

                  {strengths.map((item, index) => (

                    <li
                      key={index}
                      className="flex items-center gap-2 text-sm text-zinc-700"
                    >
                      <span className="text-green-600">✔</span>

                      {item}

                    </li>

                  ))}

                </ul>

              </div>

              <div className="mt-6">

                <h3 className="font-semibold text-zinc-900">
                  Concerns
                </h3>

                <ul className="mt-2 space-y-2">

                  {concerns.length === 0 ? (

                    <li className="text-sm text-zinc-500">
                      No significant concerns detected.
                    </li>

                  ) : (

                    concerns.map((item, index) => (

                      <li
                        key={index}
                        className="flex items-center gap-2 text-sm text-zinc-700"
                      >
                        <span className="text-yellow-500">⚠</span>

                        {item}

                      </li>

                    ))

                  )}

                </ul>

              </div>

            </Card>
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

