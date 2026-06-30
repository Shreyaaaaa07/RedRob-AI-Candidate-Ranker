import useApiQuery from './useApiQuery'
import { getExplainabilityEvidence } from '../services/explainabilityService'

export default function useExplainabilityEvidence(candidateId) {
  return useApiQuery(
    () => (candidateId ? getExplainabilityEvidence(candidateId) : Promise.resolve(null)),
    [candidateId]
  )
}

