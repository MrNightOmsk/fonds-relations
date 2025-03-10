<template>
  <div class="search-container">
    <div class="relative w-full">
      <div class="flex items-center border rounded-lg focus-within:ring-2 focus-within:ring-blue-500 bg-white">
        <span class="pl-3 text-gray-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </span>
        <input 
          type="text" 
          v-model="searchQuery" 
          @input="debouncedSearch" 
          placeholder="Поиск игроков, кейсов..." 
          class="w-full px-3 py-2.5 border-none focus:outline-none rounded-lg"
        />
        <button 
          v-if="searchQuery" 
          @click="clearSearch" 
          class="pr-3 text-gray-400 hover:text-gray-600"
          type="button"
        >
          <span>✕</span>
        </button>
      </div>
    </div>
    
    <!-- Фильтры для поиска -->
    <div v-if="(players.length > 0 || cases.length > 0) && searchQuery" class="mt-2 flex space-x-2 overflow-x-auto pb-1">
      <button 
        @click="activeFilter = 'all'" 
        class="px-3 py-1 text-xs rounded-full transition-colors whitespace-nowrap"
        :class="activeFilter === 'all' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
      >
        Все результаты ({{ players.length + cases.length }})
      </button>
      <button 
        v-if="players.length > 0"
        @click="activeFilter = 'players'" 
        class="px-3 py-1 text-xs rounded-full transition-colors whitespace-nowrap"
        :class="activeFilter === 'players' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
      >
        Только игроки ({{ players.length }})
      </button>
      <button 
        v-if="cases.length > 0"
        @click="activeFilter = 'cases'" 
        class="px-3 py-1 text-xs rounded-full transition-colors whitespace-nowrap"
        :class="activeFilter === 'cases' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
      >
        Только кейсы ({{ cases.length }})
      </button>
    </div>
    
    <!-- Индикатор загрузки -->
    <div v-if="loading" class="mt-2 p-3 text-center text-gray-500 bg-white rounded-lg border shadow-sm">
      <div class="flex items-center justify-center">
        <div class="animate-spin h-5 w-5 border-2 border-blue-500 rounded-full border-t-transparent mr-2"></div>
        <span>Идет поиск...</span>
      </div>
    </div>
    
    <!-- Сообщение "Ничего не найдено" -->
    <div v-else-if="searchPerformed && players.length === 0 && cases.length === 0" 
         class="mt-2 p-4 text-center text-gray-600 bg-white rounded-lg border shadow-sm">
      <div class="mb-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <p>По запросу <strong>"{{ searchQuery }}"</strong> ничего не найдено</p>
      <p class="text-sm text-gray-500 mt-1">Попробуйте изменить запрос или использовать другие ключевые слова</p>
    </div>
    
    <!-- Контейнер результатов -->
    <div v-else-if="(players.length > 0 || cases.length > 0) && searchQuery" 
      class="results-container mt-2 shadow-lg rounded-lg border overflow-hidden bg-white">
      
      <!-- Панель заголовка с количеством результатов -->
      <div class="bg-gray-50 px-4 py-2 border-b sticky top-0 z-20">
        <div class="flex justify-between items-center">
          <span class="text-sm text-gray-600">Найдено: {{ players.length + cases.length }}</span>
          <div class="flex space-x-2">
            <button @click="sortResults" class="text-xs px-2 py-1 rounded bg-white border text-gray-600 hover:bg-gray-50">
              <span v-if="sortDirection === 'asc'">↑ По имени</span>
              <span v-else>↓ По имени</span>
            </button>
          </div>
        </div>
      </div>
      
      <div class="overflow-auto max-h-[65vh]" ref="resultsContainer">
        <!-- Секция игроков -->
        <div v-if="players.length > 0 && (activeFilter === 'all' || activeFilter === 'players')" class="section">
          <h3 class="bg-gray-100 px-4 py-2.5 font-medium text-sm sticky top-0 z-10 border-b">
            Игроки <span class="text-gray-500 text-xs">({{ players.length }})</span>
          </h3>
          
          <div v-for="player in players" :key="player.id" 
               @click="selectResult('player', player)"
               class="player-card p-4 hover:bg-blue-50 cursor-pointer border-b border-gray-100 transition-colors">
            
            <!-- Основная информация об игроке с аватаром -->
            <div class="flex">
              <!-- Аватар игрока (заглушка) -->
              <div class="w-12 h-12 rounded-full bg-gray-200 flex-shrink-0 mr-3 overflow-hidden flex items-center justify-center text-gray-600">
                {{ player.full_name ? player.full_name.charAt(0).toUpperCase() : '?' }}
              </div>
              
              <div class="flex-grow">
                <!-- Верхняя часть карточки с именем и фондом -->
                <div class="flex justify-between items-start">
                  <div class="font-medium text-blue-700 text-lg">{{ player.full_name }}</div>
                  <div v-if="player.fund_name" class="text-xs py-1 px-2 bg-gray-100 rounded-full text-gray-600">
                    {{ player.fund_name }}
                  </div>
                </div>
                
                <!-- Информация об игроке -->
                <div class="mt-1.5 space-y-1.5">
                  <!-- Дополнительная информация: имя, фамилия, отчество -->
                  <div v-if="player.first_name || player.last_name || player.middle_name" class="text-sm text-gray-600">
                    <span v-if="player.first_name">Имя: {{ player.first_name }}</span>
                    <span v-if="player.last_name" class="ml-2">Фамилия: {{ player.last_name }}</span>
                    <span v-if="player.middle_name" class="ml-2">Отчество: {{ player.middle_name }}</span>
                  </div>
                  
                  <!-- Дата рождения -->
                  <div v-if="player.birth_date" class="text-xs text-gray-600 flex items-center gap-1.5">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    Дата рождения: {{ formatDate(player.birth_date) }}
                  </div>
                  
                  <!-- Описание игрока -->
                  <div v-if="player.description" class="text-sm text-gray-600">
                    {{ truncate(player.description, 100) }}
                  </div>
                  
                  <!-- Локация: город/страна -->
                  <div v-if="player.locations && player.locations.length" class="text-xs text-gray-600 flex items-center gap-1.5">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    {{ player.locations.join(', ') }}
                  </div>
                  
                  <!-- Никнеймы -->
                  <div v-if="player.nicknames && player.nicknames.length" class="flex flex-wrap gap-1.5 mt-1.5">
                    <span v-for="(nickname, idx) in player.nicknames.slice(0, 3)" :key="idx"
                          class="text-xs bg-blue-50 py-0.5 px-1.5 rounded text-blue-700 border border-blue-100">
                      <span class="font-medium">{{ nickname.nickname }}</span> <span class="text-gray-500">({{ nickname.room }})</span>
                    </span>
                    <span v-if="player.nicknames.length > 3" class="text-xs px-1.5 py-0.5 bg-gray-50 rounded text-gray-500">
                      +{{ player.nicknames.length - 3 }}
                    </span>
                  </div>
                  
                  <!-- Контакты с иконкой -->
                  <div v-if="player.contacts && player.contacts.length" class="text-xs text-gray-600 flex items-center gap-1.5">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                    {{ truncate(player.contacts[0], 30) }}
                    <span v-if="player.contacts.length > 1" class="text-xs text-gray-500">(+{{ player.contacts.length - 1 }})</span>
                  </div>
                  
                  <!-- Статистика по кейсам с цветовой индикацией -->
                  <div v-if="player.cases_count !== undefined" class="flex justify-between mt-2">
                    <div class="text-xs text-gray-500">
                      <span :class="{'text-yellow-600 font-medium': player.cases_count > 0}">
                        Кейсов: {{ player.cases_count }}
                      </span>
                      <span v-if="player.latest_case_date" class="ml-1">
                        (последний: {{ formatDate(player.latest_case_date) }})
                      </span>
                      <div v-if="player.updated_at" class="mt-1 text-xs text-gray-400">
                        Обновлено: {{ formatDate(player.updated_at) }}
                      </div>
                    </div>
                    
                    <!-- Кнопки быстрых действий -->
                    <div class="flex gap-2">
                      <button @click.stop="selectResult('player', player)" 
                              class="text-xs py-1 px-2 bg-blue-50 text-blue-700 rounded hover:bg-blue-100 transition-colors">
                        Профиль
                      </button>
                      <button @click.stop="createCaseForPlayer(player)" 
                              class="text-xs py-1 px-2 bg-green-50 text-green-700 rounded hover:bg-green-100 transition-colors">
                        Создать кейс
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Кнопка "Показать больше" для игроков -->
          <div v-if="hasMorePlayers" class="p-3 text-center border-t">
            <button @click="loadMorePlayers" class="text-sm text-blue-600 hover:text-blue-800">
              Показать больше игроков
            </button>
          </div>
        </div>
        
        <!-- Секция кейсов -->
        <div v-if="cases.length > 0 && (activeFilter === 'all' || activeFilter === 'cases')" class="section">
          <h3 class="bg-gray-100 px-4 py-2.5 font-medium text-sm sticky top-0 z-10 border-b">
            Кейсы <span class="text-gray-500 text-xs">({{ cases.length }})</span>
          </h3>
          
          <div v-for="case_item in cases" :key="case_item.id" 
               class="case-card p-4 hover:bg-blue-50 cursor-pointer border-b border-gray-100 transition-colors">
            
            <!-- Заголовок кейса с иконкой -->
            <div class="flex items-start">
              <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div class="flex-grow">
                <div class="font-medium text-blue-700 text-lg">{{ case_item.title }}</div>
                
                <!-- Статус кейса -->
                <div class="mt-2 flex flex-wrap gap-2 items-center">
                  <span class="text-xs py-0.5 px-2 rounded-full" 
                        :class="getCaseStatusClass(case_item.status)">
                    {{ getCaseStatusText(case_item.status) }}
                  </span>
                  
                  <span v-if="case_item.created_at" class="text-xs text-gray-500 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    Создан: {{ formatDate(case_item.created_at) }}
                  </span>
                </div>
                
                <!-- Информация об игроке -->
                <div v-if="case_item.player_name" class="mt-2 text-sm text-gray-600 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  Игрок: <span class="font-medium ml-1">{{ case_item.player_name }}</span>
                  <span v-if="case_item.fund_name" class="text-xs ml-1 py-0.5 px-1.5 bg-gray-100 rounded-full">{{ case_item.fund_name }}</span>
                </div>
                
                <!-- Кнопки действий -->
                <div class="mt-3 flex justify-end gap-2">
                  <button @click.stop="selectResult('case', case_item)" 
                          class="text-xs py-1 px-2 bg-blue-50 text-blue-700 rounded hover:bg-blue-100 transition-colors">
                    Открыть кейс
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Кнопка "Показать больше" для кейсов -->
          <div v-if="hasMoreCases" class="p-3 text-center border-t">
            <button @click="loadMoreCases" class="text-sm text-blue-600 hover:text-blue-800">
              Показать больше кейсов
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useSearchApi } from '@/api/search';
import type { SearchPlayer, SearchCase } from '@/types/search';

// Объявление пропсов
const props = defineProps({
  maxResults: { type: Number, default: 10 },
  highlightResults: { type: Boolean, default: true }
});

// Объявление эмиттера событий
const emit = defineEmits(['select', 'create-case']);

// Состояние компонента
const router = useRouter();
const searchApi = useSearchApi();
const searchQuery = ref('');
const allPlayers = ref<SearchPlayer[]>([]);
const allCases = ref<SearchCase[]>([]);
const visiblePlayersCount = ref(5);
const visibleCasesCount = ref(5);
const loading = ref(false);
const searchPerformed = ref(false);
const activeFilter = ref('all');
const sortDirection = ref('asc');
const resultsContainer = ref<HTMLElement | null>(null);
const searchTimeout = ref<number | null>(null);

// Вычисляемые свойства для фильтрации и сортировки
const players = computed(() => {
  return allPlayers.value.slice(0, visiblePlayersCount.value);
});

const cases = computed(() => {
  return allCases.value.slice(0, visibleCasesCount.value);
});

const hasMorePlayers = computed(() => {
  return visiblePlayersCount.value < allPlayers.value.length;
});

const hasMoreCases = computed(() => {
  return visibleCasesCount.value < allCases.value.length;
});

// Функция для загрузки большего количества игроков
const loadMorePlayers = () => {
  visiblePlayersCount.value += 5;
};

// Функция для загрузки большего количества кейсов
const loadMoreCases = () => {
  visibleCasesCount.value += 5;
};

// Функция для сортировки результатов
const sortResults = () => {
  sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
  
  // Сортировка игроков
  allPlayers.value.sort((a, b) => {
    const nameA = a.full_name || '';
    const nameB = b.full_name || '';
    
    if (sortDirection.value === 'asc') {
      return nameA.localeCompare(nameB);
    } else {
      return nameB.localeCompare(nameA);
    }
  });
  
  // Сортировка кейсов
  allCases.value.sort((a, b) => {
    const titleA = a.title || '';
    const titleB = b.title || '';
    
    if (sortDirection.value === 'asc') {
      return titleA.localeCompare(titleB);
    } else {
      return titleB.localeCompare(titleA);
    }
  });
};

// Функция для создания кейса для игрока
const createCaseForPlayer = (player: SearchPlayer) => {
  emit('create-case', player);
  router.push({
    path: '/cases/create',
    query: { player_id: player.id }
  });
};

// Функция для дебаунса поиска
const debouncedSearch = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value);
  }
  
  if (searchQuery.value.trim().length === 0) {
    clearResults();
    return;
  }
  
  searchTimeout.value = window.setTimeout(() => {
    performSearch();
  }, 300); // 300ms задержка
};

// Очистка результатов
const clearResults = () => {
  allPlayers.value = [];
  allCases.value = [];
  visiblePlayersCount.value = 5;
  visibleCasesCount.value = 5;
  searchPerformed.value = false;
  // Сбрасываем активный фильтр
  activeFilter.value = 'all';
};

// Очистка поиска
const clearSearch = () => {
  searchQuery.value = '';
  clearResults();
};

// Изменяем функцию performSearch, чтобы не использовать моковые данные
async function performSearch() {
  if (!searchQuery.value || searchQuery.value.trim().length === 0) {
    return;
  }

  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value);
  }

  searchTimeout.value = window.setTimeout(async () => {
    if (!searchQuery.value || searchQuery.value.trim().length === 0) {
      return;
    }

    if (searchQuery.value.trim().length < 2) {
      allPlayers.value = [];
      allCases.value = [];
      return;
    }

    loading.value = true;
    searchPerformed.value = true;

    try {
      // Получаем исходный запрос пользователя
      const query = searchQuery.value;
      
      console.log('Выполняем поиск с запросом:', query);
      
      const result = await searchApi.unifiedSearch(query);
      console.log('Результаты поиска API:', result);
      
      // Обновляем результаты поиска
      allPlayers.value = result.players || [];
      allCases.value = result.cases || [];
      
      console.log('Загружено игроков:', allPlayers.value.length);
      console.log('Загружено кейсов:', allCases.value.length);
      
      // Сортируем результаты по умолчанию
      sortResults();
    } catch (error) {
      console.error('Ошибка при выполнении поиска:', error);
      // В случае ошибки очищаем результаты
      allPlayers.value = [];
      allCases.value = [];
    } finally {
      loading.value = false;
    }
  }, 300); // Задержка для избежания слишком частых запросов при вводе
}

// Форматирование даты
const formatDate = (dateString: string): string => {
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  } catch (e) {
    return dateString;
  }
};

// Получение класса для статуса кейса
const getCaseStatusClass = (status: string): string => {
  const statusClasses: Record<string, string> = {
    'open': 'bg-green-100 text-green-700',
    'in_progress': 'bg-blue-100 text-blue-700',
    'resolved': 'bg-purple-100 text-purple-700',
    'closed': 'bg-gray-100 text-gray-700'
  };
  
  return statusClasses[status] || 'bg-gray-100 text-gray-600';
};

// Получение текста для статуса кейса
const getCaseStatusText = (status: string): string => {
  const statusMap: Record<string, string> = {
    'open': 'Открыт',
    'in_progress': 'В работе',
    'resolved': 'Решён',
    'closed': 'Закрыт'
  };
  
  return statusMap[status] || status;
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
  const parts: string[] = [];
  
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
  clearSearch();
};

// Добавляем функцию для обрезки длинных текстов
const truncate = (text: string, length: number): string => {
  if (!text) return '';
  return text.length > length ? text.substring(0, length) + '...' : text;
};

// Очистка таймера при удалении компонента
onUnmounted(() => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value);
  }
});

// Добавление слушателя события скролла
onMounted(() => {
  if (resultsContainer.value) {
    resultsContainer.value.addEventListener('scroll', handleScroll);
  }
});

// Удаление слушателя события скролла при размонтировании
onUnmounted(() => {
  if (resultsContainer.value) {
    resultsContainer.value.removeEventListener('scroll', handleScroll);
  }
});

// Обработчик события скролла для подгрузки результатов
const handleScroll = (e: Event) => {
  const target = e.target as HTMLElement;
  const scrollBottom = target.scrollHeight - target.scrollTop - target.clientHeight;
  
  // Если скролл почти достиг дна (осталось 50px), загружаем больше результатов
  if (scrollBottom < 50) {
    if (activeFilter.value === 'players' || activeFilter.value === 'all') {
      if (hasMorePlayers.value) {
        loadMorePlayers();
      }
    }
    
    if (activeFilter.value === 'cases' || activeFilter.value === 'all') {
      if (hasMoreCases.value) {
        loadMoreCases();
      }
    }
  }
};

// Заменяем вызов функции search на performSearch
// Находим место, где вызывается search и меняем на performSearch

watch(searchQuery, () => {
  if (searchQuery.value.trim().length === 0) {
    clearResults();
  } else {
    performSearch();
  }
});
</script>

<style scoped>
.search-container {
  position: relative;
  width: 100%;
}

.results-container {
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.player-card, .case-card {
  transition: all 0.2s ease;
}

.player-card:hover, .case-card:hover {
  background-color: #f0f7ff;
}

/* Анимация появления результатов */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.section {
  animation: fadeIn 0.3s ease-out;
}

/* Стилизация скроллбара */
.results-container::-webkit-scrollbar {
  width: 8px;
}

.results-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.results-container::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 4px;
}

.results-container::-webkit-scrollbar-thumb:hover {
  background: #999;
}
</style> 