import useApiQuery from './useApiQuery'
import { getCandidateDetails } from '../services/candidateService'

export default function useCandidateDetails(candidateId) {
  return useApiQuery(
    () => (candidateId ? getCandidateDetails(candidateId) : Promise.resolve(null)),
    [candidateId]
  )
}

