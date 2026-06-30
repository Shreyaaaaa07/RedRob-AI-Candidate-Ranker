import { useEffect, useState, useCallback } from 'react'

export default function useApiQuery(queryFn, deps = []) {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const run = useCallback(async () => {
    if (!queryFn) return
    setLoading(true)
    setError(null)
    try {
      const res = await queryFn()
      setData(res)
    } catch (e) {
      setError(e)
      setData(null)
    } finally {
      setLoading(false)
    }
  }, [queryFn])

  useEffect(() => {
    run()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps)

  return { data, error, loading, refetch: run }
}

