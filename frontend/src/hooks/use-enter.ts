import { useEffect } from "react"

export function useEnter(callback: () => void) {
  useEffect(() => {
    const handleEnter = (event: KeyboardEvent) => {
      if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
        const target = event.target as HTMLElement
        const tagName = target.tagName.toLowerCase()
        
        // Ignore Enter key press in text areas and buttons
        if (tagName === "textarea" || tagName === "button") {
          return
        }

        // If we are in an input field and it is not the last field in the form,
        // allow the default behavior (move to the next field)
        if (tagName === "input") {
          const form = target.closest("form")
          if (form) {
            const inputs = Array.from(form.querySelectorAll("input:not([type=hidden])"))
            const currentIndex = inputs.indexOf(target as HTMLInputElement)
            if (currentIndex < inputs.length - 1) {
              return
            }
          }
        }

        event.preventDefault()
        callback()
      }
    }

    document.addEventListener("keydown", handleEnter)

    return () => {
      document.removeEventListener("keydown", handleEnter)
    }
  }, [callback])
}