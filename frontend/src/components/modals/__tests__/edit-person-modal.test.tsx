import { screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { EditPersonModal } from '../edit-person-modal'
import { vi } from 'vitest'
import { renderWithProviders } from '@/test/test-utils'

describe('EditPersonModal', () => {
  const mockOnClose = vi.fn()
  const mockOnSuccess = vi.fn()
  const mockPersonData = {
    id: '1',
    first_name: 'Иван',
    last_name: 'Иванов',
    middle_name: 'Иванович',
    email: 'ivan@example.com',
    phone: '+7 (999) 999-99-99',
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z'
  }

  beforeEach(() => {
    mockOnClose.mockClear()
    mockOnSuccess.mockClear()
  })

  it('renders correctly when open', () => {
    renderWithProviders(
      <EditPersonModal
        isOpen={true}
        onClose={mockOnClose}
        onSuccess={mockOnSuccess}
        personData={mockPersonData}
      />
    )

    expect(screen.getByText('Редактировать персону')).toBeInTheDocument()
    expect(screen.getByLabelText('Фамилия')).toHaveValue('Иванов')
    expect(screen.getByLabelText('Имя')).toHaveValue('Иван')
    expect(screen.getByLabelText('Отчество')).toHaveValue('Иванович')
    expect(screen.getByLabelText('Email')).toHaveValue('ivan@example.com')
    expect(screen.getByLabelText('Телефон')).toHaveValue('+7 (999) 999-99-99')
  })

  it('validates required fields', async () => {
    renderWithProviders(
      <EditPersonModal
        isOpen={true}
        onClose={mockOnClose}
        onSuccess={mockOnSuccess}
        personData={mockPersonData}
      />
    )

    const lastNameInput = screen.getByLabelText('Фамилия')
    fireEvent.change(lastNameInput, { target: { value: '' } })

    const submitButton = screen.getByText('Сохранить')
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText('Фамилия не может быть пустой')).toBeInTheDocument()
    })
  })

  it('submits form with valid data', async () => {
    const user = userEvent.setup()
    
    renderWithProviders(
      <EditPersonModal
        isOpen={true}
        onClose={mockOnClose}
        onSuccess={mockOnSuccess}
        personData={mockPersonData}
      />
    )

    await user.clear(screen.getByLabelText('Фамилия'))
    await user.type(screen.getByLabelText('Фамилия'), 'Петров')

    const submitButton = screen.getByText('Сохранить')
    await user.click(submitButton)

    await waitFor(() => {
      expect(mockOnSuccess).toHaveBeenCalled()
      expect(mockOnClose).toHaveBeenCalled()
    })
  })

  it('shows confirmation dialog when closing with unsaved changes', async () => {
    const user = userEvent.setup()
    
    renderWithProviders(
      <EditPersonModal
        isOpen={true}
        onClose={mockOnClose}
        onSuccess={mockOnSuccess}
        personData={mockPersonData}
      />
    )

    await user.clear(screen.getByLabelText('Фамилия'))
    await user.type(screen.getByLabelText('Фамилия'), 'Петров')
    
    const cancelButton = screen.getByText('Отмена')
    await user.click(cancelButton)

    expect(screen.getByText('У вас есть несохраненные изменения. Вы уверены, что хотите закрыть форму?')).toBeInTheDocument()
    expect(mockOnClose).not.toHaveBeenCalled()

    const confirmButton = screen.getByText('Закрыть')
    await user.click(confirmButton)

    expect(mockOnClose).toHaveBeenCalled()
  })
}) 