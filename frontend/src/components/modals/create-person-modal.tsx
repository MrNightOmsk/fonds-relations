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

interface CreatePersonModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: () => void
}

export function CreatePersonModal({
  isOpen,
  onClose,
  onSuccess,
}: CreatePersonModalProps) {
  const [firstName, setFirstName] = useState("")
  const [lastName, setLastName] = useState("")
  const [middleName, setMiddleName] = useState("")
  const [email, setEmail] = useState("")
  const [phone, setPhone] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isConfirmDialogOpen, setIsConfirmDialogOpen] = useState(false)
  const { toast } = useToast()
  const inputRef = useFocus<HTMLInputElement>()
  const { getSignal, abort } = useAbort()

  const hasUnsavedChanges =
    firstName.trim() !== "" ||
    lastName.trim() !== "" ||
    middleName.trim() !== "" ||
    email.trim() !== "" ||
    phone.trim() !== ""

  useBeforeUnload(isOpen && hasUnsavedChanges)

  const handleClose = () => {
    if (hasUnsavedChanges) {
      setIsConfirmDialogOpen(true)
    } else {
      onClose()
    }
  }

  const handleConfirmClose = () => {
    setFirstName("")
    setLastName("")
    setMiddleName("")
    setEmail("")
    setPhone("")
    onClose()
  }

  const handleSubmit = useCallback(async () => {
    if (!lastName.trim()) {
      toast({
        variant: "destructive",
        title: "Ошибка",
        description: "Фамилия не может быть пустой",
      })
      return
    }

    if (!firstName.trim()) {
      toast({
        variant: "destructive",
        title: "Ошибка",
        description: "Имя не может быть пустым",
      })
      return
    }

    try {
      setIsLoading(true)
      await api.persons.create({
        first_name: firstName,
        last_name: lastName,
        middle_name: middleName,
        email,
        phone,
      }, getSignal())
      onSuccess()
      onClose()
    } catch (error) {
      if (error instanceof Error && error.name === "AbortError") {
        return
      }
      console.error("Ошибка при создании персоны:", error)
      toast({
        variant: "destructive",
        title: "Ошибка",
        description: "Не удалось создать персону",
      })
    } finally {
      setIsLoading(false)
    }
  }, [firstName, lastName, middleName, email, phone, onSuccess, onClose, toast, getSignal])

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
        <h2 className="text-2xl font-bold mb-4">Создать новую персону</h2>
        <form onSubmit={onSubmit}>
          <div className="space-y-4">
            <div>
              <label htmlFor="lastName" className="block text-sm font-medium mb-1">
                Фамилия
              </label>
              <Input
                id="lastName"
                ref={inputRef}
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                placeholder="Введите фамилию"
                disabled={isLoading}
              />
            </div>
            <div>
              <label htmlFor="firstName" className="block text-sm font-medium mb-1">
                Имя
              </label>
              <Input
                id="firstName"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                placeholder="Введите имя"
                disabled={isLoading}
              />
            </div>
            <div>
              <label htmlFor="middleName" className="block text-sm font-medium mb-1">
                Отчество
              </label>
              <Input
                id="middleName"
                value={middleName}
                onChange={(e) => setMiddleName(e.target.value)}
                placeholder="Введите отчество"
                disabled={isLoading}
              />
            </div>
            <div>
              <label htmlFor="email" className="block text-sm font-medium mb-1">
                Email
              </label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Введите email"
                disabled={isLoading}
              />
            </div>
            <div>
              <label htmlFor="phone" className="block text-sm font-medium mb-1">
                Телефон
              </label>
              <Input
                id="phone"
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="Введите телефон"
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