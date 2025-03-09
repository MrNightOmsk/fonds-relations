<template>
  <div class="players-list-container">
    <div class="header-section">
      <h1 class="text-2xl font-bold mb-4">Список игроков</h1>
      <div class="flex items-center gap-2 mb-4">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Поиск игроков..."
          class="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          @input="filterPlayers"
        />
      </div>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>

    <div v-else-if="filteredPlayers.length === 0" class="py-12 text-center text-gray-500">
      <p>Игроки не найдены</p>
    </div>

    <div v-else class="players-grid">
      <div v-for="player in filteredPlayers" :key="player.id" class="player-card" @click="viewPlayerDetails(player)">
        <div class="card-header">
          <h3 class="text-lg font-bold">{{ player.full_name }}</h3>
        </div>
        <div class="card-content">
          <div v-if="player.nicknames && player.nicknames.length > 0" class="mb-2">
            <p class="text-sm text-gray-600">Никнеймы:</p>
            <p class="text-sm">
              {{ player.nicknames.map(nick => nick.nickname).join(', ') }}
            </p>
          </div>
          <div v-if="player.contacts && player.contacts.length > 0" class="mb-2">
            <p class="text-sm text-gray-600">Контакты:</p>
            <p v-for="contact in player.contacts.slice(0, 2)" :key="contact.id" class="text-sm">
              {{ contact.type }}: {{ contact.value }}
            </p>
            <p v-if="player.contacts.length > 2" class="text-sm text-blue-500">
              +{{ player.contacts.length - 2 }} ещё...
            </p>
          </div>
        </div>
        <div class="card-footer flex justify-between items-center">
          <span class="text-xs text-gray-500">Создан: {{ formatDate(player.created_at) }}</span>
          <button class="btn-details" @click.stop="viewPlayerDetails(player)">
            Подробнее
          </button>
        </div>
      </div>
    </div>

    <div class="pagination-controls" v-if="filteredPlayers.length > 0">
      <button 
        :disabled="currentPage === 1" 
        @click="currentPage--" 
        class="pagination-btn"
        :class="{ 'opacity-50 cursor-not-allowed': currentPage === 1 }"
      >
        Предыдущая
      </button>
      <span>Страница {{ currentPage }} из {{ totalPages }}</span>
      <button 
        :disabled="currentPage === totalPages" 
        @click="currentPage++" 
        class="pagination-btn"
        :class="{ 'opacity-50 cursor-not-allowed': currentPage === totalPages }"
      >
        Следующая
      </button>
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
import type { Player } from '@/types/models';

const router = useRouter();
const playersApi = usePlayersApi();

// Состояние
const players = ref<Player[]>([]);
const loading = ref(true);
const searchQuery = ref('');
const currentPage = ref(1);
const itemsPerPage = 12;

// Функция загрузки данных
const loadPlayers = async () => {
  loading.value = true;
  try {
    players.value = await playersApi.getPlayers();
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

// Вычисляемые свойства
const filteredPlayers = computed(() => {
  let result = players.value;
  
  // Фильтрация по поисковому запросу
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(player => {
      return (
        player.full_name.toLowerCase().includes(query) ||
        (player.nicknames && player.nicknames.some(nick => nick.nickname.toLowerCase().includes(query)))
      );
    });
  }
  
  // Пагинация
  const startIndex = (currentPage.value - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  return result.slice(startIndex, endIndex);
});

const totalPages = computed(() => {
  if (players.value.length === 0) return 1;
  
  let filtered = players.value;
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(player => {
      return (
        player.full_name.toLowerCase().includes(query) ||
        (player.nicknames && player.nicknames.some(nick => nick.nickname.toLowerCase().includes(query)))
      );
    });
  }
  
  return Math.ceil(filtered.length / itemsPerPage);
});

// Методы
const viewPlayerDetails = (player: Player) => {
  router.push({ name: 'PlayerDetail', params: { id: player.id } });
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('ru-RU', {
    year: 'numeric',
    month: 'short', 
    day: 'numeric'
  }).format(date);
};

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