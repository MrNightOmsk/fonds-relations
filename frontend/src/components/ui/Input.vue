<template>
  <div class="input-wrapper">
    <label 
      v-if="label" 
      :for="id" 
      class="block text-sm font-medium text-text-light dark:text-text-dark mb-1"
    >
      {{ label }}
      <span v-if="required" class="text-danger dark:text-danger ml-1">*</span>
    </label>
    
    <div class="relative">
      <!-- Иконка слева, если есть -->
      <div 
        v-if="$slots['icon-left']" 
        class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-text-secondary-light dark:text-text-secondary-dark"
      >
        <slot name="icon-left"></slot>
      </div>
      
      <!-- Поле ввода -->
      <input
        :id="id"
        :type="type"
        :value="modelValue"
        @input="onInput"
        :placeholder="placeholder"
        :disabled="disabled"
        :required="required"
        :class="[
          'block w-full rounded-lg border transition-colors',
          'text-text-light dark:text-text-dark',
          'focus:ring-2 focus:outline-none',
          $slots['icon-left'] ? 'pl-10' : 'pl-4',
          $slots['icon-right'] ? 'pr-10' : 'pr-4',
          'py-3',
          {
            'bg-surface-light dark:bg-base-300 border-border-light dark:border-border-dark': !hasError && !hasSuccess,
            'focus:ring-primary dark:focus:ring-primary-dark focus:border-primary dark:focus:border-primary-dark': !hasError && !hasSuccess,
            'bg-danger/5 dark:bg-danger/10 border-danger dark:border-danger focus:ring-danger focus:border-danger': hasError,
            'bg-success/5 dark:bg-success/10 border-success dark:border-success focus:ring-success focus:border-success': hasSuccess && !hasError,
            'opacity-60 cursor-not-allowed': disabled
          }
        ]"
      />
      
      <!-- Иконка справа, если есть -->
      <div 
        v-if="$slots['icon-right']" 
        class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-text-secondary-light dark:text-text-secondary-dark"
      >
        <slot name="icon-right"></slot>
      </div>
      
      <!-- Иконка ошибки -->
      <div
        v-if="hasError && !$slots['icon-right']"
        class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-danger dark:text-danger"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
      </div>
      
      <!-- Иконка успеха -->
      <div
        v-if="hasSuccess && !hasError && !$slots['icon-right']"
        class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-success dark:text-success"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
        </svg>
      </div>
    </div>
    
    <!-- Сообщение об ошибке -->
    <div
      v-if="hasError && errorMessage"
      class="mt-1 text-sm text-danger dark:text-danger"
    >
      {{ errorMessage }}
    </div>
    
    <!-- Подсказка -->
    <div
      v-if="hint && !hasError"
      class="mt-1 text-sm text-text-secondary-light dark:text-text-secondary-dark"
    >
      {{ hint }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  id: {
    type: String,
    default: () => `input-${Math.random().toString(36).substring(2, 9)}`
  },
  label: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'text'
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
  success: {
    type: Boolean,
    default: false
  },
  hint: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['update:modelValue']);

// Вычисляемые свойства для состояний ошибки и успеха
const hasError = computed(() => props.error || !!props.errorMessage);
const hasSuccess = computed(() => props.success);

// Обработчик ввода для двустороннего связывания
const onInput = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:modelValue', target.value);
};
</script> 