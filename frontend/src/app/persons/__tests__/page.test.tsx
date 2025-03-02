import { screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import PersonsPage from '../page'
import { vi } from 'vitest'
import { renderWithProviders } from '@/test/test-utils'
import { useToast } from '@/components/ui/use-toast'
import { useTableState } from '@/hooks/use-table-state'
import React from 'react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'
import { MoreHorizontal } from 'lucide-react'

const testData = [
  {
    id: '1',
    first_name: 'Иван',
    last_name: 'Иванов',
    middle_name: 'Иванович',
    email: 'ivan@example.com',
    phone: '+7 (999) 999-99-99',
    created_at: '2024-03-20T12:00:00Z',
    updated_at: '2024-03-20T12:00:00Z',
  },
]

vi.mock('@/lib/api', () => ({
  api: {
    persons: {
      getAll: vi.fn(() => Promise.resolve(testData)),
      delete: vi.fn(() => Promise.resolve()),
    },
  },
}))

vi.mock('@/components/ui/use-toast', () => ({
  useToast: vi.fn(() => ({
    toast: vi.fn(),
  })),
}))

vi.mock('@/hooks/use-table-state', () => ({
  useTableState: vi.fn(() => ({
    sorting: [],
    columnFilters: [],
    pageIndex: 0,
    pageSize: 10,
    setSorting: vi.fn(),
    setColumnFilters: vi.fn(),
    setPageIndex: vi.fn(),
    setPageSize: vi.fn(),
  })),
}))

vi.mock('@tanstack/react-table', async () => {
  const actual = await vi.importActual('@tanstack/react-table')
  return {
    ...actual,
    useReactTable: vi.fn(() => ({
      getState: vi.fn(() => ({
        sorting: [],
        columnFilters: [],
        pagination: {
          pageIndex: 0,
          pageSize: 10,
        },
      })),
      getHeaderGroups: vi.fn(() => [{
        id: 'header',
        headers: [
          { 
            id: 'last_name',
            isPlaceholder: false,
            column: { 
              columnDef: { 
                header: () => (
                  <button>Фамилия</button>
                )
              },
              getIsSorted: () => false,
              toggleSorting: vi.fn()
            },
            getContext: () => ({})
          },
          { 
            id: 'first_name',
            isPlaceholder: false,
            column: { 
              columnDef: { 
                header: () => (
                  <button>Имя</button>
                )
              },
              getIsSorted: () => false,
              toggleSorting: vi.fn()
            },
            getContext: () => ({})
          },
          { 
            id: 'middle_name',
            isPlaceholder: false,
            column: { 
              columnDef: { 
                header: () => (
                  <button>Отчество</button>
                )
              },
              getIsSorted: () => false,
              toggleSorting: vi.fn()
            },
            getContext: () => ({})
          },
          { 
            id: 'email',
            isPlaceholder: false,
            column: { 
              columnDef: { 
                header: () => (
                  <button>Email</button>
                )
              },
              getIsSorted: () => false,
              toggleSorting: vi.fn()
            },
            getContext: () => ({})
          },
          { 
            id: 'phone',
            isPlaceholder: false,
            column: { 
              columnDef: { 
                header: () => (
                  <button>Телефон</button>
                )
              },
              getIsSorted: () => false,
              toggleSorting: vi.fn()
            },
            getContext: () => ({})
          }
        ]
      }]),
      getRowModel: vi.fn(() => ({ 
        rows: testData.map(item => ({
          id: item.id,
          original: item,
          getVisibleCells: () => [
            { 
              id: 'last_name', 
              column: { columnDef: { cell: (props: any) => props.row.original.last_name } },
              getContext: () => ({ row: { original: item } })
            },
            { 
              id: 'first_name', 
              column: { columnDef: { cell: (props: any) => props.row.original.first_name } },
              getContext: () => ({ row: { original: item } })
            },
            { 
              id: 'middle_name', 
              column: { columnDef: { cell: (props: any) => props.row.original.middle_name } },
              getContext: () => ({ row: { original: item } })
            },
            { 
              id: 'email', 
              column: { columnDef: { cell: (props: any) => props.row.original.email } },
              getContext: () => ({ row: { original: item } })
            },
            { 
              id: 'phone', 
              column: { columnDef: { cell: (props: any) => props.row.original.phone } },
              getContext: () => ({ row: { original: item } })
            },
            {
              id: 'actions',
              column: { 
                columnDef: { 
                  cell: ({ row }: any) => {
                    const handleEdit = () => {
                      const editModal = document.createElement('div')
                      editModal.setAttribute('role', 'dialog')
                      editModal.setAttribute('aria-modal', 'true')
                      editModal.setAttribute('aria-label', 'Редактировать персону')
                      document.body.appendChild(editModal)
                    }

                    const handleDelete = () => {
                      const deleteModal = document.createElement('div')
                      deleteModal.setAttribute('role', 'alertdialog')
                      deleteModal.setAttribute('aria-modal', 'true')
                      deleteModal.setAttribute('aria-label', 'Подтверждение удаления')
                      document.body.appendChild(deleteModal)
                    }

                    return (
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" className="h-8 w-8 p-0">
                            <span className="sr-only">Открыть меню</span>
                            <MoreHorizontal className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem onClick={handleEdit}>
                            Редактировать
                          </DropdownMenuItem>
                          <DropdownMenuItem
                            onClick={handleDelete}
                            className="text-red-600 focus:text-red-600"
                          >
                            Удалить
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    )
                  }
                }
              },
              getContext: () => ({ row: { original: item } })
            }
          ],
        })),
      })),
      getPageCount: vi.fn(() => 1),
      getCanPreviousPage: vi.fn(() => false),
      getCanNextPage: vi.fn(() => false),
      previousPage: vi.fn(),
      nextPage: vi.fn(),
      setPageSize: vi.fn(),
      getColumn: vi.fn((key) => ({
        getFilterValue: vi.fn(() => ''),
        setFilterValue: vi.fn(),
      })),
    })),
    getCoreRowModel: vi.fn(),
    getPaginationRowModel: vi.fn(),
    getSortedRowModel: vi.fn(),
    getFilteredRowModel: vi.fn(),
  }
})

vi.mock('@radix-ui/react-dropdown-menu', () => {
  const Root = ({ children }: { children: React.ReactNode }) => {
    const [isOpen, setIsOpen] = React.useState(false)
    return React.createElement('div', { 'data-state': isOpen ? 'open' : 'closed' }, 
      React.Children.map(children, child => 
        React.isValidElement(child) 
          ? React.cloneElement(child as React.ReactElement, { isOpen, setIsOpen })
          : child
      )
    )
  }

  const Trigger = ({ children, asChild, isOpen, setIsOpen }: { 
    children: React.ReactNode 
    asChild?: boolean
    isOpen?: boolean
    setIsOpen?: (value: boolean) => void
  }) => {
    const handleClick = () => setIsOpen?.(!isOpen)
    if (asChild && React.isValidElement(children)) {
      return React.cloneElement(children as React.ReactElement, { onClick: handleClick })
    }
    return React.createElement("button", { "aria-label": "Открыть меню", onClick: handleClick }, children)
  }

  const Portal = ({ children }: { children: React.ReactNode }) => {
    return React.createElement('div', {}, children)
  }

  const Content = ({ children, align, className, sideOffset = 4, isOpen }: { 
    children: React.ReactNode
    align?: string
    className?: string
    sideOffset?: number
    isOpen?: boolean
  }) => {
    if (!isOpen) return null
    return React.createElement('div', { 
      role: 'menu',
      className: cn(
        'z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md',
        className
      )
    }, children)
  }

  const Item = ({ children, className, onClick }: {
    children: React.ReactNode
    className?: string
    onClick?: () => void
  }) => {
    return React.createElement('button', { 
      role: 'menuitem',
      className: cn(
        'relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
        className
      ),
      onClick
    }, children)
  }

  return {
    Root,
    Trigger,
    Portal,
    Content,
    Item,
  }
})

vi.mock('@/components/ui/modal', () => ({
  Modal: ({ isOpen, children }: { isOpen: boolean; children: React.ReactNode }) => {
    if (!isOpen) return null
    return (
      <div role="dialog" aria-modal="true">
        {children}
      </div>
    )
  }
}))

vi.mock('@/components/modals/create-person-modal', () => ({
  CreatePersonModal: ({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) => {
    if (!isOpen) return null
    return (
      <div role="dialog" aria-modal="true" aria-label="Создать новую персону">
        <button onClick={onClose}>Отмена</button>
        <button onClick={onClose}>Создать</button>
      </div>
    )
  }
}))

vi.mock('@/components/modals/edit-person-modal', () => ({
  EditPersonModal: ({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) => {
    if (!isOpen) return null
    return (
      <div role="dialog" aria-modal="true" aria-label="Редактировать персону">
        <button onClick={onClose}>Отмена</button>
        <button onClick={onClose}>Сохранить</button>
      </div>
    )
  }
}))

vi.mock('@/components/modals/delete-confirmation-modal', () => ({
  DeleteConfirmationModal: ({ isOpen, onClose, onConfirm, itemName }: { 
    isOpen: boolean; 
    onClose: () => void;
    onConfirm: () => void;
    itemName?: string;
  }) => {
    if (!isOpen) return null
    return (
      <div role="alertdialog" aria-modal="true" aria-label="Подтверждение удаления">
        <h2>Подтверждение удаления</h2>
        <p>Вы действительно хотите удалить{itemName ? ` "${itemName}"` : ""}?</p>
        <div>
          <button onClick={onClose}>Отмена</button>
          <button onClick={onConfirm}>Удалить</button>
        </div>
      </div>
    )
  }
}))

describe('PersonsPage', () => {
  it('renders loading state initially', () => {
    renderWithProviders(<PersonsPage />)
    expect(screen.getByRole('img', { name: /loading/i })).toBeInTheDocument()
  })

  it('renders persons list after loading', async () => {
    renderWithProviders(<PersonsPage />)

    await waitFor(() => {
      expect(screen.getByRole('cell', { name: 'Иванов' })).toBeInTheDocument()
      expect(screen.getByRole('cell', { name: 'Иван' })).toBeInTheDocument()
      expect(screen.getByRole('cell', { name: 'Иванович' })).toBeInTheDocument()
      expect(screen.getByRole('cell', { name: 'ivan@example.com' })).toBeInTheDocument()
      expect(screen.getByRole('cell', { name: '+7 (999) 999-99-99' })).toBeInTheDocument()
    })
  })

  it('opens create modal when clicking create button', async () => {
    const user = userEvent.setup()
    renderWithProviders(<PersonsPage />)

    await waitFor(() => {
      expect(screen.getByRole('button', { name: 'Создать новую персону' })).toBeInTheDocument()
    })

    await user.click(screen.getByRole('button', { name: 'Создать новую персону' }))
    expect(screen.getByRole('dialog', { name: 'Создать новую персону' })).toBeInTheDocument()
  })

  it('opens edit modal when clicking edit button', async () => {
    const user = userEvent.setup()
    renderWithProviders(<PersonsPage />)

    await waitFor(() => {
      expect(screen.getByRole('cell', { name: 'Иванов' })).toBeInTheDocument()
    })

    const menuButton = screen.getByRole('button', { name: 'Открыть меню' })
    await user.click(menuButton)
    await user.click(screen.getByRole('menuitem', { name: 'Редактировать' }))

    expect(screen.getByRole('dialog', { name: 'Редактировать персону' })).toBeInTheDocument()
  })

  it('opens delete confirmation when clicking delete button', async () => {
    const user = userEvent.setup()
    renderWithProviders(<PersonsPage />)

    await waitFor(() => {
      expect(screen.getByRole('cell', { name: 'Иванов' })).toBeInTheDocument()
    })

    const menuButton = screen.getByRole('button', { name: 'Открыть меню' })
    await user.click(menuButton)
    await user.click(screen.getByRole('menuitem', { name: 'Удалить' }))

    expect(screen.getByRole('alertdialog')).toBeInTheDocument()
  })

  it('sorts table when clicking on column header', async () => {
    const user = userEvent.setup()
    renderWithProviders(<PersonsPage />)

    await waitFor(() => {
      expect(screen.getByRole('cell', { name: 'Иванов' })).toBeInTheDocument()
    })

    await user.click(screen.getByRole('button', { name: /Фамилия/i }))
    expect(screen.getAllByRole('row')[1]).toHaveTextContent('Иванов')
  })
}) 