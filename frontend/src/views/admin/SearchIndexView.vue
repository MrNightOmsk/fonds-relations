<template>
  <div class="search-index-admin">
    <h1 class="text-2xl font-bold mb-6">Управление поисковым индексом</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Инициализация индекса -->
      <div class="bg-white p-6 rounded-lg shadow">
        <h2 class="text-xl font-semibold mb-4">Инициализация индекса</h2>
        <p class="mb-4 text-gray-600">
          Создает индекс в Elasticsearch с необходимыми маппингами и настройками.
          Используйте эту функцию при первом запуске или если индекс был удален.
        </p>
        <button 
          @click="initializeIndex" 
          class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
          :disabled="isInitializing"
        >
          <span v-if="isInitializing">Инициализация...</span>
          <span v-else>Инициализировать индекс</span>
        </button>
        <div v-if="initMessage" class="mt-4 p-3 rounded" :class="initSuccess ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
          {{ initMessage }}
        </div>
      </div>
      
      <!-- Индексация игроков -->
      <div class="bg-white p-6 rounded-lg shadow">
        <h2 class="text-xl font-semibold mb-4">Индексация игроков</h2>
        <p class="mb-4 text-gray-600">
          Индексирует игроков из базы данных в Elasticsearch.
          Вы можете указать количество игроков для индексации и смещение.
        </p>
        
        <div class="flex flex-col space-y-4 mb-4">
          <div class="flex items-center">
            <label class="w-24">Смещение:</label>
            <input 
              v-model.number="indexOptions.skip" 
              type="number" 
              min="0" 
              class="border rounded px-2 py-1 w-24"
            />
          </div>
          <div class="flex items-center">
            <label class="w-24">Лимит:</label>
            <input 
              v-model.number="indexOptions.limit" 
              type="number" 
              min="1" 
              max="1000" 
              class="border rounded px-2 py-1 w-24"
            />
          </div>
        </div>
        
        <button 
          @click="indexAllPlayers" 
          class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:bg-gray-400"
          :disabled="isIndexing"
        >
          <span v-if="isIndexing">Индексация...</span>
          <span v-else>Индексировать игроков</span>
        </button>
        <div v-if="indexMessage" class="mt-4 p-3 rounded" :class="indexSuccess ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
          {{ indexMessage }}
        </div>
      </div>
    </div>
    
    <!-- Статистика индекса -->
    <div class="mt-8 bg-white p-6 rounded-lg shadow">
      <h2 class="text-xl font-semibold mb-4">Статистика индекса</h2>
      <p class="mb-4 text-gray-600">
        Здесь будет отображаться статистика индекса Elasticsearch.
        В будущих версиях будет добавлена возможность просмотра количества документов, размера индекса и других метрик.
      </p>
      <div class="bg-gray-100 p-4 rounded">
        <p>Функционал в разработке</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useSearchApi } from '@/api/search';

const searchApi = useSearchApi();

// Состояние для инициализации индекса
const isInitializing = ref(false);
const initMessage = ref('');
const initSuccess = ref(false);

// Состояние для индексации игроков
const isIndexing = ref(false);
const indexMessage = ref('');
const indexSuccess = ref(false);
const indexOptions = reactive({
  skip: 0,
  limit: 100
});

// Инициализация индекса
async function initializeIndex() {
  isInitializing.value = true;
  initMessage.value = '';
  
  try {
    const result = await searchApi.initializeSearchIndex();
    initSuccess.value = true;
    initMessage.value = result.message || 'Индекс успешно инициализирован';
  } catch (error: any) {
    initSuccess.value = false;
    initMessage.value = error.response?.data?.detail || 'Ошибка при инициализации индекса';
    console.error('Ошибка при инициализации индекса:', error);
  } finally {
    isInitializing.value = false;
  }
}

// Индексация всех игроков
async function indexAllPlayers() {
  isIndexing.value = true;
  indexMessage.value = '';
  
  try {
    const result = await searchApi.indexAllPlayers(
      indexOptions.skip,
      indexOptions.limit
    );
    indexSuccess.value = true;
    indexMessage.value = result.message || `Проиндексировано ${result.indexed_count} игроков`;
  } catch (error: any) {
    indexSuccess.value = false;
    indexMessage.value = error.response?.data?.detail || 'Ошибка при индексации игроков';
    console.error('Ошибка при индексации игроков:', error);
  } finally {
    isIndexing.value = false;
  }
}
</script> 