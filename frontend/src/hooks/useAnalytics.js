import useApiQuery from "./useApiQuery";
import { getAnalytics } from "../services/analyticsService";

export default function useAnalytics() {
  return useApiQuery(
    () => getAnalytics(),
    []
  );
}