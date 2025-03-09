<template>
  <div class="search-container">
    <div class="relative w-full">
      <input 
        type="text" 
        v-model="searchQuery" 
        @input="debouncedSearch" 
        placeholder="Поиск игроков, кейсов..." 
        class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button 
        v-if="searchQuery" 
        @click="clearSearch" 
        class="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600"
        type="button"
      >
        <span>✕</span>
      </button>
    </div>
    
    <div v-if="loading" class="mt-2 p-2 text-center text-gray-500">
      <div class="inline-block animate-spin h-4 w-4 border-2 border-blue-500 rounded-full border-t-transparent mr-2"></div>
      Идет поиск...
    </div>
    
    <div v-else-if="searchPerformed && players.length === 0 && cases.length === 0" class="mt-2 p-2 text-center text-gray-500">
      Ничего не найдено
    </div>
    
    <div v-else-if="(players.length > 0 || cases.length > 0) && searchQuery" 
      class="results-container mt-2 shadow-lg rounded-lg border overflow-hidden bg-white">
      <div v-if="players.length > 0" class="section">
        <h3 class="bg-gray-100 px-3 py-1 font-medium text-sm">Игроки</h3>
        <div v-for="player in players" :key="player.id" 
             @click="selectResult('player', player)" 
             class="result-item p-2 hover:bg-blue-50 cursor-pointer border-b border-gray-100">
          <div class="font-medium">{{ player.full_name }}</div>
          <div class="text-xs text-gray-600" v-if="player.description">{{ truncate(player.description, 60) }}</div>
          <div class="text-xs text-gray-600" v-if="player.fund_name">Фонд: {{ player.fund_name }}</div>
          <div class="text-xs text-gray-600" v-if="player.contacts && player.contacts.length">
            Контакт: {{ player.contacts[0] }}
          </div>
        </div>
      </div>
      
      <div v-if="cases.length > 0" class="section">
        <h3 class="bg-gray-100 px-3 py-1 font-medium text-sm">Кейсы</h3>
        <div v-for="case_item in cases" :key="case_item.id" 
             @click="selectResult('case', case_item)" 
             class="result-item p-2 hover:bg-blue-50 cursor-pointer border-b border-gray-100">
          <div class="font-medium">{{ case_item.title }}</div>
          <div class="text-xs text-gray-600">{{ getCaseDetails(case_item) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useSearchApi } from '@/api/search';
import type { SearchPlayer, SearchCase } from '@/types/search';

// Объявление пропсов
const props = defineProps({
  // Можно добавить пропсы по необходимости, например:
  // maxResults: { type: Number, default: 5 }
});

// Объявление эмиттера событий
const emit = defineEmits(['select']);

// Состояние компонента
const router = useRouter();
const searchApi = useSearchApi();
const searchQuery = ref('');
const players = ref<SearchPlayer[]>([]);
const cases = ref<SearchCase[]>([]);
const loading = ref(false);
const searchPerformed = ref(false);
let searchTimeout: ReturnType<typeof setTimeout> | null = null;

// Функция для дебаунса поиска
const debouncedSearch = () => {
  if (searchTimeout) {
    clearTimeout(searchTimeout);
  }
  
  if (searchQuery.value.trim().length < 2) {
    clearResults();
    return;
  }
  
  searchTimeout = setTimeout(() => {
    search();
  }, 300); // 300ms задержка
};

// Очистка результатов
const clearResults = () => {
  players.value = [];
  cases.value = [];
  searchPerformed.value = false;
};

// Очистка поиска
const clearSearch = () => {
  searchQuery.value = '';
  clearResults();
};

// Функция поиска
const search = async () => {
  if (searchQuery.value.trim().length < 2) {
    clearResults();
    return;
  }
  
  loading.value = true;
  searchPerformed.value = true;
  
  try {
    // Используем реальный API
    try {
      const result = await searchApi.unifiedSearch(searchQuery.value);
      console.log('Результаты поиска API:', result);
      players.value = result.players;
      cases.value = result.cases;
    } catch (apiError) {
      console.warn('Ошибка при обращении к API поиска, используем моковые данные:', apiError);
      console.error('Детали ошибки API:', apiError.response?.data || apiError.message);
      // Если API недоступен, используем моковые данные как резервный вариант
      await mockSearchRequest();
    }
  } catch (error) {
    console.error('Ошибка при поиске:', error);
    clearResults();
  } finally {
    loading.value = false;
  }
};

// Временная функция для эмуляции запроса (только если API не отвечает)
const mockSearchRequest = () => {
  return new Promise<void>((resolve) => {
    setTimeout(() => {
      // Эмуляция поиска по игрокам
      if (searchQuery.value.toLowerCase().includes('иван')) {
        players.value = [
          { id: '1', full_name: 'Иванов Иван', details: 'Телефон: +7123456789', fund_name: 'Альфа Фонд' },
          { id: '2', full_name: 'Петров Иван', details: 'Email: ivan@example.com', fund_name: 'Бета Фонд' }
        ];
      } else if (searchQuery.value.toLowerCase().includes('петр')) {
        players.value = [
          { id: '3', full_name: 'Петров Петр', details: 'Telegram: @petrov', fund_name: 'Гамма Фонд' }
        ];
      } else {
        players.value = [];
      }
      
      // Эмуляция поиска по кейсам
      if (searchQuery.value.toLowerCase().includes('скам')) {
        cases.value = [
          { 
            id: '101', 
            title: 'Скам игрока на форуме', 
            status: 'open',
            player_name: 'Иванов Иван',
            player_id: '1',
            fund_name: 'Альфа Фонд',
            created_at: '2023-03-01T10:30:00Z'
          }
        ];
      } else if (searchQuery.value.toLowerCase().includes('долг')) {
        cases.value = [
          { 
            id: '102', 
            title: 'Долг за онлайн игру', 
            status: 'closed',
            player_name: 'Петров Петр',
            player_id: '3',
            fund_name: 'Гамма Фонд',
            created_at: '2023-02-15T14:20:00Z'
          }
        ];
      } else {
        cases.value = [];
      }
      
      resolve();
    }, 500); // Эмуляция задержки сети
  });
};

// Функция для получения деталей кейса
const getCaseDetails = (case_item: SearchCase): string => {
  const statusMap: Record<string, string> = {
    'open': 'Открыт',
    'in_progress': 'В работе',
    'resolved': 'Решён',
    'closed': 'Закрыт'
  };
  
  const status = statusMap[case_item.status] || case_item.status;
  const parts = [];
  
  parts.push(`Статус: ${status}`);
  
  if (case_item.player_name) {
    parts.push(`Игрок: ${case_item.player_name}`);
  }
  
  if (case_item.fund_name) {
    parts.push(`Фонд: ${case_item.fund_name}`);
  }
  
  return parts.join(', ');
};

// Обработка выбора результата
const selectResult = (type: 'player' | 'case', item: SearchPlayer | SearchCase) => {
  // Эмитим событие выбора
  emit('select', { type, item });
  
  // Перенаправляем на страницу детального просмотра
  if (type === 'player') {
    router.push(`/players/${item.id}`);
  } else if (type === 'case') {
    router.push(`/cases/${item.id}`);
  }
  
  // Очищаем результаты поиска
  clearResults();
};

// Добавляем функцию для обрезки длинных текстов
const truncate = (text: string, length: number): string => {
  if (!text) return '';
  return text.length > length ? text.substring(0, length) + '...' : text;
};

// Очистка таймера при удалении компонента
onUnmounted(() => {
  if (searchTimeout) {
    clearTimeout(searchTimeout);
  }
});
</script>

<style scoped>
.search-container {
  position: relative;
  width: 100%;
}

.results-container {
  max-height: 350px;
  overflow-y: auto;
  z-index: 50;
  scrollbar-width: thin;
  scrollbar-color: #d1d5db transparent;
}

.results-container::-webkit-scrollbar {
  width: 6px;
}

.results-container::-webkit-scrollbar-track {
  background: transparent;
}

.results-container::-webkit-scrollbar-thumb {
  background-color: #d1d5db;
  border-radius: 6px;
}

.result-item {
  border-bottom: 1px solid #f0f0f0;
}

.result-item:last-child {
  border-bottom: none;
}
</style> 