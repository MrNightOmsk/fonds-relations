const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

async function handleResponse(response: Response) {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || response.statusText)
  }
  return response.json()
}

export const api = {
  cases: {
    getAll: async (signal?: AbortSignal) => {
      const response = await fetch(`${API_URL}/api/cases`, { signal })
      return handleResponse(response)
    },
    create: async (data: any, signal?: AbortSignal) => {
      const response = await fetch(`${API_URL}/api/cases`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
        signal,
      })
      return handleResponse(response)
    },
    update: async (id: string, data: any, signal?: AbortSignal) => {
      const response = await fetch(`${API_URL}/api/cases/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
        signal,
      })
      return handleResponse(response)
    },
    delete: async (id: string, signal?: AbortSignal) => {
      const response = await fetch(`${API_URL}/api/cases/${id}`, {
        method: "DELETE",
        signal,
      })
      return handleResponse(response)
    },
  },
} 