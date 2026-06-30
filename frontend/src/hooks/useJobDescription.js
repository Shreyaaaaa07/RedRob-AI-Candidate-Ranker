import useApiQuery from './useApiQuery'
import { getParsedJobDescription } from '../services/jobDescriptionService'

export default function useJobDescription() {
  return useApiQuery(() => getParsedJobDescription(), [])
}

