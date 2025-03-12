<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div
        v-if="isOpen"
        class="fixed inset-0 z-50 overflow-y-auto"
        @click.self="closeOnOverlay && emit('close')"
      >
        <div class="min-h-screen px-4 flex items-center justify-center">
          <!-- Затемненный фон -->
          <div class="fixed inset-0 bg-black bg-opacity-40 dark:bg-opacity-50 transition-opacity"></div>
          
          <!-- Содержимое модального окна -->
          <div
            class="bg-surface-light dark:bg-surface-dark rounded-xl p-6 max-w-lg w-full mx-auto shadow-xl relative z-10 border border-border-light/40 dark:border-border-dark transform transition-all"
            :class="{ 'sm:max-w-sm': size === 'sm', 'sm:max-w-xl': size === 'lg', 'sm:max-w-2xl': size === 'xl' }"
          >
            <!-- Заголовок -->
            <div class="flex justify-between items-center mb-4" v-if="title">
              <h3 class="text-lg font-medium text-text-light dark:text-text-dark">{{ title }}</h3>
              <button
                @click="emit('close')"
                class="text-text-secondary-light dark:text-text-secondary-dark hover:text-text-light dark:hover:text-text-dark rounded-full p-1 transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
            
            <!-- Контент -->
            <div class="space-y-4">
              <slot></slot>
            </div>
            
            <!-- Футер -->
            <div class="mt-6 flex justify-end space-x-3" v-if="$slots.footer">
              <slot name="footer"></slot>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, watch, onMounted, onUnmounted } from 'vue';

// Типы для size
type ModalSize = 'sm' | 'md' | 'lg' | 'xl' | 'full';

interface Props {
  isOpen: boolean;
  title: string;
  size: ModalSize;
  showCloseButton: boolean;
  closeOnOverlay: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  isOpen: false,
  title: '',
  size: 'md',
  showCloseButton: true,
  closeOnOverlay: true
});

const emit = defineEmits<{
  (e: 'close'): void;
}>();

// Размер модального окна
const sizeClass = computed(() => {
  switch (props.size) {
    case 'sm': return 'max-w-md w-full';
    case 'md': return 'max-w-lg w-full';
    case 'lg': return 'max-w-xl w-full';
    case 'xl': return 'max-w-2xl w-full';
    case 'full': return 'max-w-5xl w-full';
    default: return 'max-w-lg w-full';
  }
});

// Блокировка скролла body при открытии модального окна
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
});

// Обработчик нажатия клавиши Escape для закрытия модального окна
const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Escape' && props.isOpen) {
    emit('close');
  }
};

onMounted(() => {
  document.addEventListener('keydown', handleKeydown);
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown);
  // Восстановление скролла при размонтировании компонента
  document.body.style.overflow = '';
});
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
  padding: 1rem;
}

.modal-container {
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  margin: 1rem;
}

/* Анимации */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease, transform 0.2s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style> 