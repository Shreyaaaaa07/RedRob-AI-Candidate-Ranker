import { useEffect, useState } from "react";
import { getAnalytics } from "../services/analyticsService";

export default function useAnalytics() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadAnalytics() {
      try {
        const result = await getAnalytics();
        setData(result);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    }

    loadAnalytics();
  }, []);

  return {
    data,
    loading,
    error,
  };
}