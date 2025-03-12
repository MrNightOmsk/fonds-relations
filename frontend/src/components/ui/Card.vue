<template>
  <div 
    class="bg-white dark:bg-background-dark rounded-xl shadow-card dark:shadow-card-dark border border-border-light dark:border-border-dark overflow-hidden"
    :class="{ 
      'hover:shadow-lg transition-shadow duration-200': hover,
      'cursor-pointer': clickable
    }"
    @click="clickable && $emit('click')"
  >
    <!-- Заголовок карточки, если есть -->
    <div 
      v-if="$slots.header || title" 
      class="border-b border-border-light dark:border-border-dark p-4"
      :class="{ 'bg-surface-light dark:bg-surface-dark': headerBg }"
    >
      <slot name="header">
        <h3 class="text-lg font-semibold text-text-light dark:text-text-dark">{{ title }}</h3>
      </slot>
    </div>
    
    <!-- Основное содержимое -->
    <div class="p-4" :class="{ 'p-6': padding === 'lg', 'p-3': padding === 'sm' }">
      <slot></slot>
    </div>
    
    <!-- Футер карточки, если есть -->
    <div 
      v-if="$slots.footer" 
      class="border-t border-border-light dark:border-border-dark p-4"
      :class="{ 'bg-surface-light dark:bg-surface-dark': footerBg }"
    >
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
// Тип для padding
type CardPadding = 'sm' | 'md' | 'lg';

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  padding: {
    type: String as () => CardPadding,
    default: 'md',
    validator: (value: string) => ['sm', 'md', 'lg'].includes(value)
  },
  hover: {
    type: Boolean,
    default: false
  },
  clickable: {
    type: Boolean,
    default: false
  },
  headerBg: {
    type: Boolean,
    default: false
  },
  footerBg: {
    type: Boolean,
    default: false
  }
});

defineEmits(['click']);
</script> 