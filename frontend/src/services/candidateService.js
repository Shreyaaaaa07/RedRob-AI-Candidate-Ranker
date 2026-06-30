import { apiGet } from "./api";

export async function getCandidateDetails(candidateId) {
  return apiGet(`/candidate/${candidateId}`);
}