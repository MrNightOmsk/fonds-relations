"use client"

import { LoadingSpinner } from "@/components/ui/loading-spinner"

interface LoadingOverlayProps {
  isLoading: boolean
}

export function LoadingOverlay({ isLoading }: LoadingOverlayProps) {
  if (!isLoading) return null

  return (
    <div className="fixed inset-0 z-50 bg-black/20 backdrop-blur-[1px] flex items-center justify-center">
      <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-lg">
        <LoadingSpinner className="h-8 w-8" />
      </div>
    </div>
  )
} 