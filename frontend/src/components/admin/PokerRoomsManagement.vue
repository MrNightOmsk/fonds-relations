<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">Управление покерными румами</h2>
      <button @click="showCreateModal = true" class="btn-primary">
        Добавить покерный рум
      </button>
    </div>

    <!-- Поиск покерных румов -->
    <div class="mb-4">
      <div class="relative">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Поиск покерных румов по названию или идентификатору..." 
          class="w-full px-4 py-2 border border-gray-300 rounded-md"
        />
        <span v-if="searchQuery" 
          @click="searchQuery = ''" 
          class="absolute right-3 top-1/2 transform -translate-y-1/2 cursor-pointer text-gray-500 hover:text-gray-700">
          ✕
        </span>
      </div>
    </div>

    <!-- Таблица покерных румов -->
    <div class="overflow-x-auto bg-white rounded-lg shadow">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Название
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Идентификатор
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Описание
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Активен
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
          <tr v-else-if="pokerRooms.length === 0">
            <td colspan="6" class="px-6 py-4 text-center">Покерные румы не найдены</td>
          </tr>
          <tr v-for="room in sortedPokerRooms" :key="room.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">
              {{ room.name }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              {{ room.id }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              {{ room.description || 'Нет описания' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span 
                :class="[
                  'px-2 py-1 text-xs rounded-full', 
                  room.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                ]"
              >
                {{ room.is_active ? 'Активен' : 'Не активен' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ new Date(room.created_at).toLocaleDateString() }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button @click="editRoom(room)" class="text-blue-600 hover:text-blue-900 mr-3">
                Изменить
              </button>
              <button @click="confirmDeleteRoom(room)" class="text-red-600 hover:text-red-900">
                Удалить
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Модальное окно создания/редактирования покерного рума -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full">
        <h3 class="text-lg font-semibold mb-4">
          {{ showEditModal ? 'Редактирование покерного рума' : 'Добавление покерного рума' }}
        </h3>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Название</label>
          <input 
            type="text" 
            v-model="formData.name" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
            required
          >
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Идентификатор</label>
          <input 
            type="text" 
            v-model="formData.id" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
            required
            :disabled="showEditModal"
            placeholder="pokerstars, ggpoker, и т.д."
          >
          <p class="text-xs text-gray-500 mt-1">Уникальный идентификатор для покерного рума (только латинские буквы, цифры и нижнее подчеркивание)</p>
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
          <div class="flex items-center space-x-2">
            <input 
              type="checkbox" 
              id="is_active" 
              v-model="formData.is_active" 
              class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
            >
            <label for="is_active" class="text-sm text-gray-700">Активен</label>
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
            @click="saveRoom" 
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
          Вы уверены, что хотите удалить покерный рум "{{ roomToDelete?.name }}"? Это действие может повлиять на данные игроков, использующих этот рум.
        </p>
        <div class="flex justify-end space-x-2">
          <button 
            @click="showDeleteConfirm = false" 
            class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
          >
            Отмена
          </button>
          <button 
            @click="deleteRoomConfirmed" 
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

interface PokerRoom {
  id: string;
  name: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// Состояние
const pokerRooms = ref<PokerRoom[]>([]);
const loading = ref(true);
const showCreateModal = ref(false);
const showEditModal = ref(false);
const showDeleteConfirm = ref(false);
const isSubmitting = ref(false);
const roomToDelete = ref<PokerRoom | null>(null);
const searchQuery = ref('');

// Форма
const defaultFormData: Partial<PokerRoom> = {
  id: '',
  name: '',
  description: '',
  is_active: true
};

const formData = ref<Partial<PokerRoom>>({ ...defaultFormData });

// Фильтрованные покерные румы по поиску
const sortedPokerRooms = computed(() => {
  let result = [...pokerRooms.value];
  
  // Применяем поиск если есть запрос
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(room => 
      room.name.toLowerCase().includes(query) || 
      room.id.toLowerCase().includes(query) ||
      (room.description && room.description.toLowerCase().includes(query))
    );
  }
  
  // Сортировка по названию (A-Z)
  return result.sort((a, b) => {
    return a.name.localeCompare(b.name);
  });
});

// Получение данных
async function fetchPokerRooms() {
  loading.value = true;
  try {
    // Здесь будет API запрос на получение списка покерных румов
    // Временно заполняем тестовыми данными
    pokerRooms.value = [
      { 
        id: 'pokerstars', 
        name: 'PokerStars', 
        description: 'Самый крупный покерный рум в мире', 
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      { 
        id: 'ggpoker', 
        name: 'GGPoker', 
        description: 'Быстро растущий покерный рум с множеством промо-акций', 
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      { 
        id: 'partypoker', 
        name: 'PartyPoker', 
        description: 'Один из старейших покерных румов с обновленным софтом', 
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      { 
        id: '888poker', 
        name: '888poker', 
        description: 'Популярный покерный рум от компании 888 Holdings', 
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      { 
        id: 'winamax', 
        name: 'Winamax', 
        description: 'Популярный европейский покерный рум', 
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      { 
        id: 'acr', 
        name: 'Americas Cardroom', 
        description: 'Американский покерный рум', 
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      { 
        id: 'wpn', 
        name: 'Winning Poker Network', 
        description: 'Сеть покерных румов', 
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      { 
        id: 'ipoker', 
        name: 'iPoker Network', 
        description: 'Сеть покерных румов от Playtech', 
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      { 
        id: 'chico', 
        name: 'Chico Poker Network', 
        description: 'Сеть покерных румов', 
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      { 
        id: 'ignition', 
        name: 'Ignition Poker', 
        description: 'Покерный рум с анонимными столами', 
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }
    ];
  } catch (error) {
    console.error('Ошибка при получении покерных румов:', error);
  } finally {
    loading.value = false;
  }
}

// Обработчики для CRUD
function editRoom(room: PokerRoom) {
  formData.value = { ...room };
  showEditModal.value = true;
}

function confirmDeleteRoom(room: PokerRoom) {
  roomToDelete.value = room;
  showDeleteConfirm.value = true;
}

async function deleteRoomConfirmed() {
  if (!roomToDelete.value) return;
  
  isSubmitting.value = true;
  try {
    // Здесь будет API запрос на удаление покерного рума
    
    // Удаляем из локального состояния
    pokerRooms.value = pokerRooms.value.filter(r => r.id !== roomToDelete.value?.id);
    showDeleteConfirm.value = false;
  } catch (error: any) {
    alert(`Ошибка: ${error.response?.data?.detail || 'Что-то пошло не так'}`);
  } finally {
    isSubmitting.value = false;
  }
}

async function saveRoom() {
  isSubmitting.value = true;
  
  try {
    if (showEditModal.value) {
      // Обновление покерного рума
      const roomIndex = pokerRooms.value.findIndex(r => r.id === formData.value.id);
      if (roomIndex !== -1) {
        // Здесь будет API запрос на обновление
        
        // Обновляем в локальном состоянии
        pokerRooms.value[roomIndex] = {
          ...pokerRooms.value[roomIndex],
          ...formData.value,
          updated_at: new Date().toISOString()
        } as PokerRoom;
      }
    } else {
      // Создание покерного рума
      // Здесь будет API запрос на создание
      
      // Добавляем в локальное состояние
      const now = new Date().toISOString();
      const newRoom: PokerRoom = {
        ...formData.value as PokerRoom,
        created_at: now,
        updated_at: now
      };
      pokerRooms.value.push(newRoom);
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
  formData.value = { ...defaultFormData };
}

// Загрузка данных при монтировании
onMounted(async () => {
  await fetchPokerRooms();
});
</script> 