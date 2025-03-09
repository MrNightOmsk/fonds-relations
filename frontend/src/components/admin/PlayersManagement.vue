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
              Контакты
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Дата рождения
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Адрес
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Платежные системы
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Покерные румы
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
            <td colspan="9" class="px-6 py-4 text-center">Загрузка...</td>
          </tr>
          <tr v-else-if="filteredPlayers.length === 0">
            <td colspan="9" class="px-6 py-4 text-center">Игроки не найдены</td>
          </tr>
          <tr v-for="player in filteredPlayers" :key="player.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">
              {{ player.full_name }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div v-if="player.contacts && player.contacts.length > 0">
                <div v-for="contact in player.contacts.slice(0, 2)" :key="contact.id" class="text-sm">
                  <span class="font-medium">{{ contact.type }}:</span> {{ contact.value }}
                </div>
                <div v-if="player.contacts.length > 2" class="text-xs text-gray-500">
                  и еще {{ player.contacts.length - 2 }}...
                </div>
              </div>
              <span v-else class="text-gray-500">Не указаны</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              {{ player.birth_date ? new Date(player.birth_date).toLocaleDateString() : 'Не указана' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div v-if="player.locations && player.locations.length > 0" class="text-sm">
                <div v-if="player.locations[0].country">{{ player.locations[0].country }}</div>
                <div v-if="player.locations[0].city">{{ player.locations[0].city }}</div>
                <div v-if="player.locations[0].address" class="text-xs text-gray-500">{{ player.locations[0].address }}</div>
              </div>
              <span v-else class="text-gray-500">Не указан</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div v-if="player.payment_methods && player.payment_methods.length > 0">
                <div v-for="payment in player.payment_methods.slice(0, 2)" :key="payment.id" class="text-sm">
                  <span class="font-medium">{{ getPaymentSystemLabel(payment.type) }}:</span> {{ payment.value }}
                </div>
                <div v-if="player.payment_methods.length > 2" class="text-xs text-gray-500">
                  и еще {{ player.payment_methods.length - 2 }}...
                </div>
              </div>
              <span v-else class="text-gray-500">Не указаны</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div v-if="player.poker_ids && player.poker_ids.length > 0">
                <div v-for="poker in player.poker_ids.slice(0, 2)" :key="poker.id" class="text-sm">
                  <span class="font-medium">{{ getPokerRoomName(poker.room) }}:</span> {{ poker.nickname }}
                </div>
                <div v-if="player.poker_ids.length > 2" class="text-xs text-gray-500">
                  и еще {{ player.poker_ids.length - 2 }}...
                </div>
              </div>
              <span v-else class="text-gray-500">Не указаны</span>
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
        
        <!-- Сообщение об ошибке -->
        <div v-if="errorMessage" class="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <p>{{ errorMessage }}</p>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Имя</label>
          <input 
            type="text" 
            v-model="formData.first_name" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
            required
          >
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Фамилия</label>
          <input 
            type="text" 
            v-model="formData.last_name" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
            required
          >
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Отчество</label>
          <input 
            type="text" 
            v-model="formData.middle_name" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
          >
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Дата рождения</label>
          <input 
            type="date" 
            v-model="formData.birth_date" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
          >
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Адрес</label>
          <div class="space-y-2">
            <div class="mb-2">
              <label class="block text-sm text-gray-700 mb-1">Страна</label>
              <input 
                type="text" 
                v-model="formLocation.country" 
                class="w-full px-3 py-2 border border-gray-300 rounded-md"
                placeholder="Страна проживания"
              >
            </div>
            <div class="mb-2">
              <label class="block text-sm text-gray-700 mb-1">Город</label>
              <input 
                type="text" 
                v-model="formLocation.city" 
                class="w-full px-3 py-2 border border-gray-300 rounded-md"
                placeholder="Город проживания"
              >
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
        
        <div class="mb-4">
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
                class="flex-1 px-3 py-2 border border-gray-300 rounded-md"
                :placeholder="getContactPlaceholder(contact.type)"
              >
              <button 
                @click="removeContact(index)" 
                class="p-2 text-red-600 hover:text-red-900"
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
        
        <div class="mb-4">
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
                class="flex-1 px-3 py-2 border border-gray-300 rounded-md"
                :placeholder="getPaymentPlaceholder(payment.type)"
              >
              <button 
                @click="removePaymentMethod(index)" 
                class="p-2 text-red-600 hover:text-red-900"
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
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Ники в покерных румах</label>
          <div class="space-y-2">
            <div v-for="(pokerId, index) in formPokerIds" :key="index" class="flex items-center space-x-2">
              <div class="w-1/3 relative poker-dropdown-container">
                <input 
                  type="text" 
                  v-model="pokerId.searchText" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md"
                  placeholder="Поиск покерного рума..."
                  @input="filterPokerRooms(pokerId)"
                  @focus="pokerId.showDropdown = true"
                >
                <div v-if="pokerId.showDropdown && pokerId.filteredRooms.length > 0" 
                  class="absolute left-0 right-0 top-full mt-1 max-h-40 overflow-y-auto z-50 border border-gray-300 rounded-md bg-white shadow-lg">
                  <div 
                    v-for="room in pokerId.filteredRooms" 
                    :key="room.id"
                    class="px-3 py-2 cursor-pointer hover:bg-gray-100"
                    @mousedown.prevent="selectPokerRoom(pokerId, room)"
                  >
                    {{ room.name }}
                  </div>
                </div>
              </div>
              <input 
                type="text" 
                v-model="pokerId.nickname" 
                class="flex-1 px-3 py-2 border border-gray-300 rounded-md"
                placeholder="Никнейм в руме"
              >
              <button 
                @click="removePokerRoom(index)" 
                class="p-2 text-red-600 hover:text-red-900"
                type="button"
              >
                <span>✕</span>
              </button>
            </div>
            <button 
              @click="addPokerRoom" 
              class="text-blue-600 hover:text-blue-900 text-sm"
              type="button"
            >
              + Добавить покерный рум
            </button>
          </div>
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

// Форма
const defaultFormData: CreatePlayerRequest = {
  first_name: '',
  last_name: '',
  middle_name: '',
  birth_date: '',
  contacts: [],
  locations: [],
  payment_methods: [],
  poker_ids: []
};

const formData = ref<CreatePlayerRequest | UpdatePlayerRequest>({ ...defaultFormData });
const formContacts = ref<Partial<PlayerContact>[]>([]);
const formLocation = ref<Partial<PlayerLocation>>({
  country: '',
  city: '',
  address: ''
});
const formPaymentMethods = ref<Partial<PlayerPaymentMethod>[]>([]);
const formPokerIds = ref<any[]>([]); // Временная структура для ников в покерных румах

// Получение отфильтрованных игроков
const filteredPlayers = computed(() => {
  let result = [...players.value];
  
  if (fundFilter.value) {
    result = result.filter(p => p.created_by_fund_id === fundFilter.value);
  }
  
  return result.sort((a, b) => {
    // Сортировка по дате создания (сначала новые)
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
  
  // Закрыть все выпадающие списки покерных румов
  formPokerIds.value.forEach(pokerId => {
    if (pokerId.showDropdown && !event.composedPath().some(el => {
      const elem = el as HTMLElement;
      return elem.classList?.contains('poker-dropdown-container');
    })) {
      pokerId.showDropdown = false;
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

// Утилиты для работы с покерными румами
function addPokerRoom() {
  formPokerIds.value.push({
    room: '',
    nickname: '',
    searchText: '',
    showDropdown: false,
    filteredRooms: [...pokerRooms.value]
  });
}

function removePokerRoom(index: number) {
  formPokerIds.value.splice(index, 1);
}

function filterPokerRooms(pokerId: any) {
  const searchText = pokerId.searchText.toLowerCase();
  pokerId.filteredRooms = pokerRooms.value.filter(room => 
    room.name.toLowerCase().includes(searchText) || 
    room.id.toLowerCase().includes(searchText)
  );
  
  // Если есть точное совпадение или только один результат, автоматически устанавливаем значение
  const exactMatch = pokerId.filteredRooms.find(r => r.name.toLowerCase() === searchText);
  if (exactMatch) {
    selectPokerRoom(pokerId, exactMatch);
  }
}

function selectPokerRoom(pokerId: any, room: any) {
  pokerId.room = room.id;
  pokerId.searchText = room.name;
  pokerId.showDropdown = false;
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
    payment_methods: player.payment_methods || [],
    poker_ids: player.poker_ids || []
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
  
  // Заполняем ники в покерных румах
  formPokerIds.value = player.poker_ids?.map(poker => ({
    id: poker.id,
    room: poker.room,
    nickname: poker.nickname,
    searchText: getPokerRoomName(poker.room),
    showDropdown: false,
    filteredRooms: [...pokerRooms.value]
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
  formData.value.full_name = `${firstName} ${lastName} ${middleName}`.trim();
  
  // Обновляем контакты в основных данных формы
  formData.value.contacts = formContacts.value;
  
  // Добавляем локацию если есть данные
  if (formLocation.value.country || formLocation.value.city || formLocation.value.address) {
    formData.value.locations = [formLocation.value];
  }
  
  // Добавляем платежные методы
  formData.value.payment_methods = formPaymentMethods.value;
  
  // Добавляем ники в покерных румах
  formData.value.poker_ids = formPokerIds.value;
  
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
  formPokerIds.value = [];
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

// Загрузка данных при монтировании
onMounted(async () => {
  await Promise.all([
    fetchPlayers(),
    fetchFunds(),
    fetchPokerRooms()
  ]);
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
    formPokerIds.value = [];
    errorMessage.value = null;
  }
});
</script> 