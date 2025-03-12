<template>
  <div class="players-page container mx-auto px-4 py-6">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
      <h1 class="text-2xl font-bold text-text-light dark:text-text-dark">Список игроков</h1>
      <router-link 
        v-if="userCanCreatePlayers" 
        to="/players/new" 
        class="mt-2 md:mt-0 btn-primary"
      >
        Добавить игрока
      </router-link>
    </div>

    <!-- Фильтры и поиск -->
    <div class="bg-white dark:bg-background-dark rounded-lg shadow p-4 mb-6 border border-border-light dark:border-border-dark">
      <div class="flex flex-wrap gap-4">
        <!-- Поиск -->
        <div class="flex-grow max-w-md">
          <label class="sr-only">Поиск</label>
          <div class="relative">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Поиск по имени или никнейму..." 
              class="w-full px-3 py-2 pl-10 border border-border-light dark:border-border-dark rounded-md bg-white dark:bg-background-dark text-text-light dark:text-text-dark"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <span class="text-text-secondary-light dark:text-text-secondary-dark">🔍</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Индикатор загрузки -->
    <div v-if="loading" class="bg-white dark:bg-background-dark rounded-lg shadow p-6 text-center border border-border-light dark:border-border-dark">
      <div class="flex justify-center items-center p-12">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary dark:border-primary-dark"></div>
      </div>
    </div>

    <!-- Сообщение об отсутствии игроков -->
    <div v-else-if="paginatedPlayers.length === 0" class="bg-white dark:bg-background-dark rounded-lg shadow p-6 text-center border border-border-light dark:border-border-dark">
      <p class="text-lg text-text-secondary-light dark:text-text-secondary-dark">Игроки не найдены</p>
    </div>

    <!-- Сетка карточек -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
      <div v-for="player in paginatedPlayers" :key="player.id" class="bg-white dark:bg-background-dark rounded-lg shadow hover:shadow-md transition-shadow border border-border-light dark:border-border-dark">
        <!-- Заголовок карточки с именем -->
        <div class="p-4 border-b border-border-light dark:border-border-dark">
          <h3 class="font-semibold text-lg truncate text-text-light dark:text-text-dark" @click="viewPlayerDetails(player)">{{ player.full_name }}</h3>
        </div>
        
        <!-- Основное содержимое карточки -->
        <div class="p-4 space-y-3">
          <!-- Никнеймы -->
          <div v-if="player.nicknames && player.nicknames.length > 0" class="flex flex-wrap gap-2">
            <span 
              v-for="nickname in player.nicknames.slice(0, 3)" 
              :key="nickname.id" 
              class="inline-block bg-primary/10 dark:bg-primary-dark/20 text-primary dark:text-primary-dark text-xs px-2 py-1 rounded"
            >
              {{ nickname.nickname }}
            </span>
            <span 
              v-if="player.nicknames.length > 3" 
              class="inline-block bg-surface-light dark:bg-surface-dark text-text-light dark:text-text-dark text-xs px-2 py-1 rounded"
            >
              +{{ player.nicknames.length - 3 }}
            </span>
          </div>
          
          <!-- Информация о кейсах -->
          <div class="border-t border-border-light dark:border-border-dark pt-2 mt-2">
            <div class="text-sm font-medium mb-1 text-text-light dark:text-text-dark">Кейсы:</div>
            <div class="flex flex-wrap gap-2">
              <router-link 
                :to="`/cases?player_id=${player.id}&status=active`" 
                class="px-2 py-1 bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300 rounded text-xs flex items-center"
              >
                <span class="mr-1">🟢</span>
                Активные: {{ getPlayerCaseCount(player.id, 'active') }}
              </router-link>
              <router-link 
                :to="`/cases?player_id=${player.id}&status=completed`" 
                class="px-2 py-1 bg-primary/10 dark:bg-primary-dark/20 text-primary dark:text-primary-dark rounded text-xs flex items-center"
              >
                <span class="mr-1">✅</span>
                Завершенные: {{ getPlayerCaseCount(player.id, 'completed') }}
              </router-link>
            </div>
            <div v-if="getPlayerTotalCaseCount(player.id) > 0" class="mt-1">
              <router-link 
                :to="`/cases?player_id=${player.id}`" 
                class="text-xs text-primary dark:text-primary-dark hover:text-primary-600 dark:hover:text-primary-500"
              >
                Все кейсы игрока →
              </router-link>
            </div>
            <div v-else class="text-xs text-text-secondary-light dark:text-text-secondary-dark mt-1">
              Нет активных кейсов
            </div>
          </div>
          
          <!-- Контакты -->
          <div v-if="player.contacts && player.contacts.length > 0" class="space-y-1">
            <div v-for="contact in player.contacts.slice(0, 2)" :key="contact.id" class="flex items-center text-sm text-text-light dark:text-text-dark">
              <span class="mr-1 w-16 text-text-secondary-light dark:text-text-secondary-dark">{{ getContactIcon(contact.type) }} {{ contact.type }}:</span>
              <span class="truncate">{{ contact.value }}</span>
            </div>
            <div v-if="player.contacts.length > 2" class="text-xs text-text-secondary-light dark:text-text-secondary-dark">
              и еще {{ player.contacts.length - 2 }} контакта(ов)
            </div>
          </div>
        </div>
        
        <!-- Футер карточки -->
        <div class="p-3 bg-surface-light dark:bg-surface-dark text-xs text-text-secondary-light dark:text-text-secondary-dark rounded-b-lg flex justify-between">
          <span>{{ formatDate(player.created_at) }}</span>
          <button 
            @click="viewPlayerDetails(player)" 
            class="text-primary dark:text-primary-dark hover:text-primary-600 dark:hover:text-primary-500"
          >
            Подробнее →
          </button>
        </div>
      </div>
    </div>

    <!-- Информация о количестве -->
    <div class="text-center text-text-secondary-light dark:text-text-secondary-dark mb-2">
      Найдено игроков: {{ totalPlayersCount }}
    </div>

    <!-- Пагинация -->
    <div class="flex justify-center mt-4 mb-6" v-if="totalPages > 1">
      <div class="flex space-x-2">
        <button 
          @click="goToPage(1)" 
          class="px-3 py-1 rounded border" 
          :class="currentPage === 1 ? 'opacity-50 cursor-not-allowed text-text-secondary-light dark:text-text-secondary-dark border-border-light dark:border-border-dark' : 'text-primary dark:text-primary-dark border-primary dark:border-primary-dark hover:bg-primary/10 dark:hover:bg-primary-dark/20'"
          :disabled="currentPage === 1"
        >
          &laquo;
        </button>
        
        <button 
          @click="goToPage(currentPage - 1)" 
          class="px-3 py-1 rounded border" 
          :class="currentPage === 1 ? 'opacity-50 cursor-not-allowed text-text-secondary-light dark:text-text-secondary-dark border-border-light dark:border-border-dark' : 'text-primary dark:text-primary-dark border-primary dark:border-primary-dark hover:bg-primary/10 dark:hover:bg-primary-dark/20'"
          :disabled="currentPage === 1"
        >
          &larr;
        </button>
        
        <button 
          v-for="page in paginationPages" 
          :key="page" 
          @click="goToPage(page)" 
          class="px-3 py-1 rounded border" 
          :class="currentPage === page ? 'bg-primary text-white border-primary dark:border-primary-dark' : 'text-primary dark:text-primary-dark border-primary dark:border-primary-dark hover:bg-primary/10 dark:hover:bg-primary-dark/20'"
        >
          {{ page }}
        </button>
        
        <button 
          @click="goToPage(currentPage + 1)" 
          class="px-3 py-1 rounded border" 
          :class="currentPage === totalPages ? 'opacity-50 cursor-not-allowed text-text-secondary-light dark:text-text-secondary-dark border-border-light dark:border-border-dark' : 'text-primary dark:text-primary-dark border-primary dark:border-primary-dark hover:bg-primary/10 dark:hover:bg-primary-dark/20'"
          :disabled="currentPage === totalPages"
        >
          &rarr;
        </button>
        
        <button 
          @click="goToPage(totalPages)" 
          class="px-3 py-1 rounded border" 
          :class="currentPage === totalPages ? 'opacity-50 cursor-not-allowed text-text-secondary-light dark:text-text-secondary-dark border-border-light dark:border-border-dark' : 'text-primary dark:text-primary-dark border-primary dark:border-primary-dark hover:bg-primary/10 dark:hover:bg-primary-dark/20'"
          :disabled="currentPage === totalPages"
        >
          &raquo;
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, reactive } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { usePlayersApi } from '@/api/players';
import type { Player } from '@/types/models';

const router = useRouter();
const route = useRoute();
const playersApi = ref<any>(null);
const authStore = useAuthStore();

// Состояние
const players = ref<Player[]>([]);
const loading = ref(true);
const searchQuery = ref('');
const currentPage = ref(1);
const itemsPerPage = 12;
const playerCases = ref<Record<string, any>>({});
const totalPlayersCount = ref(0);

// Проверка прав на создание игроков
const userCanCreatePlayers = computed(() => {
  return authStore.isAdmin || authStore.user?.role === 'manager';
});

// Функция загрузки данных с сервера с учетом фильтров и пагинации
const loadPlayers = async () => {
  loading.value = true;
  
  try {
    // Инициализируем API, если еще не сделано
    if (!playersApi.value) {
      playersApi.value = (await import('@/api/players')).usePlayersApi();
      console.log('API игроков инициализирован');
    }
    
    // Формируем параметры запроса
    const params: any = {
      skip: (currentPage.value - 1) * itemsPerPage, // вычисляем skip на основе страницы и лимита
      limit: itemsPerPage,
    };
    
    // Добавляем поисковый запрос, если он задан
    if (searchQuery.value.trim()) {
      params.search = searchQuery.value.trim();
    }
    
    console.log('Отправка запроса к API игроков с параметрами:', params);
    console.log('URL запроса:', `/players?${new URLSearchParams(params).toString()}`);
    
    // Получаем данные с сервера с учетом пагинации
    const response = await playersApi.value.getAccessiblePlayers(params);
    
    console.log('Получен ответ от API:', response);
    console.log('Структура ответа:', Object.keys(response));
    
    // Проверяем формат ответа
    if (Array.isArray(response)) {
      console.log('API вернул массив напрямую, конвертируем в ожидаемый формат');
      players.value = response;
      totalPlayersCount.value = response.length;
    } else {
      // Обновляем данные и общее количество
      players.value = response.results || [];
      totalPlayersCount.value = response.count || 0;
    }
    
    console.log(`Загружено ${players.value.length} игроков из ${totalPlayersCount.value}`);
    console.log('Текущая страница:', currentPage.value);
    console.log('Всего страниц:', totalPages.value);
    
    // Обновляем URL для сохранения состояния
    updateUrlParams();
    
    await fetchPlayerCases();
  } catch (error) {
    console.error('Ошибка при загрузке игроков:', error);
    if (error instanceof Error) {
      console.error('Детали ошибки:', error.message);
      console.error('Стек ошибки:', error.stack);
    }
    players.value = [];
    totalPlayersCount.value = 0;
  } finally {
    loading.value = false;
  }
};

// Переход на указанную страницу
const goToPage = (page: number) => {
  currentPage.value = page;
};

// Обновление URL-параметров для сохранения состояния фильтрации и пагинации
function updateUrlParams() {
  const params = new URLSearchParams();
  
  if (currentPage.value > 1) {
    params.set('page', currentPage.value.toString());
    // Добавляем также параметр skip для отладки (он не используется для навигации пользователя)
    params.set('debug_skip', ((currentPage.value - 1) * itemsPerPage).toString());
  }
  
  if (searchQuery.value.trim()) {
    params.set('search', searchQuery.value.trim());
  }
  
  const queryString = params.toString();
  const newUrl = queryString 
    ? `${window.location.pathname}?${queryString}` 
    : window.location.pathname;
  
  window.history.replaceState({}, '', newUrl);
  
  console.log('URL обновлен:', newUrl);
  console.log('Текущие параметры:', {
    page: currentPage.value,
    skip: (currentPage.value - 1) * itemsPerPage,
    search: searchQuery.value.trim() || undefined,
    limit: itemsPerPage
  });
}

// Определяем, какие игроки отображаются на текущей странице
const paginatedPlayers = computed(() => {
  return players.value;
});

// Общее количество страниц
const totalPages = computed(() => {
  return Math.max(1, Math.ceil(totalPlayersCount.value / itemsPerPage));
});

// Номера страниц для пагинации
const paginationPages = computed(() => {
  const total = totalPages.value;
  const current = currentPage.value;
  
  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1);
  }
  
  // Когда много страниц, показываем только часть с многоточиями
  const pages: Array<number | string> = [];
  
  if (current <= 3) {
    // В начале списка
    for (let i = 1; i <= 5; i++) {
      pages.push(i);
    }
    pages.push('...');
    pages.push(total);
  } else if (current >= total - 2) {
    // В конце списка
    pages.push(1);
    pages.push('...');
    for (let i = total - 4; i <= total; i++) {
      pages.push(i);
    }
  } else {
    // В середине списка
    pages.push(1);
    pages.push('...');
    for (let i = current - 1; i <= current + 1; i++) {
      pages.push(i);
    }
    pages.push('...');
    pages.push(total);
  }
  
  return pages;
});

// Функция для форматирования даты
const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('ru-RU', {
    year: 'numeric',
    month: 'short', 
    day: 'numeric'
  }).format(date);
};

// Переход к детальной информации об игроке
const viewPlayerDetails = (player: Player) => {
  router.push({ 
    path: `/players/${player.id}`
  });
};

// Получение иконки типа контакта
function getContactIcon(type: string): string {
  const icons: Record<string, string> = {
    'email': '✉️',
    'phone': '📱',
    'telegram': '📞',
    'whatsapp': '💬',
    'gipsyteam': '🎮',
    'vk': '👥',
    'facebook': '👤',
    'instagram': '📷',
    'twitter': '🐦',
    'skype': '🗣️',
    'discord': '💬',
    'other': '🔖'
  };
  return icons[type] || '📝';
}

// Функция для получения счетчика кейсов игрока по статусу
function getPlayerCaseCount(playerId: string, status: string): number {
  if (!playerCases.value[playerId]) {
    return 0;
  }
  return playerCases.value[playerId][status] || 0;
}

// Функция для получения общего количества кейсов игрока
function getPlayerTotalCaseCount(playerId: string): number {
  if (!playerCases.value[playerId]) {
    return 0;
  }
  return Object.values(playerCases.value[playerId])
    .reduce((sum: number, count: unknown) => sum + (typeof count === 'number' ? count : 0), 0);
}

// Функция для получения данных о кейсах игроков
async function fetchPlayerCases() {
  try {
    // В реальном приложении здесь был бы запрос к API
    // Для демонстрации заполним данными-заглушками
    for (const player of players.value) {
      // Генерируем случайные данные для демонстрации
      playerCases.value[player.id] = {
        active: Math.floor(Math.random() * 3),
        completed: Math.floor(Math.random() * 5),
        paused: Math.floor(Math.random() * 2),
      };
    }
  } catch (error) {
    console.error('Ошибка при получении данных о кейсах игроков:', error);
  }
}

// Изменяем watch, чтобы отслеживать изменения поискового запроса
watch(searchQuery, () => {
  currentPage.value = 1;
  loadPlayers();
});

// Загрузка данных при изменении страницы
watch(currentPage, () => {
  loadPlayers();
});

// Инициализация при монтировании компонента
onMounted(async () => {
  // Получаем параметры из URL
  const urlParams = new URLSearchParams(window.location.search);
  const page = Number(urlParams.get('page')) || 1;
  const search = urlParams.get('search') || '';
  
  // Устанавливаем параметры поиска
  currentPage.value = page;
  searchQuery.value = search;
  
  // Загружаем данные
  await loadPlayers();
});
</script>

<style scoped>
.players-list-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header-section {
  margin-bottom: 20px;
}

.players-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.player-card {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px;
  transition: all 0.2s;
  cursor: pointer;
  background-color: white;
}

.player-card:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transform: translateY(-2px);
}

.card-header {
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 12px;
  margin-bottom: 12px;
}

.card-content {
  min-height: 100px;
}

.card-footer {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e2e8f0;
}

.btn-details {
  background-color: #3b82f6;
  color: white;
  font-size: 0.875rem;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.btn-details:hover {
  background-color: #2563eb;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 24px;
}

.pagination-btn {
  background-color: #3b82f6;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 0.875rem;
  transition: background-color 0.2s;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #2563eb;
}
</style> 