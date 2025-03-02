const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

interface FetchOptions extends RequestInit {
  signal?: AbortSignal
}

async function fetchWithTimeout(
  url: string,
  options: FetchOptions = {}
): Promise<Response> {
  const { signal, ...restOptions } = options
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), 10000) // 10 seconds timeout

  try {
    const response = await fetch(url, {
      ...restOptions,
      signal: signal || controller.signal,
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response
  } finally {
    clearTimeout(timeoutId)
  }
}

export const api = {
  async fetch<T>(
    endpoint: string,
    options: FetchOptions = {}
  ): Promise<T> {
    const response = await fetchWithTimeout(`${API_URL}${endpoint}`, options)
    if (response.status === 204) {
      return undefined as T
    }
    return response.json()
  },

  // Методы для работы с API
  cases: {
    async getAll(signal?: AbortSignal) {
      return api.fetch("/cases", { signal })
    },

    async getById(id: string, signal?: AbortSignal) {
      return api.fetch(`/cases/${id}`, { signal })
    },

    async create(data: any, signal?: AbortSignal) {
      return api.fetch("/cases", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
        signal,
      })
    },

    async update(id: string, data: any, signal?: AbortSignal) {
      return api.fetch(`/cases/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
        signal,
      })
    },

    async delete(id: string, signal?: AbortSignal) {
      return api.fetch(`/cases/${id}`, {
        method: "DELETE",
        signal,
      })
    },
  },

  persons: {
    async getAll(signal?: AbortSignal) {
      return api.fetch("/persons", { signal })
    },

    async getById(id: string, signal?: AbortSignal) {
      return api.fetch(`/persons/${id}`, { signal })
    },

    async create(data: any, signal?: AbortSignal) {
      return api.fetch("/persons", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
        signal,
      })
    },

    async update(id: string, data: any, signal?: AbortSignal) {
      return api.fetch(`/persons/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
        signal,
      })
    },

    async delete(id: string, signal?: AbortSignal) {
      return api.fetch(`/persons/${id}`, {
        method: "DELETE",
        signal,
      })
    },
  },

  organizations: {
    async getAll(signal?: AbortSignal) {
      return api.fetch("/organizations", { signal })
    },

    async getById(id: string, signal?: AbortSignal) {
      return api.fetch(`/organizations/${id}`, { signal })
    },

    async create(data: any, signal?: AbortSignal) {
      return api.fetch("/organizations", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
        signal,
      })
    },

    async update(id: string, data: any, signal?: AbortSignal) {
      return api.fetch(`/organizations/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
        signal,
      })
    },

    async delete(id: string, signal?: AbortSignal) {
      return api.fetch(`/organizations/${id}`, {
        method: "DELETE",
        signal,
      })
    },
  },
} 