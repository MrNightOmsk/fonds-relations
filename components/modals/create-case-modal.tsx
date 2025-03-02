"use client"

import { useState } from "react"
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
  const { toast } = useToast()
  const { getSignal } = useAbort()

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
      await api.cases.create(
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
      console.error("Ошибка при создании дела:", error)
      toast({
        variant: "destructive",
        title: "Ошибка",
        description: "Не удалось создать дело",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleClose = () => {
    setName("")
    setDescription("")
    onClose()
  }

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent>
        {isLoading && <LoadingOverlay />}
        <DialogHeader>
          <DialogTitle>Создать новое дело</DialogTitle>
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
              Создать
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
} 