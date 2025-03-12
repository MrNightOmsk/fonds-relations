<template>
  <div class="tooltip-container" @mouseenter="show" @mouseleave="hide">
    <!-- Контент, к которому прикреплена подсказка -->
    <slot></slot>
    
    <!-- Подсказка -->
    <Teleport to="body">
      <Transition name="tooltip-fade">
        <div 
          v-if="isVisible"
          ref="tooltipRef"
          :class="[
            'tooltip absolute py-1.5 px-3 rounded text-xs font-medium shadow-lg z-50',
            'bg-base-300 dark:bg-base-100 text-text-light dark:text-text-dark',
            positionClass
          ]"
          :style="tooltipStyle"
        >
          <slot name="content">{{ content }}</slot>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';

// Типы для положения подсказки
type TooltipPosition = 'top' | 'right' | 'bottom' | 'left';

interface Props {
  content: string;
  position?: TooltipPosition;
  delay?: number;
  offset?: number;
}

const props = defineProps({
  content: {
    type: String,
    default: ''
  },
  position: {
    type: String as () => TooltipPosition,
    default: 'top',
    validator: (value: string) => ['top', 'right', 'bottom', 'left'].includes(value)
  },
  delay: {
    type: Number,
    default: 300
  },
  offset: {
    type: Number,
    default: 8
  }
});

// Состояние видимости
const isVisible = ref(false);
const tooltipRef = ref<HTMLElement | null>(null);
const triggerElement = ref<HTMLElement | null>(null);
const tooltipStyle = ref({
  top: '0px',
  left: '0px'
});

// Классы положения
const positionClass = computed(() => {
  switch (props.position) {
    case 'top': return 'tooltip-top';
    case 'right': return 'tooltip-right';
    case 'bottom': return 'tooltip-bottom';
    case 'left': return 'tooltip-left';
    default: return 'tooltip-top';
  }
});

// Таймер для задержки
let showTimer: ReturnType<typeof setTimeout> | null = null;

// Показать подсказку
const show = () => {
  showTimer = setTimeout(() => {
    isVisible.value = true;
    // Обновляем позицию в следующем тике после рендеринга
    setTimeout(updatePosition, 0);
  }, props.delay);
};

// Скрыть подсказку
const hide = () => {
  if (showTimer) {
    clearTimeout(showTimer);
    showTimer = null;
  }
  isVisible.value = false;
};

// Обновление позиции подсказки
const updatePosition = () => {
  if (!isVisible.value || !tooltipRef.value) return;

  const element = triggerElement.value;
  const tooltip = tooltipRef.value;
  
  if (!element) return;
  
  const elementRect = element.getBoundingClientRect();
  const tooltipRect = tooltip.getBoundingClientRect();
  
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
  
  let top = 0;
  let left = 0;
  
  switch (props.position) {
    case 'top':
      top = elementRect.top + scrollTop - tooltipRect.height - props.offset;
      left = elementRect.left + scrollLeft + (elementRect.width / 2) - (tooltipRect.width / 2);
      break;
    case 'right':
      top = elementRect.top + scrollTop + (elementRect.height / 2) - (tooltipRect.height / 2);
      left = elementRect.right + scrollLeft + props.offset;
      break;
    case 'bottom':
      top = elementRect.bottom + scrollTop + props.offset;
      left = elementRect.left + scrollLeft + (elementRect.width / 2) - (tooltipRect.width / 2);
      break;
    case 'left':
      top = elementRect.top + scrollTop + (elementRect.height / 2) - (tooltipRect.height / 2);
      left = elementRect.left + scrollLeft - tooltipRect.width - props.offset;
      break;
  }
  
  // Проверка на выход за границы экрана
  const windowWidth = window.innerWidth;
  const windowHeight = window.innerHeight;
  
  // Горизонтальная проверка
  if (left < 0) {
    left = 0;
  } else if (left + tooltipRect.width > windowWidth) {
    left = windowWidth - tooltipRect.width;
  }
  
  // Вертикальная проверка
  if (top < 0) {
    top = 0;
  } else if (top + tooltipRect.height > windowHeight + scrollTop) {
    top = windowHeight + scrollTop - tooltipRect.height;
  }
  
  tooltipStyle.value = {
    top: `${top}px`,
    left: `${left}px`
  };
};

// Получаем ссылку на элемент-триггер после монтирования
onMounted(() => {
  const container = document.querySelector('.tooltip-container') as HTMLElement;
  if (container) {
    triggerElement.value = container;
  }
  
  // Обновляем позицию при изменении размера окна
  window.addEventListener('resize', updatePosition);
  window.addEventListener('scroll', updatePosition);
});

onUnmounted(() => {
  window.removeEventListener('resize', updatePosition);
  window.removeEventListener('scroll', updatePosition);
  
  if (showTimer) {
    clearTimeout(showTimer);
  }
});
</script>

<style scoped>
.tooltip-fade-enter-active,
.tooltip-fade-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}

.tooltip-fade-enter-from,
.tooltip-fade-leave-to {
  opacity: 0;
}

.tooltip-top.tooltip-fade-enter-from {
  transform: translateY(5px);
}
.tooltip-bottom.tooltip-fade-enter-from {
  transform: translateY(-5px);
}
.tooltip-left.tooltip-fade-enter-from {
  transform: translateX(5px);
}
.tooltip-right.tooltip-fade-enter-from {
  transform: translateX(-5px);
}

.tooltip {
  max-width: 250px;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.tooltip-container {
  display: inline-block;
  position: relative;
}
</style> 