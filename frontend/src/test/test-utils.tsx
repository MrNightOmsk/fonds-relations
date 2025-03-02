import { render } from '@testing-library/react'
import { Toaster } from '@/components/ui/toaster'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import React from 'react'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
})

function Providers({ children }: { children: React.ReactNode }) {
  return (
    <React.StrictMode>
      <QueryClientProvider client={queryClient}>
        <React.Suspense fallback={<div>Loading...</div>}>
          {children}
          <Toaster />
        </React.Suspense>
      </QueryClientProvider>
    </React.StrictMode>
  )
}

export function renderWithProviders(ui: React.ReactElement) {
  return render(ui, { wrapper: Providers })
} 