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
              <p class="text-gray-600">{{ player.nicknames && player.nicknames.length > 0 ? player.nicknames[0].nickname : '' }}</p>
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
      
      <!-- Содержимое всей страницы в линейном виде -->
      <div class="space-y-6">
        <!-- Секция с основной информацией -->
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
                {{ player.nicknames && player.nicknames.length > 0 ? player.nicknames[0].nickname : '-' }}
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
                {{ player.contacts && player.contacts.find(c => c.type === 'email')?.value || '-' }}
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
                {{ player.health_notes || 'Нет примечаний' }}
              </p>
            </div>
          </div>
        </div>
        
        <!-- Секция с контактами и адресом -->
        <div class="bg-white p-6 rounded-lg shadow-sm">
          <h2 class="text-lg font-medium mb-4">Контактная информация</h2>
          
          <div class="mb-4">
            <h3 class="font-semibold mb-2">Адрес</h3>
            <div class="grid grid-cols-1 gap-4">
              <p>
                {{ player.locations && player.locations.length > 0 
                   ? formatAddress(player.locations[0])
                   : 'Адрес не указан' }}
              </p>
            </div>
          </div>

          <div class="mb-4">
            <h3 class="font-semibold mb-2">Контакты</h3>
            <div v-if="player.contacts && player.contacts.length > 0">
              <div v-for="(contact, index) in player.contacts" :key="index" class="mb-2">
                <strong>{{ formatContactType(contact.type) }}:</strong> {{ contact.value }}
                <span v-if="contact.description" class="text-sm text-gray-500 ml-2">({{ contact.description }})</span>
              </div>
            </div>
            <div v-else class="text-gray-500">
              Контакты не указаны
            </div>
          </div>
        </div>
        
        <!-- Секция с методами оплаты -->
        <div class="bg-white p-6 rounded-lg shadow-sm">
          <h2 class="text-lg font-medium mb-4">Методы оплаты</h2>
          <div v-if="player.payment_methods && player.payment_methods.length > 0">
            <div v-for="(method, index) in player.payment_methods" :key="index" class="mb-4 p-3 border rounded">
              <h3 class="font-semibold">{{ method.type || 'Метод оплаты' }}</h3>
              <p><strong>Значение:</strong> {{ method.value || 'Нет данных' }}</p>
              <p v-if="method.description"><strong>Описание:</strong> {{ method.description }}</p>
              <p><strong>Добавлен:</strong> {{ formatDate(method.created_at) }}</p>
            </div>
          </div>
          <div v-else class="text-center py-2 text-gray-500">
            Методы оплаты не найдены
          </div>
        </div>
        
        <!-- Секция с социальными сетями -->
        <div class="bg-white p-6 rounded-lg shadow-sm">
          <h2 class="text-lg font-medium mb-4">Социальные сети</h2>
          <div v-if="player.social_media && player.social_media.length > 0">
            <div v-for="(social, index) in player.social_media" :key="index" class="mb-4 p-3 border rounded">
              <h3 class="font-semibold">{{ social.platform || 'Соцсеть' }}</h3>
              <p v-if="social.url"><strong>Ссылка:</strong> <a :href="social.url" target="_blank" class="text-blue-500 hover:underline">{{ social.url }}</a></p>
              <p v-if="social.username"><strong>Имя пользователя:</strong> {{ social.username }}</p>
              <p v-if="social.description"><strong>Описание:</strong> {{ social.description }}</p>
              <p><strong>Добавлена:</strong> {{ formatDate(social.created_at) }}</p>
            </div>
          </div>
          <div v-else class="text-center py-2 text-gray-500">
            Социальные сети не найдены
          </div>
        </div>
        
        <!-- Секция с дополнительной информацией и статистикой -->
        <div class="bg-white p-6 rounded-lg shadow-sm">
          <h2 class="text-lg font-medium mb-4">Дополнительная информация</h2>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
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
          
          <div class="mt-6">
            <h3 class="font-semibold mb-2">Статистика дел</h3>
            <div v-if="caseStats" class="grid grid-cols-3 gap-4">
              <div class="p-3 bg-gray-50 rounded text-center">
                <p class="text-sm text-gray-500">Всего дел</p>
                <p class="text-lg font-medium">{{ caseStats.total || 0 }}</p>
              </div>
              <div class="p-3 bg-blue-50 rounded text-center">
                <p class="text-sm text-gray-500">Открытых</p>
                <p class="text-lg font-medium text-blue-600">{{ caseStats.open || 0 }}</p>
              </div>
              <div class="p-3 bg-green-50 rounded text-center">
                <p class="text-sm text-gray-500">Закрытых</p>
                <p class="text-lg font-medium text-green-600">{{ caseStats.closed || 0 }}</p>
              </div>
            </div>
            <div v-else class="text-gray-500 text-center py-2">
              Нет данных о делах
            </div>
          </div>
        </div>
        
        <!-- Секция с делами игрока -->
        <div class="bg-white p-6 rounded-lg shadow-sm">
          <h2 class="text-lg font-medium mb-4">Дела игрока</h2>
          
          <div v-if="loadingCases" class="text-center py-4">
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
          
          <div v-else class="text-center py-4 text-gray-500">
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
import type { Player, PlayerPaymentMethod, PlayerSocialMedia, CaseExtended } from '@/types/models';
import { useAuthStore } from '@/stores/auth';
import { useCasesApi } from '@/api/cases';
import { usePlayersApi } from '@/api/players';

// Импортируем компоненты вкладок
import InformationTab from '@/components/players/tabs/InformationTab.vue';
import PaymentMethodsTab from '@/components/players/tabs/PaymentMethodsTab.vue';
import SocialMediaTab from '@/components/players/tabs/SocialMediaTab.vue';
import CasesTab from '@/components/players/tabs/CasesTab.vue';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const casesApi = useCasesApi();
const playersApi = usePlayersApi();

const loading = ref(false);
const loadingCases = ref(false);
const error = ref<string | null>(null);
const player = ref<Player | null>(null);
const paymentMethods = ref<PlayerPaymentMethod[]>([]);
const socialMedia = ref<PlayerSocialMedia[]>([]);
const cases = ref<CaseExtended[]>([]);
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
    // Вызываем реальный API для получения данных игрока
    const response = await playersApi.getPlayerById(playerId);
    console.log('API Response (Player):', JSON.stringify(response, null, 2));
    
    // Проверяем, что ответ содержит необходимые данные
    if (!response || typeof response !== 'object') {
      console.error('API вернул некорректные данные:', response);
      error.value = 'Получены некорректные данные с сервера';
      loading.value = false;
      return;
    }
    
    player.value = response;
    
    // Инициализация формы редактирования
    initEditForm();
    
    // Загрузка связанных данных
    await Promise.all([
      fetchPaymentMethods(),
      fetchSocialMedia(),
      fetchPlayerCases()
    ]);
  } catch (err) {
    console.error('Ошибка при загрузке данных игрока:', err);
    error.value = 'Не удалось загрузить информацию об игроке. Пожалуйста, попробуйте позже.';
  } finally {
    loading.value = false;
  }
}

function initEditForm() {
  if (!player.value) return;
  
  const emailContact = player.value.contacts?.find(c => c.type === 'email');
  const primaryNickname = player.value.nicknames?.length > 0 ? player.value.nicknames[0] : null;
  
  editForm.value = {
    first_name: player.value.first_name || '',
    last_name: player.value.last_name || '',
    middle_name: player.value.middle_name || '',
    nickname: primaryNickname?.nickname || '',
    email: emailContact?.value || '',
    notes: player.value.health_notes || '',
    // Другие поля...
  };
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
        type: 'telegram',  // Добавлено обязательное поле type
        platform: 'telegram',
        value: '@playerone',  // Добавлено обязательное поле value
        username: '@playerone',
        description: 'Основной аккаунт',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      {
        id: '2',
        player_id: player.value.id,
        type: 'vk',  // Добавлено обязательное поле type
        platform: 'vk',
        value: 'ivanivanov',  // Добавлено обязательное поле value
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
    cases.value = await casesApi.getCasesByPlayer(player.value.id);
    
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

async function handleAddSocialMedia(media: any) {
  if (!player.value) return;
  
  try {
    // const newMedia = await api.createPlayerSocialMedia(media);
    
    // Временный код
    const newMedia: PlayerSocialMedia = {
      id: Math.random().toString(36).substring(2, 9),
      player_id: player.value.id,
      type: media.platform || 'other',  // Добавляем обязательное поле type
      platform: media.platform || 'other',
      value: media.username || '',  // Добавляем обязательное поле value
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
    return `${player.value.first_name[0]}${player.value.last_name ? player.value.last_name[0] : ''}`.toUpperCase();
  }
  
  if (player.value.nicknames && player.value.nicknames.length > 0) {
    return player.value.nicknames[0].nickname.substring(0, 2).toUpperCase();
  }
  
  return 'ИИ';
}

function getPlayerFullName(): string {
  if (!player.value) return '';
  
  if (player.value.first_name && player.value.last_name) {
    return `${player.value.first_name} ${player.value.last_name || ''}`;
  }
  
  if (player.value.full_name) {
    return player.value.full_name;
  }
  
  if (player.value.nicknames && player.value.nicknames.length > 0) {
    return player.value.nicknames[0].nickname;
  }
  
  return 'Неизвестный игрок';
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
  if (!dateString) return 'Нет данных';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date);
}

// Добавим функцию для форматирования адреса
function formatAddress(location: any): string {
  if (!location) return '';
  
  const parts: string[] = [];
  if (location.country) parts.push(location.country);
  if (location.city) parts.push(location.city);
  if (location.address) parts.push(location.address);
  
  return parts.join(', ') || 'Адрес не указан';
}

// Добавим функцию для форматирования типа контакта
function formatContactType(type: string): string {
  const types: Record<string, string> = {
    'email': 'Email',
    'phone': 'Телефон',
    'skype': 'Skype',
    'telegram': 'Telegram',
    'whatsapp': 'WhatsApp',
    'viber': 'Viber',
    'discord': 'Discord'
  };
  
  return types[type] || type;
}
</script> 