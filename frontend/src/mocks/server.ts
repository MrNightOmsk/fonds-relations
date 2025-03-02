import { setupServer } from 'msw/node'
import { handlers } from './handlers'

export const server = setupServer(...handlers)

// Ensure cleanup after tests
process.on('SIGTERM', () => {
  server.close()
}) 