<template>
  <div 
    v-if="isVisible"
    class="alert rounded-lg p-4 mb-4 flex items-start"
    :class="variantClasses"
    role="alert"
  >
    <!-- Иконка -->
    <div v-if="showIcon" class="flex-shrink-0 mr-3">
      <svg v-if="variant === 'info'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
      </svg>
      <svg v-else-if="variant === 'success'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
      </svg>
      <svg v-else-if="variant === 'warning'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
      </svg>
      <svg v-else-if="variant === 'danger'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
      </svg>
    </div>
    
    <!-- Содержимое -->
    <div class="flex-grow">
      <h4 v-if="title" class="font-medium mb-1">{{ title }}</h4>
      <div class="text-sm">
        <slot></slot>
      </div>
    </div>
    
    <!-- Кнопка закрытия -->
    <button 
      v-if="dismissible" 
      @click="close"
      class="flex-shrink-0 ml-3 -mt-1 -mr-1 p-1 rounded-full hover:bg-black/5 dark:hover:bg-white/5 transition-colors"
      aria-label="Закрыть"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
      </svg>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

type AlertVariant = 'info' | 'success' | 'warning' | 'danger';

const props = defineProps({
  variant: {
    type: String as () => AlertVariant,
    default: 'info',
    validator: (value: string) => {
      return ['info', 'success', 'warning', 'danger'].includes(value);
    }
  },
  title: {
    type: String,
    default: ''
  },
  dismissible: {
    type: Boolean,
    default: false
  },
  showIcon: {
    type: Boolean,
    default: true
  },
  autoClose: {
    type: Boolean,
    default: false
  },
  duration: {
    type: Number,
    default: 5000
  }
});

const emit = defineEmits(['close']);

const isVisible = ref(true);

// Варианты стилей для разных типов уведомлений
const variantClasses = computed(() => {
  switch (props.variant) {
    case 'info':
      return 'bg-info/10 text-info dark:bg-info/20 dark:text-info border-l-4 border-info';
    case 'success':
      return 'bg-success/10 text-success dark:bg-success/20 dark:text-success border-l-4 border-success';
    case 'warning':
      return 'bg-warning/10 text-warning dark:bg-warning/20 dark:text-warning border-l-4 border-warning';
    case 'danger':
      return 'bg-danger/10 text-danger dark:bg-danger/20 dark:text-danger border-l-4 border-danger';
    default:
      return 'bg-info/10 text-info dark:bg-info/20 dark:text-info border-l-4 border-info';
  }
});

// Закрытие уведомления
const close = () => {
  isVisible.value = false;
  emit('close');
};

// Автоматическое закрытие, если включено
if (props.autoClose && props.duration > 0) {
  setTimeout(() => {
    close();
  }, props.duration);
}
</script>

<style scoped>
.alert-enter-active,
.alert-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.alert-enter-from,
.alert-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style> 