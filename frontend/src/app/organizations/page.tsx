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
import { CreateOrganizationModal } from "@/components/modals/create-organization-modal"
import { EditOrganizationModal } from "@/components/modals/edit-organization-modal"
import { DeleteConfirmationModal } from "@/components/modals/delete-confirmation-modal"

interface Organization {
  id: string
  name: string
  inn: string
  address: string
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

export default function OrganizationsPage() {
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [isEditModalOpen, setIsEditModalOpen] = useState(false)
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false)
  const [selectedOrganization, setSelectedOrganization] = useState<Organization | null>(null)
  const [data, setData] = useState<Organization[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isActionLoading, setIsActionLoading] = useState(false)
  const { toast } = useToast()
  const { getSignal, abort } = useAbort()

  const loadData = async () => {
    try {
      setIsLoading(true)
      const organizations = await api.organizations.getAll() as Organization[]
      setData(organizations)
    } catch (error) {
      if (error instanceof Error && error.name === "AbortError") {
        return
      }
      console.error("Ошибка при загрузке данных:", error)
      toast({
        variant: "destructive",
        title: "Ошибка",
        description: "Не удалось загрузить список организаций",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const columns: ColumnDef<Organization>[] = [
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
      accessorKey: "inn",
      header: ({ column }) => {
        return (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            ИНН
            <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        )
      },
    },
    {
      accessorKey: "address",
      header: ({ column }) => {
        return (
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          >
            Адрес
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
          setSelectedOrganization(item)
          setIsEditModalOpen(true)
        }

        const handleDelete = () => {
          setSelectedOrganization(item)
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
    if (selectedOrganization) {
      try {
        setIsActionLoading(true)
        await api.organizations.delete(selectedOrganization.id)
        toast({
          title: "Успешно",
          description: "Организация успешно удалена",
        })
        loadData()
      } catch (error) {
        if (error instanceof Error && error.name === "AbortError") {
          return
        }
        console.error("Ошибка при удалении организации:", error)
        toast({
          variant: "destructive",
          title: "Ошибка",
          description: "Не удалось удалить организацию",
        })
      } finally {
        setIsActionLoading(false)
        setIsDeleteModalOpen(false)
        setSelectedOrganization(null)
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
          <h1 className="text-3xl font-bold">Список организаций</h1>
          <Button onClick={() => setIsCreateModalOpen(true)}>
            Создать новую организацию
          </Button>
        </div>
        <DataTable columns={columns} data={data} searchKey="name" />
        <CreateOrganizationModal
          isOpen={isCreateModalOpen}
          onClose={() => setIsCreateModalOpen(false)}
          onSuccess={() => {
            loadData()
            toast({
              title: "Успешно",
              description: "Новая организация успешно создана",
            })
          }}
        />
        {selectedOrganization && (
          <>
            <EditOrganizationModal
              isOpen={isEditModalOpen}
              onClose={() => {
                setIsEditModalOpen(false)
                setSelectedOrganization(null)
              }}
              onSuccess={() => {
                loadData()
                toast({
                  title: "Успешно",
                  description: "Организация успешно обновлена",
                })
              }}
              organizationData={selectedOrganization}
            />
            <DeleteConfirmationModal
              isOpen={isDeleteModalOpen}
              onClose={() => {
                setIsDeleteModalOpen(false)
                setSelectedOrganization(null)
              }}
              onConfirm={handleConfirmDelete}
              itemName={selectedOrganization.name}
            />
          </>
        )}
      </div>
      <LoadingOverlay isLoading={isActionLoading} />
    </>
  )
} 