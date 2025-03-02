"use client"

import { useState, useEffect } from "react"
import { DataTable } from "@/components/ui/data-table"
import { ColumnDef } from "@tanstack/react-table"
import { api } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { CreateCaseModal } from "@/components/modals/create-case-modal"
import { EditCaseModal } from "@/components/modals/edit-case-modal"
import { DeleteConfirmationModal } from "@/components/modals/delete-confirmation-modal"
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

interface Case {
  id: string
  name: string
  description: string
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

export default function Home() {
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [isEditModalOpen, setIsEditModalOpen] = useState(false)
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false)
  const [selectedCase, setSelectedCase] = useState<Case | null>(null)
  const [data, setData] = useState<Case[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isActionLoading, setIsActionLoading] = useState(false)
  const { toast } = useToast()
  const { getSignal, abort } = useAbort()

  const loadData = async () => {
    try {
      setIsLoading(true)
      const cases = await api.cases.getAll(getSignal()) as Case[]
      setData(cases)
    } catch (error) {
      if (error instanceof Error && error.name === "AbortError") {
        return
      }
      console.error("Ошибка при загрузке данных:", error)
      toast({
        variant: "destructive",
        title: "Ошибка",
        description: "Не удалось загрузить список дел",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const columns: ColumnDef<Case>[] = [
    {
      accessorKey: "name",
      header: ({ column }) => {
        return (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Название
            <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        )
      },
    },
    {
      accessorKey: "description",
      header: ({ column }) => {
        return (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Описание
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
          setSelectedCase(item)
          setIsEditModalOpen(true)
        }

        const handleDelete = () => {
          setSelectedCase(item)
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
    if (selectedCase) {
      try {
        setIsActionLoading(true)
        await api.cases.delete(selectedCase.id, getSignal())
        toast({
          title: "Успешно",
          description: "Дело успешно удалено",
        })
        loadData()
      } catch (error) {
        if (error instanceof Error && error.name === "AbortError") {
          return
        }
        console.error("Ошибка при удалении дела:", error)
        toast({
          variant: "destructive",
          title: "Ошибка",
          description: "Не удалось удалить дело",
        })
      } finally {
        setIsActionLoading(false)
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
          <h1 className="text-3xl font-bold">Список дел</h1>
          <Button onClick={() => setIsCreateModalOpen(true)}>
            Создать новое дело
          </Button>
        </div>
        <DataTable columns={columns} data={data} searchKey="name" />
        <CreateCaseModal
          isOpen={isCreateModalOpen}
          onClose={() => setIsCreateModalOpen(false)}
          onSuccess={() => {
            loadData()
            toast({
              title: "Успешно",
              description: "Новое дело успешно создано",
            })
          }}
        />
        {selectedCase && (
          <>
            <EditCaseModal
              isOpen={isEditModalOpen}
              onClose={() => {
                setIsEditModalOpen(false)
                setSelectedCase(null)
              }}
              onSuccess={() => {
                loadData()
                toast({
                  title: "Успешно",
                  description: "Дело успешно обновлено",
                })
              }}
              caseData={selectedCase}
            />
            <DeleteConfirmationModal
              isOpen={isDeleteModalOpen}
              onClose={() => {
                setIsDeleteModalOpen(false)
                setSelectedCase(null)
              }}
              onConfirm={handleConfirmDelete}
              isLoading={isActionLoading}
              itemName={selectedCase.name}
            />
          </>
        )}
      </div>
    </>
  )
} 