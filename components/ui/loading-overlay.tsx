import { LoadingSpinner } from "./loading-spinner"

export function LoadingOverlay() {
  return (
    <div className="absolute inset-0 flex items-center justify-center bg-background/80">
      <LoadingSpinner className="h-8 w-8" />
    </div>
  )
} 