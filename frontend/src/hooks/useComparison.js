import { useState } from "react";
import { getCandidate } from "../services/comparisonService";

export default function useComparison() {
  const [candidateAData, setCandidateAData] = useState(null);
  const [candidateBData, setCandidateBData] = useState(null);
  const [loading, setLoading] = useState(false);

  async function compare(candidateA, candidateB) {
    setLoading(true);

    try {
      const [a, b] = await Promise.all([
        getCandidate(candidateA),
        getCandidate(candidateB),
      ]);

      setCandidateAData(a.candidate ?? a);
      setCandidateBData(b.candidate ?? b);
    } finally {
      setLoading(false);
    }
  }

  return {
    candidateAData,
    candidateBData,
    loading,
    compare,
  };
}