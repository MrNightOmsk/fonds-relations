<template>
  <div 
    :class="[
      'flex items-center justify-center overflow-hidden',
      sizeClasses,
      colorClasses,
      shapeClasses,
      { 'ring-2 ring-white dark:ring-base-200': bordered }
    ]"
  >
    <img 
      v-if="src" 
      :src="src" 
      :alt="alt || text"
      class="h-full w-full object-cover"
    />
    <span v-else-if="text" class="text-center font-medium select-none">
      {{ initials }}
    </span>
    <span v-else class="text-center font-medium">?</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

type AvatarSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';
type AvatarShape = 'square' | 'rounded' | 'circle';

const props = defineProps({
  text: {
    type: String,
    default: ''
  },
  src: {
    type: String,
    default: ''
  },
  alt: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md',
    validator: (value: string) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
  },
  shape: {
    type: String,
    default: 'circle',
    validator: (value: string) => ['square', 'rounded', 'circle'].includes(value)
  },
  color: {
    type: String,
    default: 'auto'
  },
  bordered: {
    type: Boolean,
    default: false
  }
});

// Размеры аватара
const sizeClasses = computed(() => {
  const sizes: Record<string, string> = {
    xs: 'w-6 h-6 text-xs',
    sm: 'w-8 h-8 text-xs',
    md: 'w-10 h-10 text-sm',
    lg: 'w-12 h-12 text-base',
    xl: 'w-16 h-16 text-lg'
  };
  
  const sizeValue = props.size as unknown as string;
  return sizes[sizeValue] || sizes.md;
});

// Форма аватара
const shapeClasses = computed(() => {
  const shapes: Record<string, string> = {
    square: 'rounded-none',
    rounded: 'rounded-md',
    circle: 'rounded-full'
  };
  
  const shapeValue = props.shape as unknown as string;
  return shapes[shapeValue] || shapes.circle;
});

// Цвета аватара
const colorClasses = computed(() => {
  const colorValue = props.color as unknown as string;
  const textValue = props.text as unknown as string;
  
  // Автоматическое определение цвета на основе текста
  if (colorValue === 'auto' && textValue) {
    const colors = [
      'bg-primary/10 text-primary dark:bg-primary-dark/20 dark:text-primary-dark',
      'bg-secondary/10 text-secondary dark:bg-secondary/20 dark:text-secondary',
      'bg-success/10 text-success dark:bg-success/20 dark:text-success',
      'bg-warning/10 text-warning dark:bg-warning/20 dark:text-warning',
      'bg-danger/10 text-danger dark:bg-danger/20 dark:text-danger',
      'bg-info/10 text-info dark:bg-info/20 dark:text-info'
    ];
    
    // Простой хеш для имени, чтобы получить стабильный цвет
    const hash = textValue.split('').reduce((acc, char) => {
      return char.charCodeAt(0) + acc;
    }, 0);
    
    return colors[hash % colors.length];
  }
  
  // Пользовательский цвет
  if (colorValue !== 'auto') {
    return `bg-${colorValue}/10 text-${colorValue} dark:bg-${colorValue}/20 dark:text-${colorValue}`;
  }
  
  // Цвет по умолчанию
  return 'bg-surface-light dark:bg-surface-dark text-text-light dark:text-text-dark';
});

// Инициалы из текста
const initials = computed(() => {
  const textValue = props.text as unknown as string;
  if (!textValue) return '';
  
  const words = textValue.split(' ').filter(word => word.length > 0);
  
  if (words.length === 1) {
    // Одно слово - берем первые две буквы
    return words[0].substring(0, 2).toUpperCase();
  } else {
    // Несколько слов - берем первые буквы первых двух слов
    return (words[0][0] + words[1][0]).toUpperCase();
  }
});
</script> 