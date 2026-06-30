import { apiGet, apiPost } from './api'

export async function uploadJobDescription(payload) {
  // payload could be { text } or { file } depending on backend capabilities
  return apiPost('/job-description', payload)
}

export async function getParsedJobDescription() {
  return apiGet('/job-description/parsed')
}

