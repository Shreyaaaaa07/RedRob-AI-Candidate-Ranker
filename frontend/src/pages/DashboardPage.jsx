import React, { useEffect, useState } from "react";
import Card from "../components/ui/Card";
import Badge from "../components/ui/Badge";
import { Link } from "react-router-dom";
import { getDashboardSummary } from "../services/dashboardService";

export default function DashboardPage() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const data = await getDashboardSummary();
        setDashboard(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  if (loading) {
    return (
      <div className="text-lg font-medium">
        Loading Dashboard...
      </div>
    );
  }

  return (
    <div className="space-y-8">

      {/* Header */}

      <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">

        <div>
          <h1 className="text-3xl font-bold text-zinc-900">
              🤖 AI Recruiter Dashboard
          </h1>

          <p className="text-zinc-500">
            AI-powered candidate intelligence and hiring analytics.
          </p>
        </div>

        <div className="flex flex-wrap gap-3">
          <Badge variant="primary">
            AI Powered
          </Badge>

          <Badge variant="neutral">
            Explainable AI
          </Badge>
        </div>

      </div>

      {/* Summary Cards */}

      <div className="grid gap-5 md:grid-cols-4">

        <Card className="rounded-2xl border border-zinc-200 p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-lg">
          <div className="text-sm text-zinc-500">
            👥 Total Candidates
          </div>

          <div className="mt-3 text-4xl font-bold">
            {dashboard.total_candidates}
          </div>
        </Card>

        <Card className="rounded-2xl border border-zinc-200 p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-lg">
          <div className="text-sm text-zinc-500">
            📈 Average Score
          </div>

          <div className="mt-3 text-4xl font-bold text-blue-600">
            {dashboard.average_match_score}
          </div>
        </Card>

        <Card className="rounded-2xl border border-zinc-200 p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-lg">
          <div className="text-sm text-zinc-500">
            🚨 Risk Candidates
          </div>

          <div className="mt-3 text-4xl font-bold text-red-600">
            {dashboard.risk_flagged_candidates}
          </div>
        </Card>

        <Card className="rounded-2xl border border-zinc-200 p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-lg">
          <div className="text-sm text-zinc-500">
            🏆 Top Score
          </div>

          <div className="mt-3 text-4xl font-bold text-green-600">
            {dashboard.top_candidate_score}
          </div>
        </Card>

      </div>

      {/* Top Candidates */}

      <Card className="p-5">

        <h2 className="text-xl font-semibold">
          Top Ranked Candidates
        </h2>

        <div className="mt-5 overflow-hidden rounded-lg border">

          <table className="min-w-full">

            <thead className="bg-zinc-100">

              <tr>
                <th className="px-4 py-3 text-left">
                  Rank
                </th>

                <th className="px-4 py-3 text-left">
                  Candidate ID
                </th>

                <th className="px-4 py-3 text-left">
                  Hybrid Score
                </th>
              </tr>

            </thead>

            <tbody>

              {dashboard.top_candidates.map((candidate) => (

                <tr
                  key={candidate.candidate_id}
                  className="border-t hover:bg-zinc-50"
                >

                  <td className="px-4 py-3 font-semibold">
                    #{candidate.rank}
                  </td>

                  <td className="px-4 py-3">

                    <Link
                      to={`/candidate/${candidate.candidate_id}`}
                      className="text-blue-600 hover:underline font-medium"
                    >
                      {candidate.candidate_id}
                    </Link>

                  </td>

                  <td className="px-4 py-3 font-semibold text-green-600">
                    {Number(candidate.hybrid_score).toFixed(2)}
                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      </Card>

      {/* AI Recruiter Insights */}

      <Card className="rounded-2xl border border-blue-200 bg-blue-50 p-6">

        <h2 className="text-xl font-semibold">
          AI Recruiter Insights
        </h2>

        <div className="mt-5 space-y-3">

          {dashboard.ai_insights.map((insight, index) => (

            <div
              key={index}
              className="flex items-start gap-3 rounded-lg border border-green-200 bg-green-50 p-4"
            >

              <span className="text-green-600 font-bold text-lg">
                ✓
              </span>

              <span className="text-zinc-700">
                {insight}
              </span>

            </div>

          ))}

        </div>

      </Card>

    </div>
  );
}
