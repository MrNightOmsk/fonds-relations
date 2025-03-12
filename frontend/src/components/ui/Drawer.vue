<template>
  <Teleport to="body">
    <!-- Overlay -->
    <div 
      v-if="isOpen" 
      class="fixed inset-0 bg-black/50 z-40 transition-opacity"
      :class="{ 'opacity-0': !isOpen }"
      @click="closeOnOverlay && $emit('update:isOpen', false)"
    ></div>
    
    <!-- Drawer -->
    <transition :name="transitionClass">
      <div 
        v-if="isOpen"
        class="fixed bg-white dark:bg-base-200 shadow-xl z-50 transition-all overflow-auto flex flex-col"
        :class="[positionClasses]"
        @keydown.esc="$emit('update:isOpen', false)"
      >
        <!-- Заголовок (если есть) -->
        <div 
          v-if="$slots.header || title"
          class="px-4 py-3 border-b border-border-light dark:border-border-dark flex items-center justify-between"
        >
          <div class="flex-1">
            <slot name="header">
              <h3 class="font-medium text-text-light dark:text-text-dark">{{ title }}</h3>
            </slot>
          </div>
          
          <!-- Кнопка закрытия -->
          <button
            v-if="showCloseButton"
            @click="$emit('update:isOpen', false)"
            class="p-1 text-text-secondary-light dark:text-text-secondary-dark hover:text-text-light dark:hover:text-text-dark rounded-full hover:bg-surface-light dark:hover:bg-base-300 transition-colors"
            aria-label="Закрыть"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
        
        <!-- Основное содержимое -->
        <div class="flex-1 overflow-y-auto p-4">
          <slot></slot>
        </div>
        
        <!-- Футер (если есть) -->
        <div 
          v-if="$slots.footer" 
          class="p-4 border-t border-border-light dark:border-border-dark"
        >
          <slot name="footer"></slot>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, watch, onMounted, onUnmounted } from 'vue';

// Типы для позиции панели
type DrawerPosition = 'left' | 'right' | 'top' | 'bottom';
type DrawerSize = 'sm' | 'md' | 'lg' | 'full';

// Интерфейс для props
interface Props {
  isOpen: boolean;
  position?: DrawerPosition;
  size?: DrawerSize;
  title?: string;
  showCloseButton?: boolean;
  closeOnOverlay?: boolean;
}

// Определение props с значениями по умолчанию
const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  position: {
    type: String as () => DrawerPosition,
    default: 'right',
    validator: (value: string) => ['left', 'right', 'top', 'bottom'].includes(value)
  },
  size: {
    type: String as () => DrawerSize,
    default: 'md',
    validator: (value: string) => ['sm', 'md', 'lg', 'full'].includes(value)
  },
  title: {
    type: String,
    default: ''
  },
  showCloseButton: {
    type: Boolean,
    default: true
  },
  closeOnOverlay: {
    type: Boolean,
    default: true
  }
});

// Определение событий
defineEmits(['update:isOpen']);

// Вычисление классов для позиции и размера
const positionClasses = computed(() => {
  // Базовые классы для каждой позиции
  const basePositions = {
    left: 'inset-y-0 left-0 h-full',
    right: 'inset-y-0 right-0 h-full',
    top: 'inset-x-0 top-0 w-full',
    bottom: 'inset-x-0 bottom-0 w-full'
  };
  
  // Размеры для горизонтальных панелей (left, right)
  const horizontalSizes = {
    sm: 'w-64',
    md: 'w-80',
    lg: 'w-96',
    full: 'w-full max-w-screen-md'
  };
  
  // Размеры для вертикальных панелей (top, bottom)
  const verticalSizes = {
    sm: 'h-40',
    md: 'h-60',
    lg: 'h-80',
    full: 'h-screen/2'
  };
  
  const position = props.position as DrawerPosition;
  const size = props.size as DrawerSize;
  
  // Выбираем размер в зависимости от позиции
  const sizeClass = ['left', 'right'].includes(position) 
    ? horizontalSizes[size] 
    : verticalSizes[size];
  
  return `${basePositions[position]} ${sizeClass}`;
});

// Анимация в зависимости от позиции
const transitionClass = computed(() => {
  switch (props.position) {
    case 'left': return 'drawer-left';
    case 'right': return 'drawer-right';
    case 'top': return 'drawer-top';
    case 'bottom': return 'drawer-bottom';
    default: return 'drawer-right';
  }
});

// Блокировка скролла при открытой панели
watch(() => props.isOpen, (value) => {
  if (value) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
});

// Обработка клавиши Escape для закрытия панели
const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape' && props.isOpen) {
    e.preventDefault();
    e.stopPropagation();
  }
};

// Монтирование
onMounted(() => {
  document.addEventListener('keydown', handleKeydown);
});

// Размонтирование
onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown);
  
  // Восстанавливаем прокрутку страницы
  document.body.style.overflow = '';
});
</script>

<style scoped>
/* Анимации для разных позиций */
.drawer-left-enter-active,
.drawer-left-leave-active,
.drawer-right-enter-active,
.drawer-right-leave-active,
.drawer-top-enter-active,
.drawer-top-leave-active,
.drawer-bottom-enter-active,
.drawer-bottom-leave-active {
  transition: transform 0.3s ease;
}

/* Левая панель */
.drawer-left-enter-from,
.drawer-left-leave-to {
  transform: translateX(-100%);
}

/* Правая панель */
.drawer-right-enter-from,
.drawer-right-leave-to {
  transform: translateX(100%);
}

/* Верхняя панель */
.drawer-top-enter-from,
.drawer-top-leave-to {
  transform: translateY(-100%);
}

/* Нижняя панель */
.drawer-bottom-enter-from,
.drawer-bottom-leave-to {
  transform: translateY(100%);
}
</style> 