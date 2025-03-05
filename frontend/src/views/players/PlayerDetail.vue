<template>
  <div class="player-detail">
    <div v-if="loading" class="text-center py-16">
      <div class="animate-spin h-12 w-12 border-4 border-blue-500 rounded-full border-t-transparent mx-auto"></div>
      <p class="mt-4 text-gray-600">Загрузка информации об игроке...</p>
    </div>
    
    <div v-else-if="error" class="p-6 bg-red-50 text-red-700 rounded-lg my-4">
      <h3 class="text-lg font-medium mb-2">Ошибка загрузки</h3>
      <p>{{ error }}</p>
      <button 
        @click="fetchPlayer" 
        class="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
      >
        Попробовать снова
      </button>
    </div>
    
    <div v-else-if="player">
      <!-- Верхняя панель с основной информацией и кнопками действий -->
      <div class="bg-white p-6 rounded-lg shadow-sm mb-6">
        <div class="flex justify-between items-start">
          <div class="flex items-center">
            <div class="w-16 h-16 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center text-xl font-medium mr-4">
              {{ getPlayerInitials() }}
            </div>
            <div>
              <h1 class="text-2xl font-medium">{{ getPlayerFullName() }}</h1>
              <p class="text-gray-600">{{ player.nickname }}</p>
            </div>
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
              @click="updatePlayer" 
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
            Информация
          </button>
          <button 
            @click="activeTab = 'methods'" 
            class="py-3 px-1 font-medium border-b-2 -mb-px" 
            :class="activeTab === 'methods' ? 'text-blue-600 border-blue-600' : 'text-gray-500 border-transparent hover:text-gray-700'"
          >
            Методы оплаты
          </button>
          <button 
            @click="activeTab = 'social'" 
            class="py-3 px-1 font-medium border-b-2 -mb-px" 
            :class="activeTab === 'social' ? 'text-blue-600 border-blue-600' : 'text-gray-500 border-transparent hover:text-gray-700'"
          >
            Социальные сети
          </button>
          <button 
            @click="activeTab = 'cases'" 
            class="py-3 px-1 font-medium border-b-2 -mb-px" 
            :class="activeTab === 'cases' ? 'text-blue-600 border-blue-600' : 'text-gray-500 border-transparent hover:text-gray-700'"
          >
            Дела
          </button>
        </nav>
      </div>
      
      <!-- Содержимое вкладок -->
      <div class="tab-content">
        <!-- Вкладка с информацией об игроке -->
        <div v-show="activeTab === 'details'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Основная информация -->
          <div class="lg:col-span-2 space-y-6">
            <div class="bg-white p-6 rounded-lg shadow-sm">
              <h2 class="text-lg font-medium mb-4">Основная информация</h2>
              
              <div class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Имя</label>
                    <input 
                      v-if="editMode" 
                      v-model="editForm.first_name" 
                      type="text" 
                      class="w-full p-2 border rounded"
                    />
                    <p v-else class="p-2 bg-gray-50 rounded">
                      {{ player.first_name || '-' }}
                    </p>
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Фамилия</label>
                    <input 
                      v-if="editMode" 
                      v-model="editForm.last_name" 
                      type="text" 
                      class="w-full p-2 border rounded"
                    />
                    <p v-else class="p-2 bg-gray-50 rounded">
                      {{ player.last_name || '-' }}
                    </p>
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Отчество</label>
                    <input 
                      v-if="editMode" 
                      v-model="editForm.middle_name" 
                      type="text" 
                      class="w-full p-2 border rounded"
                    />
                    <p v-else class="p-2 bg-gray-50 rounded">
                      {{ player.middle_name || '-' }}
                    </p>
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Никнейм</label>
                  <input 
                    v-if="editMode" 
                    v-model="editForm.nickname" 
                    type="text" 
                    class="w-full p-2 border rounded"
                  />
                  <p v-else class="p-2 bg-gray-50 rounded">
                    {{ player.nickname }}
                  </p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input 
                    v-if="editMode" 
                    v-model="editForm.email" 
                    type="email" 
                    class="w-full p-2 border rounded"
                  />
                  <p v-else class="p-2 bg-gray-50 rounded">
                    {{ player.email || '-' }}
                  </p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Примечания</label>
                  <textarea 
                    v-if="editMode" 
                    v-model="editForm.notes" 
                    rows="4" 
                    class="w-full p-2 border rounded"
                  ></textarea>
                  <p v-else class="p-2 bg-gray-50 rounded whitespace-pre-line">
                    {{ player.notes || 'Нет примечаний' }}
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Боковая панель с дополнительной информацией -->
          <div class="space-y-6">
            <div class="bg-white p-6 rounded-lg shadow-sm">
              <h2 class="text-lg font-medium mb-4">Дополнительно</h2>
              
              <div class="space-y-4">
                <div>
                  <p class="text-sm text-gray-500">Дата создания</p>
                  <p>{{ formatDate(player.created_at) }}</p>
                </div>
                
                <div>
                  <p class="text-sm text-gray-500">Последнее обновление</p>
                  <p>{{ formatDate(player.updated_at) }}</p>
                </div>
                
                <div>
                  <p class="text-sm text-gray-500">ID игрока</p>
                  <p>{{ player.id }}</p>
                </div>
              </div>
            </div>
            
            <div class="bg-white p-6 rounded-lg shadow-sm">
              <h2 class="text-lg font-medium mb-4">Статистика дел</h2>
              
              <div v-if="caseStats" class="divide-y">
                <div class="py-2 flex justify-between">
                  <span>Всего дел:</span>
                  <span class="font-medium">{{ caseStats.total || 0 }}</span>
                </div>
                <div class="py-2 flex justify-between">
                  <span>Открытых:</span>
                  <span class="font-medium">{{ caseStats.open || 0 }}</span>
                </div>
                <div class="py-2 flex justify-between">
                  <span>Закрытых:</span>
                  <span class="font-medium">{{ caseStats.closed || 0 }}</span>
                </div>
              </div>
              <div v-else class="text-gray-500 text-center">
                Нет данных о делах
              </div>
            </div>
          </div>
        </div>
        
        <!-- Вкладка с методами оплаты -->
        <div v-show="activeTab === 'methods'" class="bg-white p-6 rounded-lg shadow-sm">
          <PlayerPaymentMethodsComponent 
            v-model="paymentMethods"
            :player-id="player.id"
            :editable="canEdit"
            @add="handleAddPaymentMethod"
            @delete="handleDeletePaymentMethod"
          />
        </div>
        
        <!-- Вкладка с социальными сетями -->
        <div v-show="activeTab === 'social'" class="bg-white p-6 rounded-lg shadow-sm">
          <PlayerSocialMediaComponent 
            v-model="socialMedia"
            :player-id="player.id"
            :editable="canEdit"
            @add="handleAddSocialMedia"
            @delete="handleDeleteSocialMedia"
          />
        </div>
        
        <!-- Вкладка с делами -->
        <div v-show="activeTab === 'cases'" class="bg-white p-6 rounded-lg shadow-sm">
          <h2 class="text-lg font-medium mb-4">Дела игрока</h2>
          
          <div v-if="loadingCases" class="text-center py-8">
            <div class="animate-spin h-8 w-8 border-4 border-blue-500 rounded-full border-t-transparent mx-auto"></div>
            <p class="mt-2 text-gray-600">Загрузка дел...</p>
          </div>
          
          <div v-else-if="cases.length" class="space-y-4">
            <div 
              v-for="case_item in cases" 
              :key="case_item.id" 
              class="border rounded-lg p-4 hover:bg-gray-50"
            >
              <div class="flex justify-between items-start">
                <div>
                  <div class="flex items-center">
                    <span 
                      class="px-2 py-1 rounded-full text-xs font-medium mr-2"
                      :class="getStatusClass(case_item.status)"
                    >
                      {{ getStatusName(case_item.status) }}
                    </span>
                    <h3 class="font-medium">
                      {{ case_item.title }}
                    </h3>
                  </div>
                  <p class="text-sm text-gray-600 mt-1">
                    Дело #{{ case_item.case_number }} - {{ formatDate(case_item.created_at) }}
                  </p>
                </div>
                <RouterLink 
                  :to="`/cases/${case_item.id}`" 
                  class="text-blue-600 hover:text-blue-800"
                >
                  Подробнее
                </RouterLink>
              </div>
              <div class="mt-2">
                <p class="text-gray-700">
                  {{ case_item.description }}
                </p>
              </div>
            </div>
          </div>
          
          <div v-else class="text-center py-8 text-gray-500">
            У игрока нет дел
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="bg-white p-6 rounded-lg shadow-sm text-center my-8">
      <h2 class="text-xl font-medium text-gray-600">Игрок не найден</h2>
      <p class="mt-2 text-gray-500">Запрошенный игрок не существует или был удален</p>
      <RouterLink 
        to="/players" 
        class="mt-4 inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Вернуться к списку игроков
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';
import type { Player, PlayerPaymentMethod, PlayerSocialMedia, Case } from '@/types/models';
import { useAuthStore } from '@/stores/auth';
import PlayerPaymentMethodsComponent from '@/components/player/PlayerPaymentMethods.vue';
import PlayerSocialMediaComponent from '@/components/player/PlayerSocialMedia.vue';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const loading = ref(false);
const loadingCases = ref(false);
const error = ref<string | null>(null);
const player = ref<Player | null>(null);
const paymentMethods = ref<PlayerPaymentMethod[]>([]);
const socialMedia = ref<PlayerSocialMedia[]>([]);
const cases = ref<Case[]>([]);
const caseStats = ref<{total: number, open: number, closed: number} | null>(null);
const editMode = ref(false);
const activeTab = ref('details');

const editForm = ref({
  nickname: '',
  first_name: '',
  last_name: '',
  middle_name: '',
  email: '',
  notes: ''
});

const canEdit = computed(() => {
  // Здесь будет логика проверки разрешений пользователя
  return true;
});

onMounted(async () => {
  const playerId = route.params.id as string;
  if (playerId) {
    await fetchPlayer();
  }
});

watch(() => route.params.id, async (newId) => {
  if (newId) {
    await fetchPlayer();
  }
});

async function fetchPlayer() {
  const playerId = route.params.id as string;
  if (!playerId) return;
  
  loading.value = true;
  error.value = null;
  
  try {
    // Здесь нужно заменить на реальные API-вызовы
    // player.value = await api.getPlayer(playerId);
    
    // Временный мок-объект
    player.value = {
      id: playerId,
      nickname: 'PlayerOne',
      first_name: 'Иван',
      last_name: 'Иванов',
      middle_name: 'Иванович',
      email: 'player@example.com',
      notes: 'Примечания об игроке...',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
    
    // Инициализация формы редактирования
    editForm.value = { 
      nickname: player.value.nickname,
      first_name: player.value.first_name || '',
      last_name: player.value.last_name || '',
      middle_name: player.value.middle_name || '',
      email: player.value.email || '',
      notes: player.value.notes || ''
    };
    
    // Загрузка связанных данных
    await Promise.all([
      fetchPaymentMethods(),
      fetchSocialMedia(),
      fetchPlayerCases()
    ]);
  } catch (err) {
    console.error('Error fetching player:', err);
    error.value = 'Не удалось загрузить информацию об игроке. Пожалуйста, попробуйте позже.';
  } finally {
    loading.value = false;
  }
}

async function fetchPaymentMethods() {
  if (!player.value) return;
  
  try {
    // paymentMethods.value = await api.getPlayerPaymentMethods(player.value.id);
    
    // Временные мок-данные
    paymentMethods.value = [
      {
        id: '1',
        player_id: player.value.id,
        type: 'bank',
        value: '4276 1234 5678 9012',
        description: 'Личная карта',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      {
        id: '2',
        player_id: player.value.id,
        type: 'crypto',
        value: '0x71C7656EC7ab88b098defB751B7401B5f6d8976F',
        description: 'ETH кошелек',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }
    ];
  } catch (err) {
    console.error('Error fetching payment methods:', err);
    paymentMethods.value = [];
  }
}

async function fetchSocialMedia() {
  if (!player.value) return;
  
  try {
    // socialMedia.value = await api.getPlayerSocialMedia(player.value.id);
    
    // Временные мок-данные
    socialMedia.value = [
      {
        id: '1',
        player_id: player.value.id,
        platform: 'telegram',
        username: '@playerone',
        description: 'Основной аккаунт',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      {
        id: '2',
        player_id: player.value.id,
        platform: 'vk',
        username: 'ivanivanov',
        description: '',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }
    ];
  } catch (err) {
    console.error('Error fetching social media:', err);
    socialMedia.value = [];
  }
}

async function fetchPlayerCases() {
  if (!player.value) return;
  
  loadingCases.value = true;
  
  try {
    // cases.value = await api.getPlayerCases(player.value.id);
    
    // Временные мок-данные
    cases.value = [
      {
        id: '1',
        case_number: '001',
        title: 'Первое дело',
        description: 'Описание первого дела',
        case_type: 'scam',
        status: 'open',
        amount: 1000,
        currency: 'USD',
        player_id: player.value.id,
        fund_id: '1',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      {
        id: '2',
        case_number: '002',
        title: 'Второе дело',
        description: 'Описание второго дела',
        case_type: 'debt',
        status: 'closed',
        amount: 500,
        currency: 'USD',
        player_id: player.value.id,
        fund_id: '1',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }
    ];
    
    // Рассчитываем статистику дел
    caseStats.value = {
      total: cases.value.length,
      open: cases.value.filter(c => c.status === 'open' || c.status === 'in_progress').length,
      closed: cases.value.filter(c => c.status === 'closed' || c.status === 'resolved').length
    };
  } catch (err) {
    console.error('Error fetching player cases:', err);
    cases.value = [];
    caseStats.value = null;
  } finally {
    loadingCases.value = false;
  }
}

async function updatePlayer() {
  if (!player.value) return;
  
  loading.value = true;
  error.value = null;
  
  try {
    // const updatedPlayer = await api.updatePlayer(player.value.id, editForm.value);
    // player.value = updatedPlayer;
    
    // Временный код обновления
    player.value = {
      ...player.value,
      ...editForm.value,
      updated_at: new Date().toISOString()
    };
    
    editMode.value = false;
  } catch (err) {
    console.error('Error updating player:', err);
    error.value = 'Не удалось обновить игрока. Пожалуйста, попробуйте позже.';
  } finally {
    loading.value = false;
  }
}

async function handleAddPaymentMethod(method: Partial<PlayerPaymentMethod>) {
  if (!player.value) return;
  
  try {
    // const newMethod = await api.createPlayerPaymentMethod(method);
    
    // Временный код
    const newMethod: PlayerPaymentMethod = {
      id: Math.random().toString(36).substring(2, 9),
      player_id: player.value.id,
      type: method.type || 'bank',
      value: method.value || '',
      description: method.description || '',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
    
    paymentMethods.value.push(newMethod);
  } catch (err) {
    console.error('Error adding payment method:', err);
  }
}

async function handleDeletePaymentMethod(methodId: string) {
  try {
    // await api.deletePlayerPaymentMethod(methodId);
    paymentMethods.value = paymentMethods.value.filter(m => m.id !== methodId);
  } catch (err) {
    console.error('Error deleting payment method:', err);
  }
}

async function handleAddSocialMedia(media: Partial<PlayerSocialMedia>) {
  if (!player.value) return;
  
  try {
    // const newMedia = await api.createPlayerSocialMedia(media);
    
    // Временный код
    const newMedia: PlayerSocialMedia = {
      id: Math.random().toString(36).substring(2, 9),
      player_id: player.value.id,
      platform: media.platform || 'other',
      username: media.username || '',
      description: media.description || '',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
    
    socialMedia.value.push(newMedia);
  } catch (err) {
    console.error('Error adding social media:', err);
  }
}

async function handleDeleteSocialMedia(mediaId: string) {
  try {
    // await api.deletePlayerSocialMedia(mediaId);
    socialMedia.value = socialMedia.value.filter(m => m.id !== mediaId);
  } catch (err) {
    console.error('Error deleting social media:', err);
  }
}

function getPlayerInitials(): string {
  if (!player.value) return '';
  
  if (player.value.first_name && player.value.last_name) {
    return `${player.value.first_name[0]}${player.value.last_name[0]}`.toUpperCase();
  }
  
  return player.value.nickname.substring(0, 2).toUpperCase();
}

function getPlayerFullName(): string {
  if (!player.value) return '';
  
  if (player.value.first_name && player.value.last_name) {
    return `${player.value.first_name} ${player.value.last_name}`;
  }
  
  return player.value.nickname;
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

function formatDate(dateString: string): string {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  return date.toLocaleString('ru-RU', { 
    day: '2-digit', 
    month: '2-digit', 
    year: 'numeric' 
  });
}
</script> 