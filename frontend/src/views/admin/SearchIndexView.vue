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
          class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:bg-gray-400 mr-2"
          :disabled="isIndexing || isFullIndexing"
        >
          <span v-if="isIndexing">Индексация...</span>
          <span v-else>Индексировать игроков</span>
        </button>
        
        <button 
          @click="indexAllPlayersFull" 
          class="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 disabled:bg-gray-400"
          :disabled="isIndexing || isFullIndexing"
        >
          <span v-if="isFullIndexing">Полная индексация...</span>
          <span v-else>Индексировать ВСЕХ игроков</span>
        </button>
        
        <div v-if="indexMessage" class="mt-4 p-3 rounded" :class="indexSuccess ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
          {{ indexMessage }}
        </div>
      </div>
    </div>
    
    <!-- Удаление индекса -->
    <div class="mt-8 bg-white p-6 rounded-lg shadow">
      <h2 class="text-xl font-semibold mb-4">Удаление индекса</h2>
      <p class="mb-4 text-gray-600">
        Полностью удаляет индекс игроков из Elasticsearch.
        <span class="text-red-600 font-bold">Внимание! Эта операция удалит все данные из индекса и не может быть отменена!</span>
        После удаления индекса необходимо заново его создать с помощью кнопки "Инициализировать индекс".
      </p>
      
      <div v-if="!confirmDeleteIndex" class="mb-4">
        <button 
          @click="confirmDeleteIndex = true" 
          class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 disabled:bg-gray-400"
          :disabled="isDeleting"
        >
          Удалить индекс
        </button>
      </div>
      
      <div v-else class="mb-4 p-4 bg-red-50 border border-red-300 rounded">
        <p class="text-red-700 font-bold mb-3">Вы уверены, что хотите удалить индекс?</p>
        <p class="text-red-600 mb-4">Все данные индекса будут потеряны, и поиск перестанет работать до повторной инициализации.</p>
        
        <div class="flex space-x-3">
          <button 
            @click="deleteSearchIndex" 
            class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 disabled:bg-gray-400"
            :disabled="isDeleting"
          >
            <span v-if="isDeleting">Удаление...</span>
            <span v-else>Подтвердить удаление</span>
          </button>
          
          <button 
            @click="confirmDeleteIndex = false" 
            class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
            :disabled="isDeleting"
          >
            Отмена
          </button>
        </div>
      </div>
      
      <div v-if="deleteMessage" class="mt-4 p-3 rounded" :class="deleteSuccess ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
        {{ deleteMessage }}
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
const isFullIndexing = ref(false);
const indexMessage = ref('');
const indexSuccess = ref(false);
const indexOptions = reactive({
  skip: 0,
  limit: 100
});

// Состояние для удаления индекса
const isDeleting = ref(false);
const confirmDeleteIndex = ref(false);
const deleteMessage = ref('');
const deleteSuccess = ref(false);

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

// Полная индексация всех игроков
async function indexAllPlayersFull() {
  isFullIndexing.value = true;
  indexMessage.value = '';
  
  try {
    const result = await searchApi.indexAllPlayersBatched(100);
    indexSuccess.value = true;
    indexMessage.value = `Проиндексировано ${result.indexed_count} из ${result.total_count} игроков. Неудач: ${result.failed_count}`;
  } catch (error: any) {
    indexSuccess.value = false;
    indexMessage.value = error.response?.data?.detail || 'Ошибка полной индексации игроков';
    console.error('Ошибка при полной индексации игроков:', error);
  } finally {
    isFullIndexing.value = false;
  }
}

// Удаление индекса
async function deleteSearchIndex() {
  isDeleting.value = true;
  deleteMessage.value = '';
  
  try {
    const result = await searchApi.deleteSearchIndex();
    deleteSuccess.value = true;
    deleteMessage.value = result.message || 'Индекс успешно удален';
    // Сбрасываем флаг подтверждения после успешного удаления
    confirmDeleteIndex.value = false;
  } catch (error: any) {
    deleteSuccess.value = false;
    deleteMessage.value = error.response?.data?.detail || 'Ошибка при удалении индекса';
    console.error('Ошибка при удалении индекса:', error);
  } finally {
    isDeleting.value = false;
  }
}
</script> 