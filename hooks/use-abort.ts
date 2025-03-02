import { useCallback, useRef } from "react"

export function useAbort() {
  const abortControllerRef = useRef<AbortController | null>(null)

  const abort = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
      abortControllerRef.current = null
    }
  }, [])

  const getSignal = useCallback(() => {
    abort()
    abortControllerRef.current = new AbortController()
    return abortControllerRef.current.signal
  }, [abort])

  return { getSignal, abort }
} 