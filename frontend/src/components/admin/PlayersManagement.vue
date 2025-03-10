<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">Управление игроками</h2>
      <button @click="showCreateModal = true" class="btn-primary">
        Создать игрока
      </button>
    </div>

    <!-- Фильтры -->
    <div class="mb-4 bg-white rounded-lg shadow p-4">
      <div class="flex flex-wrap gap-4">
        <!-- Фильтр по фонду -->
        <div class="flex items-center">
          <label class="mr-2 text-sm font-medium text-gray-700">Фонд:</label>
          <select v-model="fundFilter" class="px-3 py-2 border border-gray-300 rounded-md text-sm">
            <option value="">Все</option>
            <option v-for="fund in funds" :key="fund.id" :value="fund.id">
              {{ fund.name }}
            </option>
          </select>
        </div>
        
        <!-- Поиск по имени -->
        <div class="flex-grow max-w-md">
          <label class="sr-only">Поиск</label>
          <div class="relative">
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Поиск по имени игрока..."
              class="w-full px-3 py-2 pl-10 border border-gray-300 rounded-md"
            >
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <span class="text-gray-500">🔍</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Новый интерфейс карточек игроков -->
    <div class="space-y-4">
      <!-- Сообщение о загрузке -->
      <div v-if="loading" class="bg-white rounded-lg shadow p-6 text-center">
        <p class="text-lg text-gray-600">Загрузка игроков...</p>
      </div>
      
      <!-- Сообщение об отсутствии игроков -->
      <div v-else-if="filteredPlayers.length === 0" class="bg-white rounded-lg shadow p-6 text-center">
        <p class="text-lg text-gray-600">Игроки не найдены</p>
      </div>
      
      <!-- Сетка карточек -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="player in filteredPlayers" :key="player.id" class="bg-white rounded-lg shadow hover:shadow-md transition-shadow">
          <!-- Заголовок карточки с именем и кнопками действий -->
          <div class="p-4 border-b border-gray-200 flex justify-between items-center">
            <h3 class="font-semibold text-lg truncate">{{ player.full_name }}</h3>
            <div class="flex space-x-2">
              <button @click="editPlayer(player)" class="text-blue-600 hover:text-blue-900">
                <span class="sr-only">Изменить</span>
                ✏️
              </button>
              <button @click="confirmDeletePlayer(player)" class="text-red-600 hover:text-red-900">
                <span class="sr-only">Удалить</span>
                🗑️
              </button>
            </div>
          </div>
          
          <!-- Основное содержимое карточки -->
          <div class="p-4 space-y-3">
            <!-- Никнеймы -->
            <div v-if="player.nicknames && player.nicknames.length > 0" class="flex flex-wrap gap-2">
              <span 
                v-for="nickname in player.nicknames.slice(0, 3)" 
                :key="nickname.id" 
                class="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded"
              >
                {{ nickname.nickname }}
              </span>
              <span 
                v-if="player.nicknames.length > 3" 
                class="inline-block bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded"
              >
                +{{ player.nicknames.length - 3 }}
              </span>
            </div>
            
            <!-- Информация о кейсах -->
            <div class="border-t border-gray-100 pt-2 mt-2">
              <div class="text-sm font-medium mb-1">Кейсы:</div>
              <div class="flex flex-wrap gap-2">
                <router-link 
                  :to="`/admin/cases?player_id=${player.id}&status=active`" 
                  class="px-2 py-1 bg-green-100 text-green-800 rounded text-xs flex items-center"
                >
                  <span class="mr-1">🟢</span>
                  Активные: {{ getPlayerCaseCount(player.id, 'active') }}
                </router-link>
                <router-link 
                  :to="`/admin/cases?player_id=${player.id}&status=completed`" 
                  class="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs flex items-center"
                >
                  <span class="mr-1">✅</span>
                  Завершенные: {{ getPlayerCaseCount(player.id, 'completed') }}
                </router-link>
                <router-link 
                  :to="`/admin/cases?player_id=${player.id}&status=paused`" 
                  class="px-2 py-1 bg-yellow-100 text-yellow-800 rounded text-xs flex items-center"
                >
                  <span class="mr-1">⏸️</span>
                  На паузе: {{ getPlayerCaseCount(player.id, 'paused') }}
                </router-link>
              </div>
              <div v-if="getPlayerTotalCaseCount(player.id) > 0" class="mt-1">
                <router-link 
                  :to="`/admin/cases?player_id=${player.id}`" 
                  class="text-xs text-blue-600 hover:text-blue-800"
                >
                  Все кейсы игрока →
                </router-link>
              </div>
              <div v-else class="text-xs text-gray-500 mt-1">
                Нет активных кейсов
              </div>
            </div>
            
            <!-- Контакты -->
            <div v-if="player.contacts && player.contacts.length > 0" class="space-y-1">
              <div v-for="contact in player.contacts.slice(0, 2)" :key="contact.id" class="flex items-center text-sm text-gray-600">
                <span class="mr-1 w-16 text-gray-500">{{ getContactIcon(contact.type) }} {{ contact.type }}:</span>
                <span class="truncate">{{ contact.value }}</span>
              </div>
              <div v-if="player.contacts.length > 2" class="text-xs text-gray-500">
                и еще {{ player.contacts.length - 2 }} контакта(ов)
              </div>
            </div>
            
            <!-- Местоположение -->
            <div v-if="player.locations && player.locations.length > 0 && (player.locations[0].country || player.locations[0].city)" class="text-sm text-gray-600">
              <span class="mr-1">📍</span>
              {{ [player.locations[0].country, player.locations[0].city].filter(Boolean).join(', ') }}
            </div>
            
            <!-- Дата рождения -->
            <div v-if="player.birth_date" class="text-sm text-gray-600">
              <span class="mr-1">🎂</span>
              {{ new Date(player.birth_date).toLocaleDateString() }}
            </div>
          </div>
          
          <!-- Футер карточки с датой создания и фондом -->
          <div class="p-3 bg-gray-50 text-xs text-gray-500 rounded-b-lg flex justify-between">
            <div>Фонд: {{ getFundName(player.created_by_fund_id) }}</div>
            <div>Создан: {{ new Date(player.created_at).toLocaleDateString() }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно создания/редактирования игрока -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 overflow-y-auto py-6">
      <div class="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 my-auto relative">
        <h3 class="text-lg font-semibold mb-4">
          {{ showEditModal ? 'Редактирование игрока' : 'Создание игрока' }}
        </h3>
        
        <!-- Контент с прокруткой, если он слишком большой -->
        <div class="max-h-[70vh] overflow-y-auto pr-2">
          <!-- Сообщение об ошибке -->
          <div v-if="errorMessage" class="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            <p>{{ errorMessage }}</p>
          </div>
          
          <!-- Форма -->
          <div class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Имя</label>
                <input 
                  type="text" 
                  v-model="formData.first_name" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md"
                  required
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Фамилия</label>
                <input 
                  type="text" 
                  v-model="formData.last_name" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md"
                  required
                >
              </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Отчество</label>
                <input 
                  type="text" 
                  v-model="formData.middle_name" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md"
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Дата рождения</label>
                <input 
                  type="date" 
                  v-model="formData.birth_date" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md"
                >
              </div>
            </div>
            
            <!-- Секция с никнеймами -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Никнеймы</label>
              <div v-for="(nickname, index) in formNicknames" :key="index" class="flex items-center mb-2">
                <input 
                  v-model="nickname.nickname" 
                  type="text" 
                  class="flex-grow px-3 py-2 border border-gray-300 rounded-md mr-2"
                  placeholder="Никнейм игрока"
                >
                <input 
                  v-model="nickname.room" 
                  type="text" 
                  class="flex-grow px-3 py-2 border border-gray-300 rounded-md mr-2"
                  placeholder="Покерный рум/площадка"
                >
                <button 
                  @click="removeNickname(index)" 
                  class="p-2 text-red-600 hover:text-red-900 flex-shrink-0"
                  type="button"
                >
                  <span>✕</span>
                </button>
              </div>
              <button 
                @click="addNickname" 
                class="text-blue-600 hover:text-blue-900 text-sm"
                type="button"
              >
                + Добавить никнейм
              </button>
            </div>
            
            <!-- Секция с адресом -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Адрес</label>
              <div class="space-y-2">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm text-gray-700 mb-1">Страна</label>
                    <input 
                      type="text" 
                      v-model="formLocation.country" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-md"
                      placeholder="Страна проживания"
                    >
                  </div>
                  <div>
                    <label class="block text-sm text-gray-700 mb-1">Город</label>
                    <input 
                      type="text" 
                      v-model="formLocation.city" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-md"
                      placeholder="Город проживания"
                    >
                  </div>
                </div>
                <div>
                  <label class="block text-sm text-gray-700 mb-1">Полный адрес</label>
                  <textarea 
                    v-model="formLocation.address" 
                    class="w-full px-3 py-2 border border-gray-300 rounded-md"
                    rows="2"
                    placeholder="Полный адрес проживания"
                  ></textarea>
                </div>
              </div>
            </div>
            
            <!-- Секция с контактной информацией -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Контактная информация</label>
              <div class="space-y-2">
                <div v-for="(contact, index) in formContacts" :key="index" class="flex items-center space-x-2">
                  <div class="w-1/3 relative contact-dropdown-container">
                    <input 
                      type="text" 
                      v-model="contact.searchText" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-md"
                      placeholder="Тип контакта..."
                      @input="filterContactTypes(contact)"
                      @focus="contact.showDropdown = true"
                    >
                    <div v-if="contact.showDropdown && contact.filteredTypes.length > 0" 
                      class="absolute left-0 right-0 top-full mt-1 max-h-40 overflow-y-auto z-50 border border-gray-300 rounded-md bg-white shadow-lg">
                      <div 
                        v-for="type in contact.filteredTypes" 
                        :key="type.value"
                        class="px-3 py-2 cursor-pointer hover:bg-gray-100"
                        @mousedown.prevent="selectContactType(contact, type)"
                      >
                        {{ type.label }}
                      </div>
                    </div>
                  </div>
                  <input 
                    type="text" 
                    v-model="contact.value" 
                    class="flex-grow px-3 py-2 border border-gray-300 rounded-md"
                    :placeholder="getContactPlaceholder(contact.type)"
                  >
                  <button 
                    @click="removeContact(index)" 
                    class="p-2 text-red-600 hover:text-red-900 flex-shrink-0"
                    type="button"
                  >
                    <span>✕</span>
                  </button>
                </div>
                <button 
                  @click="addContact" 
                  class="text-blue-600 hover:text-blue-900 text-sm"
                  type="button"
                >
                  + Добавить контакт
                </button>
              </div>
            </div>
            
            <!-- Секция с платежными системами -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Платежные системы</label>
              <div class="space-y-2">
                <div v-for="(payment, index) in formPaymentMethods" :key="index" class="flex items-center space-x-2">
                  <div class="w-1/3 relative payment-dropdown-container">
                    <input 
                      type="text" 
                      v-model="payment.searchText" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-md"
                      placeholder="Поиск платежной системы..."
                      @input="filterPaymentSystems(payment)"
                      @focus="payment.showDropdown = true"
                    >
                    <div v-if="payment.showDropdown && payment.filteredSystems.length > 0" 
                      class="absolute left-0 right-0 top-full mt-1 max-h-40 overflow-y-auto z-50 border border-gray-300 rounded-md bg-white shadow-lg">
                      <div 
                        v-for="system in payment.filteredSystems" 
                        :key="system.value"
                        class="px-3 py-2 cursor-pointer hover:bg-gray-100"
                        @mousedown.prevent="selectPaymentSystem(payment, system)"
                      >
                        {{ system.label }}
                      </div>
                    </div>
                  </div>
                  <input 
                    type="text" 
                    v-model="payment.value" 
                    class="flex-grow px-3 py-2 border border-gray-300 rounded-md"
                    :placeholder="getPaymentPlaceholder(payment.type)"
                  >
                  <button 
                    @click="removePaymentMethod(index)" 
                    class="p-2 text-red-600 hover:text-red-900 flex-shrink-0"
                    type="button"
                  >
                    <span>✕</span>
                  </button>
                </div>
                <button 
                  @click="addPaymentMethod" 
                  class="text-blue-600 hover:text-blue-900 text-sm"
                  type="button"
                >
                  + Добавить платежную систему
                </button>
              </div>
            </div>
          </div>
        </div>
        <!-- Кнопки действий внизу модального окна, всегда видимые -->
        <div class="mt-6 flex justify-end space-x-2 sticky bottom-0 bg-white pt-4 border-t">
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
import { ref, onMounted, computed, onBeforeUnmount, watch } from 'vue';
// @ts-ignore
import { usePlayersApi } from '@/api/players';
// @ts-ignore
import { useFundsApi } from '@/api/funds';
// @ts-ignore
import type { Player, CreatePlayerRequest, UpdatePlayerRequest, Fund, PlayerContact, PlayerLocation, PlayerPaymentMethod, PlayerPokerId } from '@/types/models';

// API клиенты
const playersApi = usePlayersApi();
const fundsApi = useFundsApi();

// Состояние
const players = ref<Player[]>([]);
const funds = ref<Fund[]>([]);
const pokerRooms = ref<any[]>([]); // Временный массив для покерных румов
const loading = ref(true);
const showCreateModal = ref(false);
const showEditModal = ref(false);
const showDeleteConfirm = ref(false);
const isSubmitting = ref(false);
const currentPlayerId = ref<string | null>(null);
const playerToDelete = ref<Player | null>(null);
const errorMessage = ref<string | null>(null);

// Фильтры
const fundFilter = ref('');
const searchQuery = ref('');

// Форма
const defaultFormData: CreatePlayerRequest = {
  first_name: '',
  last_name: '',
  middle_name: '',
  birth_date: '',
  contacts: [],
  locations: [],
  payment_methods: [],
  nicknames: []
};

const formData = ref<CreatePlayerRequest | UpdatePlayerRequest>({ ...defaultFormData });
const formContacts = ref<Partial<PlayerContact>[]>([]);
const formLocation = ref<Partial<PlayerLocation>>({
  country: '',
  city: '',
  address: ''
});
const formPaymentMethods = ref<Partial<PlayerPaymentMethod>[]>([]);
const formNicknames = ref<any[]>([]); // Временная структура для никнеймов

// Состояние для кейсов игроков
const playerCases = ref<Record<string, any>>({});

// Получение отфильтрованных игроков
const filteredPlayers = computed(() => {
  let result = [...players.value];
  
  // Фильтрация по фонду
  if (fundFilter.value) {
    result = result.filter(p => p.created_by_fund_id === fundFilter.value);
  }
  
  // Поиск по имени
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(p => {
      // Поиск по полному имени
      if (p.full_name && p.full_name.toLowerCase().includes(query)) {
        return true;
      }
      
      // Поиск по никнеймам
      if (p.nicknames && p.nicknames.some(n => n.nickname.toLowerCase().includes(query))) {
        return true;
      }
      
      // Поиск по электронной почте (если есть в контактах)
      if (p.contacts && p.contacts.some(c => 
        c.value && c.value.toLowerCase().includes(query)
      )) {
        return true;
      }
      
      return false;
    });
  }
  
  // Сортировка по дате создания (сначала новые)
  return result.sort((a, b) => {
    return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
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

async function fetchPokerRooms() {
  try {
    // Здесь будет API запрос на получение списка покерных румов
    // Временно заполняем тестовыми данными
    pokerRooms.value = [
      { id: 'pokerstars', name: 'PokerStars' },
      { id: 'ggpoker', name: 'GGPoker' },
      { id: 'partypoker', name: 'PartyPoker' },
      { id: '888poker', name: '888poker' },
      { id: 'winamax', name: 'Winamax' },
      { id: 'acr', name: 'Americas Cardroom' },
      { id: 'wpn', name: 'Winning Poker Network' },
      { id: 'ipoker', name: 'iPoker Network' },
      { id: 'chico', name: 'Chico Poker Network' },
      { id: 'ignition', name: 'Ignition Poker' }
    ];
  } catch (error) {
    console.error('Ошибка при получении покерных румов:', error);
  }
}

// Получение данных о связанных объектах
function getFundName(fundId: string): string {
  const fund = funds.value.find(f => f.id === fundId);
  return fund ? fund.name : 'Неизвестный фонд';
}

function getPokerRoomName(roomId: string): string {
  const room = pokerRooms.value.find(r => r.id === roomId);
  return room ? room.name : roomId;
}

// Список типов контактов
const contactTypes = ref([
  { value: 'email', label: 'Email' },
  { value: 'phone', label: 'Телефон' },
  { value: 'telegram', label: 'Telegram' },
  { value: 'whatsapp', label: 'WhatsApp' },
  { value: 'gipsyteam', label: 'GipsyTeam' },
  { value: 'vk', label: 'VK' },
  { value: 'facebook', label: 'Facebook' },
  { value: 'instagram', label: 'Instagram' },
  { value: 'twitter', label: 'Twitter' },
  { value: 'skype', label: 'Skype' },
  { value: 'discord', label: 'Discord' },
  { value: 'other', label: 'Другое' }
]);

// Обработчик клика вне выпадающих списков
const handleClickOutside = (event: MouseEvent) => {
  // Закрыть все выпадающие списки контактов
  formContacts.value.forEach(contact => {
    if (contact.showDropdown && !event.composedPath().some(el => {
      const elem = el as HTMLElement;
      return elem.classList?.contains('contact-dropdown-container');
    })) {
      contact.showDropdown = false;
    }
  });
  
  // Закрыть все выпадающие списки платежных систем
  formPaymentMethods.value.forEach(payment => {
    if (payment.showDropdown && !event.composedPath().some(el => {
      const elem = el as HTMLElement;
      return elem.classList?.contains('payment-dropdown-container');
    })) {
      payment.showDropdown = false;
    }
  });
};

// Установка слушателя клика при монтировании
onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

// Удаление слушателя клика при размонтировании
onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});

// Утилиты для работы с контактами
function addContact() {
  formContacts.value.push({
    type: '',
    value: '',
    searchText: '',
    showDropdown: false,
    filteredTypes: [...contactTypes.value]
  });
}

function removeContact(index: number) {
  formContacts.value.splice(index, 1);
}

function filterContactTypes(contact: any) {
  const searchText = contact.searchText.toLowerCase();
  contact.filteredTypes = contactTypes.value.filter(type => 
    type.label.toLowerCase().includes(searchText) || 
    type.value.toLowerCase().includes(searchText)
  );
  
  // Если есть точное совпадение или только один результат, автоматически устанавливаем значение
  const exactMatch = contact.filteredTypes.find(t => t.label.toLowerCase() === searchText);
  if (exactMatch) {
    selectContactType(contact, exactMatch);
  }
}

function selectContactType(contact: any, type: any) {
  contact.type = type.value;
  contact.searchText = type.label;
  contact.showDropdown = false;
}

function getContactPlaceholder(type: string): string {
  const placeholders: Record<string, string> = {
    'email': 'example@mail.com',
    'phone': '+7 (XXX) XXX-XX-XX',
    'telegram': '@username',
    'whatsapp': '+7XXXXXXXXXX',
    'gipsyteam': 'Ник или ссылка на профиль',
    'vk': 'username или ссылка',
    'facebook': 'username или ссылка',
    'instagram': '@username',
    'twitter': '@username',
    'skype': 'логин Skype',
    'discord': 'username#0000',
    'other': 'Значение'
  };
  return placeholders[type] || 'Значение';
}

// Список платежных систем
const paymentSystems = ref([
  { value: 'skrill', label: 'Skrill' },
  { value: 'neteller', label: 'Neteller' },
  { value: 'webmoney', label: 'WebMoney' },
  { value: 'qiwi', label: 'QIWI' },
  { value: 'yoomoney', label: 'ЮMoney' },
  { value: 'paypal', label: 'PayPal' },
  { value: 'ecopayz', label: 'ecoPayz' },
  { value: 'muchbetter', label: 'MuchBetter' },
  { value: 'cryptocurrencies', label: 'Криптовалюты' },
  { value: 'other', label: 'Другое' }
]);

// Утилиты для работы с платежными системами
function addPaymentMethod() {
  formPaymentMethods.value.push({
    type: '',
    value: '',
    searchText: '',
    showDropdown: false,
    filteredSystems: [...paymentSystems.value]
  });
}

function removePaymentMethod(index: number) {
  formPaymentMethods.value.splice(index, 1);
}

function filterPaymentSystems(payment: any) {
  const searchText = payment.searchText.toLowerCase();
  payment.filteredSystems = paymentSystems.value.filter(system => 
    system.label.toLowerCase().includes(searchText) || 
    system.value.toLowerCase().includes(searchText)
  );
  
  // Если есть точное совпадение или только один результат, автоматически устанавливаем значение
  const exactMatch = payment.filteredSystems.find(s => s.label.toLowerCase() === searchText);
  if (exactMatch) {
    selectPaymentSystem(payment, exactMatch);
  }
}

function selectPaymentSystem(payment: any, system: any) {
  payment.type = system.value;
  payment.searchText = system.label;
  payment.showDropdown = false;
}

function getPaymentPlaceholder(type: string): string {
  const placeholders: Record<string, string> = {
    'skrill': 'Email или ID аккаунта',
    'neteller': 'Email или ID аккаунта',
    'webmoney': 'WMID или номер кошелька',
    'qiwi': 'Номер кошелька',
    'yoomoney': 'Номер кошелька',
    'paypal': 'Email аккаунта',
    'ecopayz': 'ID аккаунта',
    'muchbetter': 'ID или телефон',
    'cryptocurrencies': 'Адрес кошелька',
    'other': 'Значение'
  };
  return placeholders[type] || 'Значение';
}

// Обработчики для CRUD
function editPlayer(player: Player) {
  currentPlayerId.value = player.id;
  formData.value = {
    first_name: player.first_name,
    last_name: player.last_name,
    middle_name: player.middle_name || '',
    birth_date: player.birth_date || '',
    locations: player.locations || [],
    payment_methods: player.payment_methods || []
  };
  
  // Заполняем контактные данные
  formContacts.value = player.contacts?.map(contact => ({ 
    id: contact.id,
    type: contact.type,
    value: contact.value,
    description: contact.description,
    searchText: getContactTypeLabel(contact.type),
    showDropdown: false,
    filteredTypes: [...contactTypes.value]
  })) || [];
  
  // Заполняем никнеймы
  formNicknames.value = player.nicknames?.map(nickname => ({
    id: nickname.id,
    nickname: nickname.nickname,
    room: nickname.room || '',
    discipline: nickname.discipline || ''
  })) || [];
  
  // Заполняем адрес
  if (player.locations && player.locations.length > 0) {
    const mainLocation = player.locations[0];
    formLocation.value = {
      id: mainLocation.id,
      country: mainLocation.country || '',
      city: mainLocation.city || '',
      address: mainLocation.address || ''
    };
  } else {
    formLocation.value = {
      country: '',
      city: '',
      address: ''
    };
  }
  
  // Заполняем платежные методы
  formPaymentMethods.value = player.payment_methods?.map(payment => ({
    id: payment.id,
    type: payment.type,
    value: payment.value,
    description: payment.description,
    searchText: getPaymentSystemLabel(payment.type),
    showDropdown: false,
    filteredSystems: [...paymentSystems.value]
  })) || [];
  
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
  // Проверка обязательных полей
  if (!formData.value.first_name?.trim()) {
    errorMessage.value = 'Имя обязательно для заполнения';
    return;
  }
  
  isSubmitting.value = true;
  errorMessage.value = null; // Сбрасываем ошибку перед отправкой
  
  // Генерируем full_name из доступных данных ФИО
  const firstName = formData.value.first_name || '';
  const lastName = formData.value.last_name || '';
  const middleName = formData.value.middle_name || '';
  
  // Исправляем ошибку компилятора, используя явное приведение типов
  if ('full_name' in formData.value) {
    formData.value.full_name = `${firstName} ${lastName} ${middleName}`.trim();
  }
  
  // Обрабатываем пустую дату рождения
  if (formData.value.birth_date === '' || formData.value.birth_date === undefined) {
    delete formData.value.birth_date;
  }
  
  // Обновляем контакты в основных данных формы
  formData.value.contacts = formContacts.value;
  
  // Обновляем никнеймы в основных данных формы
  formData.value.nicknames = formNicknames.value.filter(n => n.nickname.trim() !== '');
  
  // Добавляем локацию если есть данные
  if (formLocation.value.country || formLocation.value.city || formLocation.value.address) {
    formData.value.locations = [formLocation.value];
  }
  
  // Добавляем платежные методы
  formData.value.payment_methods = formPaymentMethods.value;
  
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
    console.error('Ошибка при сохранении игрока:', error);
    errorMessage.value = error.response?.data?.detail || 'Произошла ошибка при сохранении игрока';
  } finally {
    isSubmitting.value = false;
  }
}

function closeModal() {
  showCreateModal.value = false;
  showEditModal.value = false;
  currentPlayerId.value = null;
  formData.value = { ...defaultFormData };
  errorMessage.value = null; // Сбрасываем ошибку при закрытии окна
  formContacts.value = [];
  formLocation.value = {
    country: '',
    city: '',
    address: ''
  };
  formPaymentMethods.value = [];
  formNicknames.value = [];
}

// Утилиты для работы с платежными системами - вспомогательная функция
function getPaymentSystemLabel(type: string): string {
  const system = paymentSystems.value.find(s => s.value === type);
  return system ? system.label : type;
}

// Утилиты для работы с контактами - вспомогательная функция
function getContactTypeLabel(type: string): string {
  const contactType = contactTypes.value.find(t => t.value === type);
  return contactType ? contactType.label : type;
}

// Функции для работы с никнеймами
function addNickname() {
  formNicknames.value.push({
    nickname: '',
    room: '',
  });
}

function removeNickname(index: number) {
  formNicknames.value.splice(index, 1);
}

// Функция для получения иконки типа контакта
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
  return Object.values(playerCases.value[playerId]).reduce((sum: number, count: number) => sum + count, 0);
}

// Функция для получения данных о кейсах игроков
async function fetchPlayerCases() {
  try {
    // В реальном приложении здесь был бы запрос к API
    // Пример: const response = await axios.get('/api/v1/players/cases-summary');
    
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

// Загрузка данных при монтировании
onMounted(async () => {
  await Promise.all([
    fetchPlayers(),
    fetchFunds(),
    fetchPokerRooms()
  ]);
  
  // Загружаем данные о кейсах после получения списка игроков
  await fetchPlayerCases();
});

// Отслеживаем изменение флага showCreateModal
watch(showCreateModal, (newValue) => {
  if (newValue) {
    // При открытии модального окна создания игрока сбрасываем все значения
    formData.value = { ...defaultFormData };
    formContacts.value = [];
    formLocation.value = {
      country: '',
      city: '',
      address: ''
    };
    formPaymentMethods.value = [];
    formNicknames.value = [];
    errorMessage.value = null;
  }
});
</script> 