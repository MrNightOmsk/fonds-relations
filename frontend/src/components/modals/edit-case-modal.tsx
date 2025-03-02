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

interface Case {
  id: string
  name: string
  description: string
  created_at: string
  updated_at: string
}

interface EditCaseModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: () => void
  caseData: Case
}

export function EditCaseModal({
  isOpen,
  onClose,
  onSuccess,
  caseData,
}: EditCaseModalProps) {
  const [name, setName] = useState(caseData.name)
  const [description, setDescription] = useState(caseData.description)
  const [isLoading, setIsLoading] = useState(false)
  const [isConfirmDialogOpen, setIsConfirmDialogOpen] = useState(false)
  const { toast } = useToast()
  const inputRef = useFocus<HTMLInputElement>()
  const { getSignal, abort } = useAbort()

  useEffect(() => {
    setName(caseData.name)
    setDescription(caseData.description)
  }, [caseData])

  const hasUnsavedChanges =
    name.trim() !== caseData.name.trim() ||
    description.trim() !== caseData.description.trim()

  useBeforeUnload(isOpen && hasUnsavedChanges)

  const handleClose = () => {
    if (hasUnsavedChanges) {
      setIsConfirmDialogOpen(true)
    } else {
      onClose()
    }
  }

  const handleConfirmClose = () => {
    setName(caseData.name)
    setDescription(caseData.description)
    onClose()
  }

  const handleSubmit = useCallback(async () => {
    if (!name.trim()) {
      toast({
        variant: "destructive",
        title: "Ошибка",
        description: "Название дела не может быть пустым",
      })
      return
    }
    try {
      setIsLoading(true)
      await api.cases.update(caseData.id, {
        name,
        description,
      }, getSignal())
      onSuccess()
      onClose()
    } catch (error) {
      if (error instanceof Error && error.name === "AbortError") {
        return
      }
      console.error("Ошибка при обновлении дела:", error)
      toast({
        variant: "destructive",
        title: "Ошибка",
        description: "Не удалось обновить дело",
      })
    } finally {
      setIsLoading(false)
    }
  }, [name, description, caseData.id, onSuccess, onClose, toast, getSignal])

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
        <h2 className="text-2xl font-bold mb-4">Редактировать дело</h2>
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
                placeholder="Введите название дела"
                disabled={isLoading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">
                Описание
              </label>
              <Input
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Введите описание дела"
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