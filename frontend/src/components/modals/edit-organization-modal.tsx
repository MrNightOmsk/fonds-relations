"use client"

import { useState, useEffect, useCallback } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Modal } from "@/components/ui/modal"
import { api } from "@/lib/api"
import { useToast } from "@/hooks/use-toast"
import { useFocus } from "@/hooks/use-focus"
import { useEnter } from "@/hooks/use-enter"
import { useBeforeUnload } from "@/hooks/use-before-unload"
import { useAbort } from "@/hooks/use-abort"
import { LoadingOverlay } from "@/components/ui/loading-overlay"
import { ConfirmationDialog } from "@/components/modals/confirmation-dialog"

interface Organization {
  id: string
  name: string
  inn: string
  address: string
  created_at: string
  updated_at: string
}

interface EditOrganizationModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: () => void
  organizationData: Organization
}

export function EditOrganizationModal({
  isOpen,
  onClose,
  onSuccess,
  organizationData,
}: EditOrganizationModalProps) {
  const [name, setName] = useState(organizationData.name)
  const [inn, setInn] = useState(organizationData.inn)
  const [address, setAddress] = useState(organizationData.address)
  const [isLoading, setIsLoading] = useState(false)
  const [isConfirmDialogOpen, setIsConfirmDialogOpen] = useState(false)
  const { toast } = useToast()
  const inputRef = useFocus<HTMLInputElement>()
  const { getSignal, abort } = useAbort()

  useEffect(() => {
    setName(organizationData.name)
    setInn(organizationData.inn)
    setAddress(organizationData.address)
  }, [organizationData])

  const hasUnsavedChanges =
    name.trim() !== organizationData.name.trim() ||
    inn.trim() !== organizationData.inn.trim() ||
    address.trim() !== organizationData.address.trim()

  useBeforeUnload(isOpen && hasUnsavedChanges)

  const handleClose = () => {
    if (hasUnsavedChanges) {
      setIsConfirmDialogOpen(true)
    } else {
      onClose()
    }
  }

  const handleConfirmClose = () => {
    setName(organizationData.name)
    setInn(organizationData.inn)
    setAddress(organizationData.address)
    onClose()
  }

  const handleSubmit = useCallback(async () => {
    if (!name.trim()) {
      toast({
        variant: "destructive",
        title: "Ошибка",
        description: "Название организации не может быть пустым",
      })
      return
    }

    if (!inn.trim()) {
      toast({
        variant: "destructive",
        title: "Ошибка",
        description: "ИНН организации не может быть пустым",
      })
      return
    }

    try {
      setIsLoading(true)
      await api.organizations.update(organizationData.id, {
        name,
        inn,
        address,
      }, getSignal())
      onSuccess()
      onClose()
    } catch (error) {
      if (error instanceof Error && error.name === "AbortError") {
        return
      }
      console.error("Ошибка при обновлении организации:", error)
      toast({
        variant: "destructive",
        title: "Ошибка",
        description: "Не удалось обновить организацию",
      })
    } finally {
      setIsLoading(false)
    }
  }, [name, inn, address, organizationData.id, onSuccess, onClose, toast, getSignal])

  useEnter(() => {
    if (!isLoading && !isConfirmDialogOpen) {
      handleSubmit()
    }
  })

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await handleSubmit()
  }

  useEffect(() => {
    return () => {
      abort()
    }
  }, [abort])

  return (
    <>
      <Modal isOpen={isOpen} onClose={handleClose}>
        <h2 className="text-2xl font-bold mb-4">Редактировать организацию</h2>
        <form onSubmit={onSubmit}>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">
                Название
              </label>
              <Input
                ref={inputRef}
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Введите название организации"
                disabled={isLoading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">
                ИНН
              </label>
              <Input
                value={inn}
                onChange={(e) => setInn(e.target.value)}
                placeholder="Введите ИНН организации"
                disabled={isLoading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">
                Адрес
              </label>
              <Input
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                placeholder="Введите адрес организации"
                disabled={isLoading}
              />
            </div>
          </div>
          <div className="flex justify-end space-x-2 mt-6">
            <Button
              type="button"
              variant="outline"
              onClick={handleClose}
              disabled={isLoading}
            >
              Отмена
            </Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? "Сохранение..." : "Сохранить"}
            </Button>
          </div>
        </form>
      </Modal>
      <ConfirmationDialog
        isOpen={isConfirmDialogOpen}
        onClose={() => setIsConfirmDialogOpen(false)}
        onConfirm={handleConfirmClose}
        title="Подтверждение"
        description="У вас есть несохраненные изменения. Вы уверены, что хотите закрыть форму?"
        confirmText="Закрыть"
        cancelText="Продолжить редактирование"
      />
      <LoadingOverlay isLoading={isLoading} />
    </>
  )
} 