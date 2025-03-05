<template>
  <div class="payment-methods">
    <h3 class="text-lg font-medium mb-2">Методы оплаты</h3>

    <!-- Список методов оплаты -->
    <div v-if="paymentMethods.length" class="mb-4 space-y-2">
      <div 
        v-for="method in paymentMethods" 
        :key="method.id" 
        class="p-3 bg-white border rounded-lg shadow-sm"
      >
        <div class="flex justify-between items-start">
          <div>
            <div class="flex items-center">
              <span 
                class="px-2 py-1 rounded-full text-xs font-medium mr-2"
                :class="getTypeClass(method.type)"
              >
                {{ getTypeName(method.type) }}
              </span>
              <span class="font-medium">{{ method.value }}</span>
            </div>
            <div v-if="method.description" class="text-sm text-gray-600 mt-1">
              {{ method.description }}
            </div>
          </div>
          <div v-if="editable" class="flex space-x-2">
            <button 
              @click="deleteMethod(method.id)"
              class="text-red-500 hover:text-red-700" 
              title="Удалить"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-gray-500 mb-4 p-3 bg-gray-50 rounded-lg text-center">
      У игрока нет методов оплаты
    </div>

    <!-- Форма добавления метода оплаты -->
    <div v-if="editable" class="border rounded-lg p-4 bg-gray-50">
      <h4 class="font-medium mb-3">Добавить метод оплаты</h4>
      <div class="grid gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Тип</label>
          <select v-model="newMethod.type" class="w-full p-2 border rounded">
            <option value="bank">Банковская карта</option>
            <option value="crypto">Криптовалюта</option>
            <option value="paypal">PayPal</option>
            <option value="other">Другое</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Значение</label>
          <input 
            v-model="newMethod.value" 
            type="text" 
            class="w-full p-2 border rounded"
            placeholder="Номер карты, криптокошелек и т.д."
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Описание (опционально)</label>
          <textarea 
            v-model="newMethod.description" 
            class="w-full p-2 border rounded"
            rows="2"
            placeholder="Дополнительная информация"
          ></textarea>
        </div>
        <div>
          <button 
            @click="addMethod" 
            class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            :disabled="!newMethod.value"
          >
            Добавить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits, computed, watch } from 'vue';
import type { PlayerPaymentMethod } from '@/types/models';

const props = defineProps<{
  modelValue: PlayerPaymentMethod[];
  playerId: string;
  editable?: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', methods: PlayerPaymentMethod[]): void;
  (e: 'add', method: Partial<PlayerPaymentMethod>): void;
  (e: 'delete', methodId: string): void;
}>();

const paymentMethods = computed({
  get: () => props.modelValue || [],
  set: (value) => emit('update:modelValue', value)
});

const newMethod = ref<Partial<PlayerPaymentMethod>>({
  player_id: props.playerId,
  type: 'bank',
  value: '',
  description: ''
});

watch(() => props.playerId, (newPlayerId) => {
  newMethod.value.player_id = newPlayerId;
});

function getTypeName(type: string): string {
  const types: Record<string, string> = {
    'bank': 'Банк',
    'crypto': 'Крипто',
    'paypal': 'PayPal',
    'other': 'Другое'
  };
  return types[type] || type;
}

function getTypeClass(type: string): string {
  const classes: Record<string, string> = {
    'bank': 'bg-blue-100 text-blue-800',
    'crypto': 'bg-green-100 text-green-800',
    'paypal': 'bg-purple-100 text-purple-800',
    'other': 'bg-gray-100 text-gray-800'
  };
  return classes[type] || 'bg-gray-100 text-gray-800';
}

function addMethod() {
  if (!newMethod.value.value) return;
  
  emit('add', { ...newMethod.value });
  
  // Сброс формы
  newMethod.value = {
    player_id: props.playerId,
    type: 'bank',
    value: '',
    description: ''
  };
}

function deleteMethod(methodId: string) {
  if (!methodId) return;
  emit('delete', methodId);
}
</script> 