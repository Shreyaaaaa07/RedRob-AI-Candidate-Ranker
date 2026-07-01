import React, { useState } from "react";
import Card from "../components/ui/Card";
import useComparison from "../hooks/useComparison";

export default function CandidateComparisonPage() {

  const [candidateA, setCandidateA] = useState("");
  const [candidateB, setCandidateB] = useState("");

  const {
    candidateAData,
    candidateBData,
    loading,
    compare,
  } = useComparison();

  return (
    <div className="space-y-6">

      <div>
        <h1 className="text-3xl font-bold text-zinc-900">
          Candidate Comparison
        </h1>

        <p className="mt-2 text-zinc-600">
          Compare two candidates side by side using AI evaluation metrics.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">

        {/* Candidate A */}

        <Card className="p-6">

          <h2 className="text-xl font-semibold">
            Candidate A
          </h2>

          <div className="mt-6">

            <input
              value={candidateA}
              onChange={(e) => setCandidateA(e.target.value)}
              placeholder="Enter Candidate ID"
              className="w-full rounded-lg border p-3"
            />

          </div>

          {candidateAData && (

            <div className="mt-6 space-y-2">

              <div>
                <strong>ID:</strong> {candidateAData.candidate_id}
              </div>

              <div>
                <strong>Hybrid Score:</strong>{" "}
                {candidateAData.hybrid_score?.toFixed(2)}
              </div>

              <div>
                <strong>Semantic Match:</strong>{" "}
                {(candidateAData.semantic_similarity_score * 100).toFixed(0)}%
              </div>

              <div>
                <strong>Experience Match:</strong>{" "}
                {(candidateAData.experience_match_score * 100).toFixed(0)}%
              </div>

              <div>
                <strong>Risk Score:</strong>{" "}
                {candidateAData.risk_score}
              </div>

            </div>

          )}

        </Card>

        {/* Candidate B */}

        <Card className="p-6">

          <h2 className="text-xl font-semibold">
            Candidate B
          </h2>

          <div className="mt-6">

            <input
              value={candidateB}
              onChange={(e) => setCandidateB(e.target.value)}
              placeholder="Enter Candidate ID"
              className="w-full rounded-lg border p-3"
            />

          </div>

          {candidateBData && (

            <div className="mt-6 space-y-2">

              <div>
                <strong>ID:</strong> {candidateBData.candidate_id}
              </div>

              <div>
                <strong>Hybrid Score:</strong>{" "}
                {candidateBData.hybrid_score?.toFixed(2)}
              </div>

              <div>
                <strong>Semantic Match:</strong>{" "}
                {(candidateBData.semantic_similarity_score * 100).toFixed(0)}%
              </div>

              <div>
                <strong>Experience Match:</strong>{" "}
                {(candidateBData.experience_match_score * 100).toFixed(0)}%
              </div>

              <div>
                <strong>Risk Score:</strong>{" "}
                {candidateBData.risk_score}
              </div>

            </div>

          )}

        </Card>

      </div>

      {/* Compare Button */}

      <div className="flex justify-center">

        <button
          onClick={() => compare(candidateA, candidateB)}
          className="rounded-lg bg-blue-600 px-8 py-3 font-semibold text-white hover:bg-blue-700"
        >
          {loading ? "Comparing..." : "Compare Candidates"}
        </button>

      </div>

      {/* AI Recommendation */}

      <Card className="p-6">

        <h2 className="text-xl font-semibold">
          AI Recommendation
        </h2>

        {!candidateAData || !candidateBData ? (

          <div className="mt-4 rounded-xl bg-blue-50 p-4 text-blue-700">
            Select two candidates and click <strong>Compare Candidates</strong>.
          </div>

        ) : (

          <div className="mt-4 rounded-xl bg-green-50 p-4">

            <div className="font-semibold text-lg">
              Recommended Candidate:
            </div>

            <div className="mt-2 text-xl font-bold text-green-700">
              {candidateAData.hybrid_score >= candidateBData.hybrid_score
                ? candidateAData.candidate_id
                : candidateBData.candidate_id}
            </div>

            <div className="mt-4 text-zinc-700">

              {candidateAData.hybrid_score >= candidateBData.hybrid_score
                ? `${candidateAData.candidate_id} has a higher hybrid score (${candidateAData.hybrid_score.toFixed(
                    2
                  )}) than ${candidateBData.candidate_id} (${candidateBData.hybrid_score.toFixed(
                    2
                  )}).`
                : `${candidateBData.candidate_id} has a higher hybrid score (${candidateBData.hybrid_score.toFixed(
                    2
                  )}) than ${candidateAData.candidate_id} (${candidateAData.hybrid_score.toFixed(
                    2
                  )}).`}

            </div>

          </div>

        )}

      </Card>

    </div>
  );
}