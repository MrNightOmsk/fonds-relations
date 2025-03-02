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

interface EditPersonModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: () => void
  personData: Person
}

export function EditPersonModal({
  isOpen,
  onClose,
  onSuccess,
  personData,
}: EditPersonModalProps) {
  const [firstName, setFirstName] = useState(personData.first_name)
  const [lastName, setLastName] = useState(personData.last_name)
  const [middleName, setMiddleName] = useState(personData.middle_name)
  const [email, setEmail] = useState(personData.email)
  const [phone, setPhone] = useState(personData.phone)
  const [isLoading, setIsLoading] = useState(false)
  const [isConfirmDialogOpen, setIsConfirmDialogOpen] = useState(false)
  const { toast } = useToast()
  const inputRef = useFocus<HTMLInputElement>()
  const { getSignal, abort } = useAbort()

  useEffect(() => {
    setFirstName(personData.first_name)
    setLastName(personData.last_name)
    setMiddleName(personData.middle_name)
    setEmail(personData.email)
    setPhone(personData.phone)
  }, [personData])

  const hasUnsavedChanges =
    firstName.trim() !== personData.first_name.trim() ||
    lastName.trim() !== personData.last_name.trim() ||
    middleName.trim() !== personData.middle_name.trim() ||
    email.trim() !== personData.email.trim() ||
    phone.trim() !== personData.phone.trim()

  useBeforeUnload(isOpen && hasUnsavedChanges)

  const handleClose = () => {
    if (hasUnsavedChanges) {
      setIsConfirmDialogOpen(true)
    } else {
      onClose()
    }
  }

  const handleConfirmClose = () => {
    setFirstName(personData.first_name)
    setLastName(personData.last_name)
    setMiddleName(personData.middle_name)
    setEmail(personData.email)
    setPhone(personData.phone)
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
      await api.persons.update(personData.id, {
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
      console.error("Ошибка при обновлении персоны:", error)
      toast({
        variant: "destructive",
        title: "Ошибка",
        description: "Не удалось обновить персону",
      })
    } finally {
      setIsLoading(false)
    }
  }, [firstName, lastName, middleName, email, phone, personData.id, onSuccess, onClose, toast, getSignal])

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
        <h2 className="text-2xl font-bold mb-4">Редактировать персону</h2>
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