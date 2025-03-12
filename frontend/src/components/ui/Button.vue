<template>
  <button
    :type="type"
    :class="[
      'font-medium rounded-md transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2',
      sizeClasses,
      variantClasses,
      { 'opacity-60 cursor-not-allowed': disabled }
    ]"
    :disabled="disabled || loading"
    @click="onClick"
  >
    <div class="flex items-center justify-center space-x-2">
      <!-- Индикатор загрузки -->
      <svg
        v-if="loading"
        class="animate-spin h-4 w-4"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="4"
        />
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </svg>

      <!-- Иконка слева -->
      <slot name="icon-left"></slot>

      <!-- Текст кнопки -->
      <span><slot>{{ text }}</slot></span>

      <!-- Иконка справа -->
      <slot name="icon-right"></slot>
    </div>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';

// Определяем типы для variant и size
type ButtonVariant = 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info' | 'outline' | 'ghost';
type ButtonSize = 'sm' | 'md' | 'lg';
type ButtonType = 'button' | 'submit' | 'reset';

interface Props {
  variant: ButtonVariant;
  size: ButtonSize;
  text: string;
  type: ButtonType;
  loading: boolean;
  disabled: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  text: '',
  type: 'button',
  loading: false,
  disabled: false
});

const emit = defineEmits(['click']);

const onClick = (event: MouseEvent) => {
  if (!props.disabled && !props.loading) {
    emit('click', event);
  }
};

const variantClasses = computed(() => {
  switch (props.variant) {
    case 'primary':
      return 'bg-primary dark:bg-primary-dark text-white hover:bg-primary-dark focus:ring-primary';
    case 'secondary':
      return 'bg-secondary dark:bg-secondary text-white hover:bg-secondary-dark focus:ring-secondary';
    case 'success':
      return 'bg-success dark:bg-success text-white hover:bg-success-dark focus:ring-success';
    case 'danger':
      return 'bg-danger dark:bg-danger text-white hover:bg-danger-dark focus:ring-danger';
    case 'warning':
      return 'bg-warning dark:bg-warning text-white hover:bg-warning-dark focus:ring-warning';
    case 'info':
      return 'bg-primary/10 dark:bg-primary-dark/10 text-primary dark:text-primary-dark hover:bg-primary/20 dark:hover:bg-primary-dark/20 focus:ring-primary';
    case 'outline':
      return 'bg-transparent border border-border-light dark:border-border-dark text-text-light dark:text-text-dark hover:bg-surface-light dark:hover:bg-base-300';
    case 'ghost':
      return 'bg-transparent text-text-light dark:text-text-dark hover:bg-surface-light dark:hover:bg-base-300';
    default:
      return 'bg-primary dark:bg-primary-dark text-white hover:bg-primary-dark focus:ring-primary';
  }
});

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'px-3 py-1.5 text-sm';
    case 'md':
      return 'px-4 py-2 text-base';
    case 'lg':
      return 'px-5 py-2.5 text-lg';
    default:
      return 'px-4 py-2 text-base';
  }
});
</script> 