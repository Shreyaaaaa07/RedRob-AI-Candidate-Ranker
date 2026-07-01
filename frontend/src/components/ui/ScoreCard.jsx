import React from "react";

export default function ScoreCard({ title, score }) {
  const percentage = Math.round((score ?? 0) * 100);

  let barColor = "bg-red-500";
  let textColor = "text-red-600";

  if (percentage >= 80) {
    barColor = "bg-green-500";
    textColor = "text-green-600";
  } else if (percentage >= 50) {
    barColor = "bg-yellow-500";
    textColor = "text-yellow-600";
  }

  return (
    <div className="rounded-xl border bg-white p-4 shadow-sm hover:shadow-md transition-all duration-300">

      <div className="flex items-center justify-between">

        <span className="text-sm font-medium text-zinc-700">
          {title}
        </span>

        <span className={`text-sm font-bold ${textColor}`}>
          {percentage}%
        </span>

      </div>

      <div className="mt-3 h-2 w-full overflow-hidden rounded-full bg-zinc-200">

        <div
          className={`h-2 rounded-full transition-all duration-500 ${barColor}`}
          style={{ width: `${percentage}%` }}
        />

      </div>

    </div>
  );
}
