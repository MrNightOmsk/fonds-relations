<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">Управление игроками</h2>
      <button @click="showCreateModal = true" class="btn-primary">
        Создать игрока
      </button>
    </div>

    <!-- Фильтры -->
    <div class="mb-4 flex space-x-4">
      <div class="flex items-center">
        <label class="mr-2 text-sm font-medium text-gray-700">Фонд:</label>
        <select v-model="fundFilter" class="px-3 py-2 border border-gray-300 rounded-md text-sm">
          <option value="">Все</option>
          <option v-for="fund in funds" :key="fund.id" :value="fund.id">
            {{ fund.name }}
          </option>
        </select>
      </div>
    </div>
    
    <!-- Таблица игроков -->
    <div class="overflow-x-auto bg-white rounded-lg shadow">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Имя
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Email
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Телефон
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Фонд
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Создан
            </th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              Действия
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-if="loading">
            <td colspan="6" class="px-6 py-4 text-center">Загрузка...</td>
          </tr>
          <tr v-else-if="filteredPlayers.length === 0">
            <td colspan="6" class="px-6 py-4 text-center">Игроки не найдены</td>
          </tr>
          <tr v-for="player in filteredPlayers" :key="player.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">
              {{ player.name }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              {{ player.email || 'Не указан' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              {{ player.phone || 'Не указан' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              {{ getFundName(player.created_by_fund_id) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ new Date(player.created_at).toLocaleDateString() }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button @click="editPlayer(player)" class="text-blue-600 hover:text-blue-900 mr-3">
                Изменить
              </button>
              <button @click="confirmDeletePlayer(player)" class="text-red-600 hover:text-red-900">
                Удалить
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Модальное окно создания/редактирования игрока -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full">
        <h3 class="text-lg font-semibold mb-4">
          {{ showEditModal ? 'Редактирование игрока' : 'Создание игрока' }}
        </h3>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Имя</label>
          <input 
            type="text" 
            v-model="formData.name" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
            required
          >
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input 
            type="email" 
            v-model="formData.email" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
          >
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Телефон</label>
          <input 
            type="tel" 
            v-model="formData.phone" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
          >
        </div>
        
        <div class="flex justify-end space-x-2">
          <button 
            @click="closeModal" 
            class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
          >
            Отмена
          </button>
          <button 
            @click="savePlayer" 
            class="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-dark"
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? 'Сохранение...' : 'Сохранить' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Модальное окно подтверждения удаления -->
    <div v-if="showDeleteConfirm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full">
        <h3 class="text-lg font-semibold mb-4">Подтверждение удаления</h3>
        <p class="mb-4 text-gray-700">
          Вы уверены, что хотите удалить игрока "{{ playerToDelete?.name }}"? Это действие необратимо.
        </p>
        <div class="flex justify-end space-x-2">
          <button 
            @click="showDeleteConfirm = false" 
            class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
          >
            Отмена
          </button>
          <button 
            @click="deletePlayerConfirmed" 
            class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? 'Удаление...' : 'Удалить' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// @ts-ignore
import { ref, onMounted, computed } from 'vue';
// @ts-ignore
import { usePlayersApi } from '@/api/players';
// @ts-ignore
import { useFundsApi } from '@/api/funds';
// @ts-ignore
import type { Player, CreatePlayerRequest, UpdatePlayerRequest, Fund } from '@/types/models';

// API клиенты
const playersApi = usePlayersApi();
const fundsApi = useFundsApi();

// Состояние
const players = ref<Player[]>([]);
const funds = ref<Fund[]>([]);
const loading = ref(true);
const showCreateModal = ref(false);
const showEditModal = ref(false);
const showDeleteConfirm = ref(false);
const isSubmitting = ref(false);
const currentPlayerId = ref<string | null>(null);
const playerToDelete = ref<Player | null>(null);

// Фильтры
const fundFilter = ref('');

// Форма
const defaultFormData: CreatePlayerRequest = {
  name: '',
  email: '',
  phone: ''
};

const formData = ref<CreatePlayerRequest | UpdatePlayerRequest>({ ...defaultFormData });

// Получение отфильтрованных игроков
const filteredPlayers = computed(() => {
  let result = [...players.value];
  
  if (fundFilter.value) {
    result = result.filter(p => p.created_by_fund_id === fundFilter.value);
  }
  
  return result.sort((a, b) => {
    // Сортировка по имени
    return a.name.localeCompare(b.name);
  });
});

// Получение данных
async function fetchPlayers() {
  loading.value = true;
  try {
    players.value = await playersApi.getPlayers();
  } catch (error) {
    console.error('Ошибка при получении игроков:', error);
  } finally {
    loading.value = false;
  }
}

async function fetchFunds() {
  try {
    funds.value = await fundsApi.getFunds();
  } catch (error) {
    console.error('Ошибка при получении фондов:', error);
  }
}

// Получение данных о связанных объектах
function getFundName(fundId: string): string {
  const fund = funds.value.find(f => f.id === fundId);
  return fund ? fund.name : 'Неизвестный фонд';
}

// Обработчики для CRUD
function editPlayer(player: Player) {
  currentPlayerId.value = player.id;
  formData.value = {
    name: player.name,
    email: player.email || '',
    phone: player.phone || ''
  };
  showEditModal.value = true;
}

function confirmDeletePlayer(player: Player) {
  playerToDelete.value = player;
  showDeleteConfirm.value = true;
}

async function deletePlayerConfirmed() {
  if (!playerToDelete.value) return;
  
  isSubmitting.value = true;
  try {
    await playersApi.deletePlayer(playerToDelete.value.id);
    
    // Удаляем из локального состояния
    players.value = players.value.filter(p => p.id !== playerToDelete.value?.id);
    showDeleteConfirm.value = false;
  } catch (error: any) {
    alert(`Ошибка: ${error.response?.data?.detail || 'Что-то пошло не так'}`);
  } finally {
    isSubmitting.value = false;
  }
}

async function savePlayer() {
  isSubmitting.value = true;
  try {
    if (showEditModal.value && currentPlayerId.value) {
      // Обновление игрока
      const updatedPlayer = await playersApi.updatePlayer(currentPlayerId.value, formData.value as UpdatePlayerRequest);
      
      // Обновляем игрока в локальном состоянии
      const index = players.value.findIndex(p => p.id === updatedPlayer.id);
      if (index !== -1) {
        players.value[index] = updatedPlayer;
      }
    } else {
      // Создание игрока
      const newPlayer = await playersApi.createPlayer(formData.value as CreatePlayerRequest);
      players.value.push(newPlayer);
    }
    
    closeModal();
  } catch (error: any) {
    alert(`Ошибка: ${error.response?.data?.detail || 'Что-то пошло не так'}`);
  } finally {
    isSubmitting.value = false;
  }
}

function closeModal() {
  showCreateModal.value = false;
  showEditModal.value = false;
  currentPlayerId.value = null;
  formData.value = { ...defaultFormData };
}

// Загрузка данных при монтировании
onMounted(async () => {
  await Promise.all([
    fetchPlayers(),
    fetchFunds()
  ]);
});
</script> 