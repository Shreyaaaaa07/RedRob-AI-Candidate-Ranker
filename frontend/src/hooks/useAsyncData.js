import { useCallback, useEffect, useState } from 'react'

export default function useAsyncData(asyncFn, deps = []) {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  const exec = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await asyncFn()
      setData(res)
    } catch (e) {
      setError(e)
      setData(null)
    } finally {
      setLoading(false)
    }
  }, [asyncFn])

  useEffect(() => {
    exec()
  }, deps) // eslint-disable-line

  return { data, error, loading, refetch: exec }
}

