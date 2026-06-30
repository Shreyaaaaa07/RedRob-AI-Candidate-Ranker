import { apiGet } from './api'

export async function getExplainabilityEvidence(candidateId) {
  return apiGet(`/explainability/${candidateId}`)
}

