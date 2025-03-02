import { http, HttpResponse } from 'msw'

const API_URL = 'http://localhost:8000/api/v1'

export const handlers = [
  // GET /persons
  http.get(`${API_URL}/persons`, () => {
    return HttpResponse.json([
      {
        id: '1',
        first_name: 'Иван',
        last_name: 'Иванов',
        middle_name: 'Иванович',
        email: 'ivan@example.com',
        phone: '+7 (999) 999-99-99',
        created_at: '2024-03-20T10:00:00Z',
        updated_at: '2024-03-20T10:00:00Z',
      },
    ])
  }),

  // POST /persons
  http.post(`${API_URL}/persons`, async ({ request }) => {
    const body = await request.json()
    return HttpResponse.json({
      id: '2',
      ...body,
      created_at: '2024-03-20T11:00:00Z',
      updated_at: '2024-03-20T11:00:00Z',
    }, { status: 201 })
  }),

  // PUT /persons/:id
  http.put(`${API_URL}/persons/:id`, async ({ params, request }) => {
    const { id } = params
    const body = await request.json()
    return HttpResponse.json({
      id,
      ...body,
      created_at: '2024-03-20T10:00:00Z',
      updated_at: '2024-03-20T12:00:00Z',
    })
  }),

  // DELETE /persons/:id
  http.delete(`${API_URL}/persons/:id`, () => {
    return HttpResponse.json({}, { status: 204 })
  }),
] 