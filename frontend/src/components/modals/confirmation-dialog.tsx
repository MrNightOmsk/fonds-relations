"use client"

import { Button } from "@/components/ui/button"
import { Modal } from "@/components/ui/modal"

interface ConfirmationDialogProps {
  isOpen: boolean
  onClose: () => void
  onConfirm: () => void
  title: string
  description: string
  confirmText?: string
  cancelText?: string
}

export function ConfirmationDialog({
  isOpen,
  onClose,
  onConfirm,
  title,
  description,
  confirmText = "Подтвердить",
  cancelText = "Отмена",
}: ConfirmationDialogProps) {
  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <h2 className="text-2xl font-bold mb-4">{title}</h2>
      <p className="mb-6">{description}</p>
      <div className="flex justify-end space-x-2">
        <Button
          type="button"
          variant="outline"
          onClick={onClose}
        >
          {cancelText}
        </Button>
        <Button
          type="button"
          variant="destructive"
          onClick={() => {
            onConfirm()
            onClose()
          }}
        >
          {confirmText}
        </Button>
      </div>
    </Modal>
  )
} 