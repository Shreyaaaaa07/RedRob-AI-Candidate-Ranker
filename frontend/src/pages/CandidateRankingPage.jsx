import Card from '../components/ui/Card'
import Input from '../components/ui/Input'
import Select from '../components/ui/Select'
import React, { useMemo } from 'react'
import Table from '../components/ui/Table'
import Badge from '../components/ui/Badge'
import EmptyState from '../components/ui/EmptyState'
import ErrorState from '../components/ui/ErrorState'
import Pagination from '../components/ui/Pagination'
import Spinner from '../components/ui/Spinner'
import { Link } from 'react-router-dom'
import useCandidateRanking from '../hooks/useCandidateRanking'

function rankToBadge(score) {
  if (score === null || score === undefined || Number.isNaN(Number(score))) return <Badge>—</Badge>
  const s = Number(score)
  if (s >= 80) return <Badge variant="success">Strong</Badge>
  if (s >= 60) return <Badge variant="primary">Good</Badge>
  if (s >= 40) return <Badge variant="warning">Review</Badge>
  return <Badge variant="danger">Risk</Badge>
}

export default function CandidateRankingPage() {
    const { data, error, loading, page, setPage, pageSize, search, setSearch, sort, setSort, jobId, setJobId } =
      useCandidateRanking()

    const rows = useMemo(() => {
      if (!data) return []

      if (Array.isArray(data))
          return data

      return data.candidates ?? data.results ?? []
  }, [data])

  const total = rows.length

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-zinc-900">Candidate Rankings</h1>
          <p className="mt-1 text-sm text-zinc-600">Recruiter-first view: score, match, and evidence cues.</p>
        </div>
      </div>

      <Card className="p-5">
        <div className="grid gap-4 md:grid-cols-4">
          <div className="md:col-span-2">
            <div className="text-xs font-medium text-zinc-500">Search candidates</div>
            <div className="mt-2">
              <Input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Name, skill keyword, etc." />
            </div>
          </div>

          <div>
            <div className="text-xs font-medium text-zinc-500">Sort</div>
            <div className="mt-2">
              <Select
                value={sort}
                onChange={(e) => setSort(e.target.value)}
                options={[
                  { value: 'score_desc', label: 'Score (high → low)' },
                  { value: 'score_asc', label: 'Score (low → high)' },
                ]}
              />
            </div>
          </div>

          <div>
            <div className="text-xs font-medium text-zinc-500">Job ID (optional)</div>
            <div className="mt-2">
              <Input value={jobId ?? ''} onChange={(e) => setJobId(e.target.value || null)} placeholder="e.g. 1" />
            </div>
          </div>
        </div>

        <div className="mt-4 text-xs text-zinc-500">
          Note: backend endpoint shapes may differ. This UI expects a list of candidates with id + score fields.
        </div>
      </Card>

      <Card className="p-0">
        {loading ? (
          <div className="p-5">
            <Spinner label="Fetching ranked candidates…" />
          </div>
        ) : error ? (
          <div className="p-5">
            <ErrorState message={String(error?.message ?? error)} />
          </div>
        ) : rows.length === 0 ? (
          <div className="p-5">
            <EmptyState title="No candidates found" description="Try changing search or sort." />
          </div>
        ) : (
          <>
            <Table>
              <thead className="bg-zinc-50 text-left text-xs font-semibold uppercase tracking-wide text-zinc-500">
                <tr>
                  <th className="px-4 py-3">Rank</th>
                  <th className="px-4 py-3">Candidate</th>
                  <th className="px-4 py-3">Score</th>
                  <th className="px-4 py-3">Match</th>
                  <th className="px-4 py-3">Risk</th>
                  <th className="px-4 py-3">Evidence</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-200 bg-white text-sm">
                {rows.map((c) => {
                  const id = c.candidate_id ?? c.id ?? c.candidateId
                  const score =
                    c.hybrid_score ??
                    c.score ??
                    c.rank_score ??
                    c.total_score ??
                    0

                  const match = Math.round(
                    (c.semantic_similarity_score ?? 0) * 100
                  )

                  const risks =
                    c.risk_flags
                      ? (
                          typeof c.risk_flags === "string"
                            ? JSON.parse(c.risk_flags || "[]")
                            : c.risk_flags
                        )
                      : []

                  const riskCount = risks.length

                  let evidence = {}

                  try {
                    evidence =
                      typeof c.evidence === "string"
                        ? JSON.parse(c.evidence)
                        : (c.evidence || {})
                  } catch {
                    evidence = {}
                  }

                  const evidenceCount = Object.keys(evidence).length

                  return (
                    <tr key={id} className="hover:bg-zinc-50">

                      <td className="px-4 py-3 font-bold text-zinc-900">
                        #{c.rank}
                      </td>

                      <td className="px-4 py-3">
                        <Link
                          to={`/candidate/${id}`}
                          className="font-semibold text-zinc-900 hover:underline"
                        >
                          {id}
                        </Link>

                        <td className="px-4 py-3">
                          <Link
                            to={`/candidate/${id}`}
                            className="font-semibold text-zinc-900 hover:underline"
                          >
                            {id}
                          </Link>

                          <div className="mt-1 text-xs text-zinc-500">
                            Hybrid Score: {Number(score).toFixed(2)}
                          </div>
                        </td>
                      </td>

                      <td className="px-4 py-3">
                        <div className="flex items-center gap-2">
                          <span className="font-semibold">
                            {Number(score).toFixed(2)}
                          </span>

                          {rankToBadge(score)}
                        </div>
                      </td>

                      <td className="px-4 py-3">
                        {match}%
                      </td>

                      <td className="px-4 py-3">
                        {riskCount > 0 ? (
                          <Badge variant="danger">
                            {riskCount} Flag{riskCount > 1 ? "s" : ""}
                          </Badge>
                        ) : (
                          <Badge variant="success">
                            Safe
                          </Badge>
                        )}
                      </td>

                      <td className="px-4 py-3">
                        <Link
                            to={`/candidate/${id}`}
                            className="text-blue-600 hover:underline font-medium"
                        >
                            View Details →
                        </Link>
                      </td>

                    </tr>
                  )
                })}
              </tbody>
            </Table>

            <div className="p-5">
              <Pagination
                page={page}
                pageSize={pageSize}
                total={total}
                onPageChange={(p) => setPage(p)}
              />
            </div>
          </>
        )}
      </Card>
    </div>
  )
}

