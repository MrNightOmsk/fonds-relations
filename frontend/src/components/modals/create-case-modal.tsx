"use client"

import { useState, useCallback, useEffect } from "react"
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

interface CreateCaseModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: () => void
}

export function CreateCaseModal({
  isOpen,
  onClose,
  onSuccess,
}: CreateCaseModalProps) {
  const [name, setName] = useState("")
  const [description, setDescription] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isConfirmDialogOpen, setIsConfirmDialogOpen] = useState(false)
  const { toast } = useToast()
  const inputRef = useFocus<HTMLInputElement>()
  const { getSignal, abort } = useAbort()

  const hasUnsavedChanges = name.trim() !== "" || description.trim() !== ""

  useBeforeUnload(isOpen && hasUnsavedChanges)

  const handleClose = () => {
    if (hasUnsavedChanges) {
      setIsConfirmDialogOpen(true)
    } else {
      onClose()
    }
  }

  const handleConfirmClose = () => {
    setName("")
    setDescription("")
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
      await api.cases.create({
        name,
        description,
      }, getSignal())
      onSuccess()
      onClose()
    } catch (error) {
      if (error instanceof Error && error.name === "AbortError") {
        return
      }
      console.error("Ошибка при создании дела:", error)
      toast({
        variant: "destructive",
        title: "Ошибка",
        description: "Не удалось создать дело",
      })
    } finally {
      setIsLoading(false)
    }
  }, [name, description, onSuccess, onClose, toast, getSignal])

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
        <h2 className="text-2xl font-bold mb-4">Создать новое дело</h2>
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
              {isLoading ? "Создание..." : "Создать"}
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