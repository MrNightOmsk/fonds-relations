import { screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { CreatePersonModal } from '../create-person-modal'
import { vi } from 'vitest'
import { renderWithProviders } from '@/test/test-utils'

describe('CreatePersonModal', () => {
  const mockOnClose = vi.fn()
  const mockOnSuccess = vi.fn()

  beforeEach(() => {
    mockOnClose.mockClear()
    mockOnSuccess.mockClear()
  })

  it('renders correctly when open', () => {
    renderWithProviders(
      <CreatePersonModal
        isOpen={true}
        onClose={mockOnClose}
        onSuccess={mockOnSuccess}
      />
    )

    expect(screen.getByText('Создать новую персону')).toBeInTheDocument()
    expect(screen.getByLabelText('Фамилия')).toBeInTheDocument()
    expect(screen.getByLabelText('Имя')).toBeInTheDocument()
    expect(screen.getByLabelText('Отчество')).toBeInTheDocument()
    expect(screen.getByLabelText('Email')).toBeInTheDocument()
    expect(screen.getByLabelText('Телефон')).toBeInTheDocument()
  })

  it('validates required fields', async () => {
    renderWithProviders(
      <CreatePersonModal
        isOpen={true}
        onClose={mockOnClose}
        onSuccess={mockOnSuccess}
      />
    )

    const submitButton = screen.getByText('Создать')
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText('Фамилия не может быть пустой')).toBeInTheDocument()
    })
  })

  it('submits form with valid data', async () => {
    const user = userEvent.setup()
    
    renderWithProviders(
      <CreatePersonModal
        isOpen={true}
        onClose={mockOnClose}
        onSuccess={mockOnSuccess}
      />
    )

    await user.type(screen.getByLabelText('Фамилия'), 'Иванов')
    await user.type(screen.getByLabelText('Имя'), 'Иван')
    await user.type(screen.getByLabelText('Отчество'), 'Иванович')
    await user.type(screen.getByLabelText('Email'), 'ivan@example.com')
    await user.type(screen.getByLabelText('Телефон'), '+7 (999) 999-99-99')

    const submitButton = screen.getByText('Создать')
    await user.click(submitButton)

    await waitFor(() => {
      expect(mockOnSuccess).toHaveBeenCalled()
      expect(mockOnClose).toHaveBeenCalled()
    })
  })

  it('shows confirmation dialog when closing with unsaved changes', async () => {
    const user = userEvent.setup()
    
    renderWithProviders(
      <CreatePersonModal
        isOpen={true}
        onClose={mockOnClose}
        onSuccess={mockOnSuccess}
      />
    )

    await user.type(screen.getByLabelText('Фамилия'), 'Иванов')
    
    const cancelButton = screen.getByText('Отмена')
    await user.click(cancelButton)

    expect(screen.getByText('У вас есть несохраненные изменения. Вы уверены, что хотите закрыть форму?')).toBeInTheDocument()
    expect(mockOnClose).not.toHaveBeenCalled()

    const confirmButton = screen.getByText('Закрыть')
    await user.click(confirmButton)

    expect(mockOnClose).toHaveBeenCalled()
  })
}) 