import { useEffect, useMemo, useState, useCallback } from 'react'
import { getCandidateRankings } from '../services/rankingService'

export default function useCandidateRanking() {
  const [page, setPage] = useState(1)
  const [pageSize] = useState(20)
  const [search, setSearch] = useState('')
  const [sort, setSort] = useState('score_desc')
  const [jobId, setJobId] = useState(null)

  const queryKey = useMemo(() => ({ page, pageSize, search, sort, jobId }), [page, pageSize, search, sort, jobId])

  const [state, setState] = useState({ loading: true, error: null, data: null })

  const fetchData = useCallback(async () => {
    setState({ loading: true, error: null, data: null })
    try {
      const res = await getCandidateRankings({ ...queryKey })
      setState({ loading: false, error: null, data: res })
    } catch (e) {
      setState({ loading: false, error: e, data: null })
    }
  }, [queryKey])

  useEffect(() => {
    fetchData()
  }, [fetchData])

  return {
    ...state,
    page,
    setPage,
    pageSize,
    search,
    setSearch,
    sort,
    setSort,
    jobId,
    setJobId,
  }
}

