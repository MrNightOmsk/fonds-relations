<template>
  <div class="case-detail">
    <div v-if="loading" class="text-center py-16">
      <div class="animate-spin h-12 w-12 border-4 border-blue-500 rounded-full border-t-transparent mx-auto"></div>
      <p class="mt-4 text-gray-600">Загрузка дела...</p>
    </div>
    
    <div v-else-if="error" class="p-6 bg-red-50 text-red-700 rounded-lg my-4">
      <h3 class="text-lg font-medium mb-2">Ошибка загрузки</h3>
      <p>{{ error }}</p>
      <button 
        @click="fetchCase" 
        class="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
      >
        Попробовать снова
      </button>
    </div>
    
    <div v-else-if="currentCase">
      <!-- Верхняя панель с основной информацией и кнопками действий -->
      <div class="bg-white p-6 rounded-lg shadow-sm mb-6">
        <div class="flex justify-between items-start">
          <div>
            <h1 class="text-2xl font-medium">
              Дело #{{ currentCase.case_number }}
              <span 
                class="ml-2 px-3 py-1 text-sm rounded-full" 
                :class="getStatusClass(currentCase.status)"
              >
                {{ getStatusName(currentCase.status) }}
              </span>
            </h1>
            <p class="text-gray-600 mt-1">
              Создано {{ formatDate(currentCase.created_at) }}
            </p>
          </div>
          <div class="flex space-x-3">
            <button 
              v-if="canEdit" 
              @click="editMode = !editMode" 
              class="px-4 py-2 border rounded-lg text-gray-700 hover:bg-gray-50"
            >
              {{ editMode ? 'Отменить' : 'Редактировать' }}
            </button>
            <button 
              v-if="editMode" 
              @click="updateCase" 
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
      
      <!-- Вкладки навигации -->
      <div class="border-b mb-6">
        <nav class="flex space-x-6">
          <button 
            @click="activeTab = 'details'" 
            class="py-3 px-1 font-medium border-b-2 -mb-px" 
            :class="activeTab === 'details' ? 'text-blue-600 border-blue-600' : 'text-gray-500 border-transparent hover:text-gray-700'"
          >
            Детали дела
          </button>
          <button 
            @click="activeTab = 'comments'" 
            class="py-3 px-1 font-medium border-b-2 -mb-px" 
            :class="activeTab === 'comments' ? 'text-blue-600 border-blue-600' : 'text-gray-500 border-transparent hover:text-gray-700'"
          >
            Комментарии
          </button>
          <button 
            @click="activeTab = 'evidences'" 
            class="py-3 px-1 font-medium border-b-2 -mb-px" 
            :class="activeTab === 'evidences' ? 'text-blue-600 border-blue-600' : 'text-gray-500 border-transparent hover:text-gray-700'"
          >
            Доказательства
          </button>
        </nav>
      </div>
      
      <!-- Содержимое вкладок -->
      <div class="tab-content">
        <!-- Вкладка с деталями дела -->
        <div v-show="activeTab === 'details'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Основная информация -->
          <div class="lg:col-span-2 space-y-6">
            <div class="bg-white p-6 rounded-lg shadow-sm">
              <h2 class="text-lg font-medium mb-4">Основная информация</h2>
              
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Название дела</label>
                  <input 
                    v-if="editMode" 
                    v-model="editForm.title" 
                    type="text" 
                    class="w-full p-2 border rounded"
                  />
                  <p v-else class="p-2 bg-gray-50 rounded">
                    {{ currentCase.title }}
                  </p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Описание</label>
                  <textarea 
                    v-if="editMode" 
                    v-model="editForm.description" 
                    rows="4" 
                    class="w-full p-2 border rounded"
                  ></textarea>
                  <p v-else class="p-2 bg-gray-50 rounded whitespace-pre-line">
                    {{ currentCase.description || 'Описание отсутствует' }}
                  </p>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Тип дела</label>
                    <select 
                      v-if="editMode" 
                      v-model="editForm.case_type" 
                      class="w-full p-2 border rounded"
                    >
                      <option value="scam">Скам</option>
                      <option value="debt">Долг</option>
                      <option value="multi_accounting">Мультиаккаунтинг</option>
                      <option value="other">Другое</option>
                    </select>
                    <p v-else class="p-2 bg-gray-50 rounded">
                      {{ getCaseTypeName(currentCase.case_type) }}
                    </p>
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Статус</label>
                    <select 
                      v-if="editMode" 
                      v-model="editForm.status" 
                      class="w-full p-2 border rounded"
                    >
                      <option value="open">Открыто</option>
                      <option value="in_progress">В работе</option>
                      <option value="resolved">Разрешено</option>
                      <option value="closed">Закрыто</option>
                    </select>
                    <p v-else class="p-2 bg-gray-50 rounded">
                      {{ getStatusName(currentCase.status) }}
                    </p>
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Сумма</label>
                  <div v-if="editMode" class="grid grid-cols-2 gap-2">
                    <input 
                      v-model.number="editForm.amount" 
                      type="number"
                      min="0" 
                      class="w-full p-2 border rounded"
                    />
                    <select 
                      v-model="editForm.currency" 
                      class="w-full p-2 border rounded"
                    >
                      <option value="USD">USD</option>
                      <option value="EUR">EUR</option>
                      <option value="RUB">RUB</option>
                    </select>
                  </div>
                  <p v-else class="p-2 bg-gray-50 rounded">
                    {{ formatAmount(currentCase.amount, currentCase.currency) }}
                  </p>
                </div>
                
                <!-- Информация об арбитраже -->
                <div v-if="currentCase.arbitrage_type || editMode">
                  <h3 class="text-md font-medium mb-2">Информация об арбитраже</h3>
                  <div class="space-y-4 p-4 bg-gray-50 rounded-lg">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">Тип арбитража</label>
                      <select 
                        v-if="editMode" 
                        v-model="editForm.arbitrage_type" 
                        class="w-full p-2 border rounded"
                      >
                        <option value="">Нет арбитража</option>
                        <option value="pending">В ожидании</option>
                        <option value="in_progress">В процессе</option>
                        <option value="completed">Завершен</option>
                      </select>
                      <p v-else class="p-2 bg-white rounded">
                        {{ getArbitrageTypeName(currentCase.arbitrage_type) || 'Нет арбитража' }}
                      </p>
                    </div>
                    
                    <div v-if="editForm.arbitrage_type || currentCase.arbitrage_type">
                      <label class="block text-sm font-medium text-gray-700 mb-1">Сумма арбитража</label>
                      <div v-if="editMode" class="grid grid-cols-2 gap-2">
                        <input 
                          v-model.number="editForm.arbitrage_amount" 
                          type="number"
                          min="0" 
                          class="w-full p-2 border rounded"
                        />
                        <select 
                          v-model="editForm.arbitrage_currency" 
                          class="w-full p-2 border rounded"
                        >
                          <option value="USD">USD</option>
                          <option value="EUR">EUR</option>
                          <option value="RUB">RUB</option>
                        </select>
                      </div>
                      <p v-else class="p-2 bg-white rounded">
                        {{ formatAmount(currentCase.arbitrage_amount, currentCase.arbitrage_currency) }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Боковая панель с информацией о фонде и игроке -->
          <div class="space-y-6">
            <div class="bg-white p-6 rounded-lg shadow-sm">
              <h2 class="text-lg font-medium mb-4">Игрок</h2>
              
              <div v-if="player" class="space-y-3">
                <div class="flex items-center">
                  <div class="w-10 h-10 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center font-medium mr-3">
                    {{ getPlayerInitials(player) }}
                  </div>
                  <div>
                    <div class="font-medium">{{ getPlayerFullName(player) }}</div>
                    <div class="text-sm text-gray-500">ID: {{ player.id }}</div>
                  </div>
                </div>
                <div class="pt-2">
                  <RouterLink 
                    :to="`/players/${player.id}`" 
                    class="text-blue-600 hover:text-blue-800"
                  >
                    Подробнее об игроке
                  </RouterLink>
                </div>
              </div>
              <div v-else class="text-gray-500">
                Информация об игроке недоступна
              </div>
            </div>
            
            <div class="bg-white p-6 rounded-lg shadow-sm">
              <h2 class="text-lg font-medium mb-4">Фонд</h2>
              
              <div v-if="fund" class="space-y-3">
                <div class="font-medium">{{ fund.name }}</div>
                <div class="text-sm text-gray-600">{{ fund.description }}</div>
                <div class="pt-2">
                  <RouterLink 
                    :to="`/funds/${fund.id}`" 
                    class="text-blue-600 hover:text-blue-800"
                  >
                    Подробнее о фонде
                  </RouterLink>
                </div>
              </div>
              <div v-else class="text-gray-500">
                Информация о фонде недоступна
              </div>
            </div>
          </div>
        </div>
        
        <!-- Вкладка с комментариями -->
        <div v-show="activeTab === 'comments'" class="bg-white p-6 rounded-lg shadow-sm">
          <CaseComments 
            :case-id="currentCase.id" 
            @comment-added="handleCommentAdded"
          />
        </div>
        
        <!-- Вкладка с доказательствами -->
        <div v-show="activeTab === 'evidences'" class="bg-white p-6 rounded-lg shadow-sm">
          <CaseEvidences 
            :case-id="currentCase.id" 
            :editable="canEdit"
            @evidence-added="handleEvidenceAdded"
            @evidence-deleted="handleEvidenceDeleted"
          />
        </div>
      </div>
    </div>
    
    <div v-else class="bg-white p-6 rounded-lg shadow-sm text-center my-8">
      <h2 class="text-xl font-medium text-gray-600">Дело не найдено</h2>
      <p class="mt-2 text-gray-500">Запрошенное дело не существует или было удалено</p>
      <RouterLink 
        to="/cases" 
        class="mt-4 inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Вернуться к списку дел
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';
import type { Case, Player, Fund, CaseComment, CaseEvidence } from '@/types/models';
import { useAuthStore } from '@/stores/auth';
import CaseComments from '@/components/case/CaseComments.vue';
import CaseEvidences from '@/components/case/CaseEvidences.vue';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const loading = ref(false);
const error = ref<string | null>(null);
const currentCase = ref<Case | null>(null);
const player = ref<Player | null>(null);
const fund = ref<Fund | null>(null);
const editMode = ref(false);
const activeTab = ref('details');

const editForm = ref({
  title: '',
  description: '',
  case_type: '',
  status: '',
  amount: 0,
  currency: 'USD',
  arbitrage_type: '',
  arbitrage_amount: 0,
  arbitrage_currency: 'USD'
});

const canEdit = computed(() => {
  // Здесь будет логика проверки разрешений пользователя
  return true;
});

onMounted(async () => {
  const caseId = route.params.id as string;
  if (caseId) {
    await fetchCase();
  }
});

watch(() => route.params.id, async (newId) => {
  if (newId) {
    await fetchCase();
  }
});

async function fetchCase() {
  const caseId = route.params.id as string;
  if (!caseId) return;
  
  loading.value = true;
  error.value = null;
  
  try {
    // Здесь нужно заменить на реальные API-вызовы
    // currentCase.value = await api.getCase(caseId);
    
    // Временный мок-объект
    currentCase.value = {
      id: caseId,
      case_number: '001',
      title: 'Пример дела',
      description: 'Описание примера дела...',
      case_type: 'scam',
      status: 'open',
      amount: 1000,
      currency: 'USD',
      player_id: '1',
      fund_id: '1',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      arbitrage_type: 'pending',
      arbitrage_amount: 500,
      arbitrage_currency: 'USD'
    };
    
    // Инициализация формы редактирования
    editForm.value = { 
      title: currentCase.value.title,
      description: currentCase.value.description || '',
      case_type: currentCase.value.case_type,
      status: currentCase.value.status,
      amount: currentCase.value.amount,
      currency: currentCase.value.currency,
      arbitrage_type: currentCase.value.arbitrage_type || '',
      arbitrage_amount: currentCase.value.arbitrage_amount || 0,
      arbitrage_currency: currentCase.value.arbitrage_currency || 'USD'
    };
    
    // Загрузка связанных данных
    await Promise.all([
      fetchPlayer(currentCase.value.player_id),
      fetchFund(currentCase.value.fund_id)
    ]);
  } catch (err) {
    console.error('Error fetching case:', err);
    error.value = 'Не удалось загрузить дело. Пожалуйста, попробуйте позже.';
  } finally {
    loading.value = false;
  }
}

async function fetchPlayer(playerId: string) {
  try {
    // player.value = await api.getPlayer(playerId);
    
    // Временный мок-объект
    player.value = {
      id: playerId,
      nickname: 'PlayerOne',
      first_name: 'Иван',
      last_name: 'Иванов',
      middle_name: 'Иванович',
      email: 'player@example.com',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
  } catch (err) {
    console.error('Error fetching player:', err);
    player.value = null;
  }
}

async function fetchFund(fundId: string) {
  try {
    // fund.value = await api.getFund(fundId);
    
    // Временный мок-объект
    fund.value = {
      id: fundId,
      name: 'Example Fund',
      description: 'Описание фонда...',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
  } catch (err) {
    console.error('Error fetching fund:', err);
    fund.value = null;
  }
}

async function updateCase() {
  if (!currentCase.value) return;
  
  loading.value = true;
  error.value = null;
  
  try {
    // const updatedCase = await api.updateCase(currentCase.value.id, editForm.value);
    // currentCase.value = updatedCase;
    
    // Временный код обновления
    currentCase.value = {
      ...currentCase.value,
      ...editForm.value,
      updated_at: new Date().toISOString()
    };
    
    editMode.value = false;
  } catch (err) {
    console.error('Error updating case:', err);
    error.value = 'Не удалось обновить дело. Пожалуйста, попробуйте позже.';
  } finally {
    loading.value = false;
  }
}

function handleCommentAdded(comment: CaseComment) {
  console.log('Комментарий добавлен:', comment);
  // Дополнительная логика, если нужно
}

function handleEvidenceAdded(evidence: CaseEvidence) {
  console.log('Доказательство добавлено:', evidence);
  // Дополнительная логика, если нужно
}

function handleEvidenceDeleted(evidenceId: string) {
  console.log('Доказательство удалено:', evidenceId);
  // Дополнительная логика, если нужно
}

function getCaseTypeName(type: string): string {
  const types: Record<string, string> = {
    'scam': 'Скам',
    'debt': 'Долг',
    'multi_accounting': 'Мультиаккаунтинг',
    'other': 'Другое'
  };
  return types[type] || type;
}

function getStatusName(status: string): string {
  const statuses: Record<string, string> = {
    'open': 'Открыто',
    'in_progress': 'В работе',
    'resolved': 'Разрешено',
    'closed': 'Закрыто'
  };
  return statuses[status] || status;
}

function getStatusClass(status: string): string {
  const classes: Record<string, string> = {
    'open': 'bg-yellow-100 text-yellow-800',
    'in_progress': 'bg-blue-100 text-blue-800',
    'resolved': 'bg-green-100 text-green-800',
    'closed': 'bg-gray-100 text-gray-800'
  };
  return classes[status] || 'bg-gray-100 text-gray-800';
}

function getArbitrageTypeName(type: string | undefined): string {
  if (!type) return '';
  
  const types: Record<string, string> = {
    'pending': 'В ожидании',
    'in_progress': 'В процессе',
    'completed': 'Завершен'
  };
  return types[type] || type;
}

function formatDate(dateString: string): string {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  return date.toLocaleString('ru-RU', { 
    day: '2-digit', 
    month: '2-digit', 
    year: 'numeric' 
  });
}

function formatAmount(amount: number, currency: string): string {
  if (amount === undefined || amount === null) return '-';
  
  return new Intl.NumberFormat('ru-RU', { 
    style: 'currency', 
    currency: currency || 'USD' 
  }).format(amount);
}

function getPlayerInitials(player: Player): string {
  if (!player) return '';
  
  if (player.first_name && player.last_name) {
    return `${player.first_name[0]}${player.last_name[0]}`.toUpperCase();
  }
  
  return player.nickname.substring(0, 2).toUpperCase();
}

function getPlayerFullName(player: Player): string {
  if (!player) return '';
  
  if (player.first_name && player.last_name) {
    return `${player.first_name} ${player.last_name}`;
  }
  
  return player.nickname;
}
</script> 