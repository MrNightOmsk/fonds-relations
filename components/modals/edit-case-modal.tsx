"use client"

import { useState, useEffect } from "react"
import { api } from "@/lib/api"
import { useToast } from "@/hooks/use-toast"
import { useAbort } from "@/hooks/use-abort"
import { LoadingOverlay } from "@/components/ui/loading-overlay"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog"

interface Case {
  id: string
  name: string
  description: string
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
  const { toast } = useToast()
  const { getSignal } = useAbort()

  useEffect(() => {
    setName(caseData.name)
    setDescription(caseData.description)
  }, [caseData])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim()) {
      toast({
        variant: "destructive",
        title: "Ошибка",
        description: "Название дела обязательно для заполнения",
      })
      return
    }

    try {
      setIsLoading(true)
      await api.cases.update(
        caseData.id,
        {
          name: name.trim(),
          description: description.trim(),
        },
        getSignal()
      )
      onSuccess()
      handleClose()
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
  }

  const handleClose = () => {
    setName(caseData.name)
    setDescription(caseData.description)
    onClose()
  }

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent>
        {isLoading && <LoadingOverlay />}
        <DialogHeader>
          <DialogTitle>Редактировать дело</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <label htmlFor="name">Название</label>
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Введите название дела"
              />
            </div>
            <div className="grid gap-2">
              <label htmlFor="description">Описание</label>
              <Input
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Введите описание дела"
              />
            </div>
          </div>
          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={handleClose}
              disabled={isLoading}
            >
              Отмена
            </Button>
            <Button type="submit" disabled={isLoading}>
              Сохранить
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
} 