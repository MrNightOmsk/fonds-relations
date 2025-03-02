import { api } from '../api'
import { server } from '../../mocks/server'
import { http, HttpResponse } from 'msw'

const API_URL = 'http://localhost:8000/api/v1'

interface Person {
  id: string
  first_name: string
  last_name: string
  middle_name: string
  email: string
  phone: string
  created_at: string
  updated_at: string
}

describe('API Client', () => {
  const mockPerson = {
    first_name: 'Иван',
    last_name: 'Иванов',
    middle_name: 'Иванович',
    email: 'ivan@example.com',
    phone: '+7 (999) 999-99-99',
  }

  describe('persons', () => {
    it('fetches all persons', async () => {
      const response = await api.persons.getAll() as Person[]
      expect(response).toHaveLength(1)
      expect(response[0]).toHaveProperty('id', '1')
    })

    it('creates a new person', async () => {
      const response = await api.persons.create(mockPerson)
      expect(response).toHaveProperty('id', '2')
      expect(response).toMatchObject(mockPerson)
    })

    it('updates a person', async () => {
      const updatedPerson = { ...mockPerson, last_name: 'Петров' }
      const response = await api.persons.update('1', updatedPerson)
      expect(response).toHaveProperty('id', '1')
      expect(response).toMatchObject(updatedPerson)
    })

    it('deletes a person', async () => {
      server.use(
        http.delete(`${API_URL}/persons/1`, () => {
          return HttpResponse.json({}, { status: 204 })
        })
      )
      
      const response = await api.persons.delete('1')
      expect(response).toBeUndefined()
    })

    it('handles network errors', async () => {
      server.use(
        http.get(`${API_URL}/persons`, () => {
          return new HttpResponse(null, { status: 500 })
        })
      )

      await expect(api.persons.getAll()).rejects.toThrow()
    })

    it('handles validation errors', async () => {
      const invalidPerson = { ...mockPerson, email: 'invalid-email' }
      
      server.use(
        http.post(`${API_URL}/persons`, () => {
          return HttpResponse.json(
            { detail: 'Invalid email format' },
            { status: 400 }
          )
        })
      )

      await expect(api.persons.create(invalidPerson)).rejects.toThrow()
    })

    it('handles not found errors', async () => {
      server.use(
        http.get(`${API_URL}/persons/999`, () => {
          return new HttpResponse(null, { status: 404 })
        })
      )

      await expect(api.persons.getById('999')).rejects.toThrow()
    })

    it('supports request cancellation', async () => {
      const controller = new AbortController()
      const promise = api.persons.getAll(controller.signal)
      controller.abort()

      await expect(promise).rejects.toThrow('The operation was aborted.')
    })
  })
}) 