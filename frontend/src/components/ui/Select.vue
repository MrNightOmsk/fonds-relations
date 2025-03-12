<template>
  <div class="select-wrapper">
    <label 
      v-if="label" 
      :for="id" 
      class="block text-sm font-medium text-text-light dark:text-text-dark mb-1"
    >
      {{ label }}
      <span v-if="required" class="text-danger dark:text-danger ml-1">*</span>
    </label>
    
    <div class="relative">
      <select
        :id="id"
        :value="modelValue"
        @change="onChange"
        :disabled="disabled"
        :required="required"
        :class="[
          'block w-full rounded-lg border appearance-none transition-colors',
          'text-text-light dark:text-text-dark',
          'focus:ring-2 focus:outline-none',
          'pl-4 pr-10 py-3',
          {
            'bg-surface-light dark:bg-base-300 border-border-light dark:border-border-dark': !error,
            'focus:ring-primary dark:focus:ring-primary-dark focus:border-primary dark:focus:border-primary-dark': !error,
            'bg-danger/5 dark:bg-danger/10 border-danger dark:border-danger focus:ring-danger focus:border-danger': error,
            'opacity-60 cursor-not-allowed': disabled
          }
        ]"
      >
        <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
        <option 
          v-for="option in options" 
          :key="option.value" 
          :value="option.value" 
          :disabled="option.disabled"
        >
          {{ option.label }}
        </option>
      </select>
      
      <!-- Иконка выпадающего списка -->
      <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-text-secondary-light dark:text-text-secondary-dark">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
      </div>
    </div>
    
    <!-- Сообщение об ошибке -->
    <div
      v-if="error && errorMessage"
      class="mt-1 text-sm text-danger dark:text-danger"
    >
      {{ errorMessage }}
    </div>
    
    <!-- Подсказка -->
    <div
      v-if="hint && !error"
      class="mt-1 text-sm text-text-secondary-light dark:text-text-secondary-dark"
    >
      {{ hint }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface SelectOption {
  value: string | number;
  label: string;
  disabled?: boolean;
}

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  id: {
    type: String,
    default: () => `select-${Math.random().toString(36).substring(2, 9)}`
  },
  options: {
    type: Array as () => SelectOption[],
    default: () => []
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  required: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  error: {
    type: Boolean,
    default: false
  },
  errorMessage: {
    type: String,
    default: ''
  },
  hint: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['update:modelValue']);

// Обработчик изменения для двустороннего связывания
const onChange = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  emit('update:modelValue', target.value);
};
</script> 