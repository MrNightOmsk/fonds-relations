"use client"

import { LoadingOverlay } from "@/components/loading-overlay"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

interface DeleteConfirmationModalProps {
  isOpen: boolean
  onClose: () => void
  onConfirm: () => void
  isLoading?: boolean
  itemName: string
}

export function DeleteConfirmationModal({
  isOpen,
  onClose,
  onConfirm,
  isLoading = false,
  itemName,
}: DeleteConfirmationModalProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        {isLoading && <LoadingOverlay />}
        <DialogHeader>
          <DialogTitle>Подтверждение удаления</DialogTitle>
          <DialogDescription>
            Вы уверены, что хотите удалить {itemName}?
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button
            variant="outline"
            onClick={onClose}
            disabled={isLoading}
          >
            Отмена
          </Button>
          <Button
            variant="destructive"
            onClick={onConfirm}
            disabled={isLoading}
          >
            Удалить
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
} 