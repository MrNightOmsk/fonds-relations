"use client"

import { useEffect, useState } from "react"
import { cn } from "@/lib/utils"
import { useEscape } from "@/hooks/use-escape"

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  children: React.ReactNode
  className?: string
}

export function Modal({
  isOpen,
  onClose,
  children,
  className,
}: ModalProps) {
  const [isAnimating, setIsAnimating] = useState(false)
  const [shouldRender, setShouldRender] = useState(false)

  useEscape(onClose)

  useEffect(() => {
    if (isOpen) {
      setShouldRender(true)
      requestAnimationFrame(() => {
        setIsAnimating(true)
      })
    } else {
      setIsAnimating(false)
      const timer = setTimeout(() => {
        setShouldRender(false)
      }, 200) // Длительность анимации
      return () => clearTimeout(timer)
    }
  }, [isOpen])

  if (!shouldRender) return null

  return (
    <div
      className={cn(
        "fixed inset-0 z-50 transition-opacity duration-200",
        isAnimating ? "opacity-100" : "opacity-0"
      )}
    >
      <div
        className="fixed inset-0 bg-black/50"
        onClick={onClose}
      />
      <div className="fixed inset-0 flex items-center justify-center">
        <div
          className={cn(
            "bg-white dark:bg-gray-800 p-6 rounded-lg w-full max-w-md transform transition-all duration-200",
            isAnimating
              ? "translate-y-0 opacity-100"
              : "translate-y-4 opacity-0",
            className
          )}
        >
          {children}
        </div>
      </div>
    </div>
  )
} 