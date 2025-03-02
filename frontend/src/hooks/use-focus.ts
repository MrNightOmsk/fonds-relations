import { useEffect, useRef } from "react"

export function useFocus<T extends HTMLElement>() {
  const ref = useRef<T>(null)

  useEffect(() => {
    if (ref.current) {
      ref.current.focus()
    }
  }, [])

  return ref
} 