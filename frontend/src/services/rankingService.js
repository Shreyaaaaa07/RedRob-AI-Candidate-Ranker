import { apiGet } from './api'

export async function getCandidateRankings({ jobId, page = 1, pageSize = 20, search = '', sort = 'score_desc' } = {}) {
  return apiGet('/rankings', {
    params: { jobId, page, pageSize, search, sort },
  })
}

