<template>
  <span 
    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
    :class="[
      variantClasses,
      sizeClasses,
      outlineClasses
    ]"
  >
    <slot></slot>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue';

type BadgeVariant = 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info' | 'default';
type BadgeSize = 'sm' | 'md' | 'lg';

const props = defineProps({
  variant: {
    type: String as () => BadgeVariant,
    default: 'default',
    validator: (value: string) => {
      return ['primary', 'secondary', 'success', 'warning', 'danger', 'info', 'default'].includes(value);
    }
  },
  size: {
    type: String as () => BadgeSize,
    default: 'md',
    validator: (value: string) => {
      return ['sm', 'md', 'lg'].includes(value);
    }
  },
  outline: {
    type: Boolean,
    default: false
  }
});

const variantClasses = computed(() => {
  const isOutline = props.outline;
  const variant = props.variant as string;
  
  switch (variant) {
    case 'primary':
      return isOutline
        ? 'text-primary dark:text-primary-dark border border-primary dark:border-primary-dark'
        : 'bg-primary dark:bg-primary-dark text-white';
    case 'secondary':
      return isOutline
        ? 'text-secondary dark:text-secondary border border-secondary dark:border-secondary'
        : 'bg-secondary dark:bg-secondary text-white';
    case 'success':
      return isOutline
        ? 'text-success dark:text-success border border-success dark:border-success'
        : 'bg-success dark:bg-success text-white';
    case 'warning':
      return isOutline
        ? 'text-warning dark:text-warning border border-warning dark:border-warning'
        : 'bg-warning dark:bg-warning text-white';
    case 'danger':
      return isOutline
        ? 'text-danger dark:text-danger border border-danger dark:border-danger'
        : 'bg-danger dark:bg-danger text-white';
    case 'info':
      return isOutline
        ? 'text-info dark:text-info border border-info dark:border-info'
        : 'bg-info dark:bg-info text-white';
    default:
      return isOutline
        ? 'text-text-light dark:text-text-dark border border-border-light dark:border-border-dark'
        : 'bg-surface-light dark:bg-surface-dark text-text-light dark:text-text-dark';
  }
});

const sizeClasses = computed(() => {
  const size = props.size as string;
  
  switch (size) {
    case 'sm': return 'text-xs px-2 py-0.5';
    case 'md': return 'text-xs px-2.5 py-0.5';
    case 'lg': return 'text-sm px-3 py-1';
    default: return 'text-xs px-2.5 py-0.5';
  }
});

const outlineClasses = computed(() => props.outline ? 'bg-transparent' : '');
</script> 