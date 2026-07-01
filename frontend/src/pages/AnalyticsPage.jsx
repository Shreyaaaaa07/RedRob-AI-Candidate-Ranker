import React from "react";
import Card from "../components/ui/Card";
import Spinner from "../components/ui/Spinner";
import ErrorState from "../components/ui/ErrorState";
import useAnalytics from "../hooks/useAnalytics";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
} from "recharts";

export default function AnalyticsPage() {

  const { data, loading, error } = useAnalytics();

  const chartData = Object.entries(
    data?.score_distribution ?? {}
  ).map(([range, count]) => ({
    range,
    count,
  }));

  const riskData = [
  {
    name: "Safe",
    value:
      (data?.total_candidates ?? 0) -
      (data?.risk_candidates ?? 0),
  },
  {
    name: "Risk",
    value: data?.risk_candidates ?? 0,
  },
];

  const COLORS = ["#22c55e", "#ef4444"];

  if (loading)
    return <Spinner label="Loading analytics..." />;

  if (error)
    return <ErrorState message={String(error)} />;

  return (
    <div className="space-y-6">

      <div>
        <h1 className="text-3xl font-bold text-zinc-900">
          Analytics Dashboard
        </h1>

        <p className="mt-2 text-zinc-600">
          AI Candidate Ranking Insights
        </p>
      </div>

      {/* Summary Cards */}

      <div className="grid grid-cols-1 gap-4 md:grid-cols-4">

        <Card className="p-5">
          <div className="text-sm text-zinc-500">
            Total Candidates
          </div>

          <div className="mt-3 text-3xl font-bold">
            {data?.total_candidates ?? 0}
          </div>
        </Card>

        <Card className="p-5">
          <div className="text-sm text-zinc-500">
            Average Score
          </div>

          <div className="mt-3 text-3xl font-bold text-blue-600">
            {data?.average_score ?? 0}
          </div>
        </Card>

        <Card className="p-5">
          <div className="text-sm text-zinc-500">
            Top Score
          </div>

          <div className="mt-3 text-3xl font-bold text-green-600">
            {data?.top_score ?? 0}
          </div>
        </Card>

        <Card className="p-5">
          <div className="text-sm text-zinc-500">
            Risk Candidates
          </div>

          <div className="mt-3 text-3xl font-bold text-red-600">
            {data?.risk_candidates ?? 0}
          </div>
        </Card>

      </div>

      {/* Score Distribution */}

      <Card className="p-5">

        <h2 className="text-xl font-semibold">
          Score Distribution
        </h2>

        <div className="mt-6 h-80">

          <ResponsiveContainer width="100%" height="100%">

            <BarChart data={chartData}>

              <XAxis dataKey="range" />

              <YAxis />

              <Tooltip />

              <Bar
                dataKey="count"
                radius={[8, 8, 0, 0]}
              />

            </BarChart>

          </ResponsiveContainer>

        </div>

      </Card>

      <Card className="p-5">

        <h2 className="text-xl font-semibold">
          Risk Distribution
        </h2>

        <div className="mt-6 h-80">

          <ResponsiveContainer width="100%" height="100%">

            <PieChart>

              <Pie
                data={riskData}
                dataKey="value"
                nameKey="name"
                outerRadius={100}
                label
              >
                {riskData.map((entry, index) => (
                  <Cell
                    key={index}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>

              <Tooltip />

              <Legend />

            </PieChart>

          </ResponsiveContainer>

        </div>

      </Card>

      {/* Top Skills */}

      <Card className="p-5">

        <h2 className="text-xl font-semibold">
          Top Skills
        </h2>

        <div className="mt-4 flex flex-wrap gap-3">

          {(data?.top_skills ?? []).map(skill => (

            <span
              key={skill}
              className="rounded-full bg-blue-100 px-4 py-2 text-sm font-medium text-blue-700"
            >
              {skill}
            </span>

          ))}

        </div>

      </Card>

    </div>
  );
}