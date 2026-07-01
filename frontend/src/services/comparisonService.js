import { apiGet } from "./api";

export async function getCandidate(candidateId) {
  return apiGet(`/candidate/${candidateId}`);
}