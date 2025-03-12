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
              @input="filterPlayers"
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

    <!-- Пагинация -->
    <div class="flex justify-center mt-6" v-if="totalPages > 1">
      <div class="flex space-x-2">
        <button 
          @click="currentPage > 1 && (currentPage--)" 
          class="px-3 py-1 rounded border" 
          :class="currentPage === 1 ? 'text-text-secondary-light dark:text-text-secondary-dark border-border-light dark:border-border-dark' : 'text-primary dark:text-primary-dark border-primary dark:border-primary-dark hover:bg-primary/10 dark:hover:bg-primary-dark/20'"
          :disabled="currentPage === 1"
        >
          &larr;
        </button>
        
        <button 
          v-for="page in paginationPages" 
          :key="page" 
          @click="currentPage = page" 
          class="px-3 py-1 rounded border" 
          :class="currentPage === page ? 'bg-primary text-white border-primary dark:border-primary-dark' : 'text-primary dark:text-primary-dark border-primary dark:border-primary-dark hover:bg-primary/10 dark:hover:bg-primary-dark/20'"
        >
          {{ page }}
        </button>
        
        <button 
          @click="currentPage < totalPages && (currentPage++)" 
          class="px-3 py-1 rounded border" 
          :class="currentPage === totalPages ? 'text-text-secondary-light dark:text-text-secondary-dark border-border-light dark:border-border-dark' : 'text-primary dark:text-primary-dark border-primary dark:border-primary-dark hover:bg-primary/10 dark:hover:bg-primary-dark/20'"
          :disabled="currentPage === totalPages"
        >
          &rarr;
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// @ts-ignore
import { ref, computed, onMounted } from 'vue';
// @ts-ignore
import { useRouter } from 'vue-router';
// @ts-ignore
import { usePlayersApi } from '@/api/players';
// @ts-ignore
import { useAuthStore } from '@/stores/auth';
// @ts-ignore
import type { Player } from '@/types/models';

const router = useRouter();
const playersApi = usePlayersApi();
const authStore = useAuthStore();

// Состояние
const players = ref<Player[]>([]);
const loading = ref(true);
const searchQuery = ref('');
const currentPage = ref(1);
const itemsPerPage = 12;
const playerCases = ref<Record<string, any>>({});

// Проверка прав на создание игроков
const userCanCreatePlayers = computed(() => {
  return authStore.isAdmin || authStore.user?.role === 'manager';
});

// Функция загрузки данных
const loadPlayers = async () => {
  loading.value = true;
  try {
    players.value = await playersApi.getPlayers();
    await fetchPlayerCases();
  } catch (error) {
    console.error('Ошибка при загрузке игроков:', error);
  } finally {
    loading.value = false;
  }
};

// Фильтрация игроков
const filterPlayers = () => {
  currentPage.value = 1; // Сбрасываем пагинацию при поиске
};

// Фильтрованные игроки
const filteredPlayers = computed(() => {
  let result = players.value;
  
  // Фильтрация по поисковому запросу
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(player => {
      // Поиск по полному имени
      if (player.full_name && player.full_name.toLowerCase().includes(query)) {
        return true;
      }
      
      // Поиск по никнеймам
      if (player.nicknames && player.nicknames.some(n => n.nickname.toLowerCase().includes(query))) {
        return true;
      }
      
      // Поиск по контактам
      if (player.contacts && player.contacts.some(c => c.value && c.value.toLowerCase().includes(query))) {
        return true;
      }
      
      return false;
    });
  }
  
  // Удаляем фильтрацию по фонду - все менеджеры должны видеть всех игроков
  // в соответствии с новыми требованиями
  
  return result;
});

// Пагинация
const paginatedPlayers = computed(() => {
  const startIndex = (currentPage.value - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  return filteredPlayers.value.slice(startIndex, endIndex);
});

// Общее количество страниц
const totalPages = computed(() => {
  return Math.ceil(filteredPlayers.value.length / itemsPerPage);
});

// Номера страниц для пагинации
const paginationPages = computed(() => {
  const pages: number[] = [];
  const maxVisiblePages = 5;
  let startPage = Math.max(1, currentPage.value - Math.floor(maxVisiblePages / 2));
  let endPage = Math.min(totalPages.value, startPage + maxVisiblePages - 1);
  
  if (endPage - startPage + 1 < maxVisiblePages) {
    startPage = Math.max(1, endPage - maxVisiblePages + 1);
  }
  
  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
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

// Хуки жизненного цикла
onMounted(() => {
  loadPlayers();
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