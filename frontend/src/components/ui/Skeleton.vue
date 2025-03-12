<template>
  <div 
    class="animate-pulse rounded"
    :class="[
      'bg-surface-light/50 dark:bg-surface-dark/50',
      radiusClass
    ]"
    :style="{
      width: width || '100%',
      height: height || '1rem'
    }"
  ></div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  width: {
    type: String,
    default: '100%'
  },
  height: {
    type: String,
    default: '1rem'
  },
  radius: {
    type: String,
    default: 'md',
    validator: (value: string) => {
      return ['none', 'sm', 'md', 'lg', 'full'].includes(value);
    }
  }
});

const radiusClass = computed(() => {
  const radiusMap: Record<string, string> = {
    'none': 'rounded-none',
    'sm': 'rounded-sm',
    'md': 'rounded',
    'lg': 'rounded-lg',
    'full': 'rounded-full'
  };
  
  const radiusValue = props.radius as string;
  return radiusMap[radiusValue] || 'rounded';
});
</script> 