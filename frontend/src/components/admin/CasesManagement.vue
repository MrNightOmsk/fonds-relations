<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">Управление кейсами</h2>
      <button @click="showCreateModal = true" class="btn-primary">
        Создать кейс
      </button>
    </div>

    <!-- Фильтры -->
    <div class="mb-4 flex space-x-4">
      <div class="flex items-center">
        <label class="mr-2 text-sm font-medium text-gray-700">Статус:</label>
        <select v-model="statusFilter" class="px-3 py-2 border border-gray-300 rounded-md text-sm">
          <option value="">Все</option>
          <option value="open">Открыт</option>
          <option value="in_progress">В работе</option>
          <option value="closed">Закрыт</option>
        </select>
      </div>
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
    
    <!-- Таблица кейсов -->
    <div class="overflow-x-auto bg-white rounded-lg shadow">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Название
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Статус
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Игрок
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
          <tr v-else-if="filteredCases.length === 0">
            <td colspan="6" class="px-6 py-4 text-center">Кейсы не найдены</td>
          </tr>
          <tr v-for="case_item in filteredCases" :key="case_item.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">
              {{ case_item.title }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" 
                :class="{
                  'bg-green-100 text-green-800': case_item.status === 'open',
                  'bg-yellow-100 text-yellow-800': case_item.status === 'in_progress',
                  'bg-red-100 text-red-800': case_item.status === 'closed'
                }">
                {{ getStatusText(case_item.status) }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              {{ getPlayerName(case_item.player_id) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              {{ getFundName(case_item.created_by_fund_id) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ new Date(case_item.created_at).toLocaleDateString() }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button @click="editCase(case_item)" class="text-blue-600 hover:text-blue-900 mr-3">
                Изменить
              </button>
              <button @click="confirmDeleteCase(case_item)" class="text-red-600 hover:text-red-900">
                Удалить
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Модальное окно создания/редактирования кейса -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full">
        <h3 class="text-lg font-semibold mb-4">
          {{ showEditModal ? 'Редактирование кейса' : 'Создание кейса' }}
        </h3>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Название</label>
          <input 
            type="text" 
            v-model="formData.title" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
            required
          >
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Описание</label>
          <textarea 
            v-model="formData.description" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
            rows="3"
          ></textarea>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Статус</label>
          <select 
            v-model="formData.status" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
          >
            <option value="open">Открыт</option>
            <option value="in_progress">В работе</option>
            <option value="closed">Закрыт</option>
          </select>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Игрок</label>
          <select 
            v-model="formData.player_id" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
          >
            <option value="">Не выбран</option>
            <option v-for="player in players" :key="player.id" :value="player.id">
              {{ player.full_name || `${player.first_name} ${player.last_name}` }}
            </option>
          </select>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Тип арбитража</label>
          <input 
            type="text" 
            v-model="formData.arbitrage_type" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
            placeholder="Например: штраф, компенсация"
          >
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Сумма арбитража</label>
          <input 
            type="number" 
            v-model="formData.arbitrage_amount" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
            min="0"
            step="0.01"
          >
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Валюта арбитража</label>
          <select 
            v-model="formData.arbitrage_currency" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
          >
            <option value="USD">USD</option>
            <option value="EUR">EUR</option>
            <option value="RUB">RUB</option>
          </select>
        </div>
        
        <div class="flex justify-end space-x-2">
          <button 
            @click="closeModal" 
            class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
          >
            Отмена
          </button>
          <button 
            @click="saveCase" 
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
          Вы уверены, что хотите удалить кейс "{{ caseToDelete?.title }}"? Это действие необратимо.
        </p>
        <div class="flex justify-end space-x-2">
          <button 
            @click="showDeleteConfirm = false" 
            class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
          >
            Отмена
          </button>
          <button 
            @click="deleteCaseConfirmed" 
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
import { useCasesApi } from '@/api/cases';
// @ts-ignore
import { useFundsApi } from '@/api/funds';
// @ts-ignore
import { usePlayersApi } from '@/api/players';
// @ts-ignore
import type { CaseExtended, CaseCreate, CaseUpdate, Fund, Player, CaseStatus } from '@/types/models';

// API клиенты
const casesApi = useCasesApi();
const fundsApi = useFundsApi();
const playersApi = usePlayersApi();

// Состояние
const cases = ref<CaseExtended[]>([]);
const funds = ref<Fund[]>([]);
const players = ref<Player[]>([]);
const loading = ref(true);
const showCreateModal = ref(false);
const showEditModal = ref(false);
const showDeleteConfirm = ref(false);
const isSubmitting = ref(false);
const currentCaseId = ref<string | null>(null);
const caseToDelete = ref<CaseExtended | null>(null);

// Фильтры
const statusFilter = ref('');
const fundFilter = ref('');

// Форма
const defaultFormData: CaseCreate = {
  title: '',
  description: '',
  status: 'open',
  player_id: '',
  arbitrage_type: '',
  arbitrage_amount: 0,
  arbitrage_currency: 'USD'
};

const formData = ref<CaseCreate | CaseUpdate>({ ...defaultFormData });

// Получение отфильтрованных кейсов
const filteredCases = computed(() => {
  let result = [...cases.value];
  
  if (statusFilter.value) {
    result = result.filter(c => c.status === statusFilter.value);
  }
  
  if (fundFilter.value) {
    result = result.filter(c => c.created_by_fund_id === fundFilter.value);
  }
  
  return result.sort((a, b) => {
    // Сортировка по дате создания (сначала новые)
    return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
  });
});

// Получение данных
async function fetchCases() {
  loading.value = true;
  try {
    cases.value = await casesApi.getCases();
  } catch (error) {
    console.error('Ошибка при получении кейсов:', error);
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

async function fetchPlayers() {
  try {
    players.value = await playersApi.getPlayers();
  } catch (error) {
    console.error('Ошибка при получении игроков:', error);
  }
}

// Получение данных о связанных объектах
function getFundName(fundId: string): string {
  if (!fundId) return 'Не привязан';
  
  // Если есть расширенные данные о фонде, используем их
  const caseItem = cases.value.find(c => c.created_by_fund_id === fundId);
  if (caseItem && caseItem.fund) {
    return caseItem.fund.name || 'Не указан';
  }
  
  // Иначе ищем в списке фондов
  const fund = funds.value.find(f => f.id === fundId);
  return fund ? (fund.name || 'Не указан') : 'Не привязан';
}

function getPlayerName(playerId?: string): string {
  if (!playerId) return 'Не назначен';
  
  // Если есть расширенные данные об игроке, используем их
  const caseItem = cases.value.find(c => c.player_id === playerId);
  if (caseItem && caseItem.player) {
    const player = caseItem.player;
    if (player.full_name) return player.full_name;
    
    const firstName = player.first_name || '';
    const lastName = player.last_name || '';
    
    if (firstName || lastName) {
      return `${firstName} ${lastName}`.trim();
    }
    
    return 'Игрок #' + playerId.substring(0, 8);
  }
  
  // Иначе ищем в списке игроков
  const player = players.value.find(p => p.id === playerId);
  if (player) {
    if (player.full_name) return player.full_name;
    
    const firstName = player.first_name || '';
    const lastName = player.last_name || '';
    
    if (firstName || lastName) {
      return `${firstName} ${lastName}`.trim();
    }
  }
  
  return 'Игрок #' + playerId.substring(0, 8);
}

function getStatusText(status: string): string {
  const statusMap: Record<string, string> = {
    'open': 'Открыт',
    'in_progress': 'В работе',
    'closed': 'Закрыт'
  };
  return statusMap[status] || status;
}

// Обработчики для CRUD
function editCase(case_item: CaseExtended) {
  currentCaseId.value = case_item.id;
  formData.value = {
    title: case_item.title || '',
    description: case_item.description || '',
    status: case_item.status as CaseStatus || 'open',
    player_id: case_item.player_id || '',
    arbitrage_type: case_item.arbitrage_type || '',
    arbitrage_amount: case_item.arbitrage_amount ?? 0,
    arbitrage_currency: case_item.arbitrage_currency || 'USD'
  };
  showEditModal.value = true;
}

function confirmDeleteCase(case_item: CaseExtended) {
  caseToDelete.value = case_item;
  showDeleteConfirm.value = true;
}

async function deleteCaseConfirmed() {
  if (!caseToDelete.value) return;
  
  isSubmitting.value = true;
  try {
    await casesApi.deleteCase(caseToDelete.value.id);
    
    // Удаляем из локального состояния
    cases.value = cases.value.filter(c => c.id !== caseToDelete.value?.id);
    showDeleteConfirm.value = false;
  } catch (error: any) {
    alert(`Ошибка: ${error.response?.data?.detail || 'Что-то пошло не так'}`);
  } finally {
    isSubmitting.value = false;
  }
}

async function saveCase() {
  isSubmitting.value = true;
  try {
    if (showEditModal.value && currentCaseId.value) {
      // Обновление кейса
      const updatedCase = await casesApi.updateCase(currentCaseId.value, formData.value as CaseUpdate);
      
      // Обновляем кейс в локальном состоянии
      const index = cases.value.findIndex(c => c.id === updatedCase.id);
      if (index !== -1) {
        cases.value[index] = updatedCase;
      }
    } else {
      // Создание кейса
      // Для создания кейса нужно добавить created_by_fund_id из текущего пользователя
      const createData = {
        ...formData.value as CaseCreate,
        // Здесь мы используем ID фонда текущего пользователя
      };
      const newCase = await casesApi.createCase(createData);
      cases.value.push(newCase);
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
  currentCaseId.value = null;
  formData.value = { ...defaultFormData };
}

// Загрузка данных при монтировании
onMounted(async () => {
  await Promise.all([
    fetchCases(),
    fetchFunds(),
    fetchPlayers()
  ]);
});
</script> 