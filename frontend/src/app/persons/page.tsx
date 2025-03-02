"use client"

import { useState, useEffect } from "react"
import { DataTable } from "@/components/ui/data-table"
import { ColumnDef } from "@tanstack/react-table"
import { api } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { LoadingSpinner } from "@/components/ui/loading-spinner"
import { LoadingOverlay } from "@/components/ui/loading-overlay"
import { useToast } from "@/hooks/use-toast"
import { useAbort } from "@/hooks/use-abort"
import { MoreHorizontal, ArrowUpDown } from "lucide-react"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { CreatePersonModal } from "@/components/modals/create-person-modal"
import { EditPersonModal } from "@/components/modals/edit-person-modal"
import { DeleteConfirmationModal } from "@/components/modals/delete-confirmation-modal"

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

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat("ru", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date)
}

export default function PersonsPage() {
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [isEditModalOpen, setIsEditModalOpen] = useState(false)
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false)
  const [selectedPerson, setSelectedPerson] = useState<Person | null>(null)
  const [data, setData] = useState<Person[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isActionLoading, setIsActionLoading] = useState(false)
  const { toast } = useToast()
  const { getSignal, abort } = useAbort()

  const loadData = async () => {
    try {
      setIsLoading(true)
      const persons = await api.persons.getAll(getSignal()) as Person[]
      setData(persons)
    } catch (error) {
      if (error instanceof Error && error.name === "AbortError") {
        return
      }
      console.error("Ошибка при загрузке данных:", error)
      toast({
        variant: "destructive",
        title: "Ошибка",
        description: "Не удалось загрузить список персон",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const columns: ColumnDef<Person>[] = [
    {
      accessorKey: "last_name",
      header: ({ column }) => {
        return (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Фамилия
            <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        )
      },
    },
    {
      accessorKey: "first_name",
      header: ({ column }) => {
        return (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Имя
            <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        )
      },
    },
    {
      accessorKey: "middle_name",
      header: ({ column }) => {
        return (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Отчество
            <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        )
      },
    },
    {
      accessorKey: "email",
      header: ({ column }) => {
        return (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Email
            <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        )
      },
    },
    {
      accessorKey: "phone",
      header: ({ column }) => {
        return (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Телефон
            <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        )
      },
    },
    {
      accessorKey: "created_at",
      header: ({ column }) => {
        return (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Создано
            <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        )
      },
      cell: ({ row }) => formatDate(row.original.created_at),
    },
    {
      accessorKey: "updated_at",
      header: ({ column }) => {
        return (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Обновлено
            <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        )
      },
      cell: ({ row }) => formatDate(row.original.updated_at),
    },
    {
      id: "actions",
      cell: ({ row }) => {
        const item = row.original

        const handleEdit = () => {
          setSelectedPerson(item)
          setIsEditModalOpen(true)
        }

        const handleDelete = () => {
          setSelectedPerson(item)
          setIsDeleteModalOpen(true)
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
      },
    },
  ]

  const handleConfirmDelete = async () => {
    if (selectedPerson) {
      try {
        setIsActionLoading(true)
        await api.persons.delete(selectedPerson.id, getSignal())
        toast({
          title: "Успешно",
          description: "Персона успешно удалена",
        })
        loadData()
      } catch (error) {
        if (error instanceof Error && error.name === "AbortError") {
          return
        }
        console.error("Ошибка при удалении персоны:", error)
        toast({
          variant: "destructive",
          title: "Ошибка",
          description: "Не удалось удалить персону",
        })
      } finally {
        setIsActionLoading(false)
        setIsDeleteModalOpen(false)
        setSelectedPerson(null)
      }
    }
  }

  useEffect(() => {
    loadData()
    return () => {
      abort()
    }
  }, [abort])

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <LoadingSpinner className="h-8 w-8" />
      </div>
    )
  }

  return (
    <>
      <div className="container mx-auto py-10">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-3xl font-bold">Список персон</h1>
          <Button onClick={() => setIsCreateModalOpen(true)}>
            Создать новую персону
          </Button>
        </div>
        <DataTable columns={columns} data={data} searchKey="last_name" />
        <CreatePersonModal
          isOpen={isCreateModalOpen}
          onClose={() => setIsCreateModalOpen(false)}
          onSuccess={() => {
            loadData()
            toast({
              title: "Успешно",
              description: "Новая персона успешно создана",
            })
          }}
        />
        {selectedPerson && (
          <>
            <EditPersonModal
              isOpen={isEditModalOpen}
              onClose={() => {
                setIsEditModalOpen(false)
                setSelectedPerson(null)
              }}
              onSuccess={() => {
                loadData()
                toast({
                  title: "Успешно",
                  description: "Персона успешно обновлена",
                })
              }}
              personData={selectedPerson}
            />
            <DeleteConfirmationModal
              isOpen={isDeleteModalOpen}
              onClose={() => {
                setIsDeleteModalOpen(false)
                setSelectedPerson(null)
              }}
              onConfirm={handleConfirmDelete}
              itemName={`${selectedPerson.last_name} ${selectedPerson.first_name}`}
            />
          </>
        )}
      </div>
      <LoadingOverlay isLoading={isActionLoading} />
    </>
  )
} 