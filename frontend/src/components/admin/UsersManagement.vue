<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">Управление пользователями</h2>
      <button @click="showCreateModal = true" class="btn-primary">
        Создать пользователя
      </button>
    </div>

    <!-- Таблица пользователей -->
    <div class="overflow-x-auto bg-white rounded-lg shadow">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Имя пользователя
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Email
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Фонд
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Роль
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Статус
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
          <tr v-else-if="users.length === 0">
            <td colspan="6" class="px-6 py-4 text-center">Пользователи не найдены</td>
          </tr>
          <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap">
              {{ user.full_name || 'Не указано' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              {{ user.email }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              {{ getFundName(user.fund_id) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="[
                'px-2 py-1 text-xs font-medium rounded-full',
                user.role === 'admin' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'
              ]">
                {{ user.role === 'admin' ? 'Администратор' : 'Менеджер' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="[
                'px-2 py-1 text-xs font-medium rounded-full',
                user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
              ]">
                {{ user.is_active ? 'Активен' : 'Не активен' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button @click="editUser(user)" class="text-blue-600 hover:text-blue-900 mr-3">
                Изменить
              </button>
              <button @click="toggleUserStatus(user)" :class="[
                user.is_active ? 'text-red-600 hover:text-red-900' : 'text-green-600 hover:text-green-900'
              ]">
                {{ user.is_active ? 'Деактивировать' : 'Активировать' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Модальное окно создания/редактирования пользователя -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full">
        <h3 class="text-lg font-semibold mb-4">
          {{ showEditModal ? 'Редактирование пользователя' : 'Создание пользователя' }}
        </h3>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input 
            type="email" 
            v-model="formData.email" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
            :disabled="showEditModal"
          >
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Полное имя</label>
          <input 
            type="text" 
            v-model="formData.full_name" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
          >
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ showEditModal ? 'Новый пароль (оставьте пустым, чтобы не менять)' : 'Пароль' }}
          </label>
          <input 
            type="password" 
            v-model="formData.password" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
            :required="!showEditModal"
          >
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Фонд</label>
          <select 
            v-model="formData.fund_id" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
          >
            <option :value="null" disabled>Выберите фонд</option>
            <option v-for="fund in funds" :key="fund.id" :value="fund.id">
              {{ fund.name }}
            </option>
          </select>
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Роль</label>
          <select 
            v-model="formData.role" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
          >
            <option value="admin">Администратор</option>
            <option value="manager">Менеджер</option>
          </select>
        </div>
        
        <div class="mb-4" v-if="showEditModal">
          <label class="block text-sm font-medium text-gray-700 mb-1">Статус</label>
          <select 
            v-model="formData.is_active" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
          >
            <option :value="true">Активен</option>
            <option :value="false">Не активен</option>
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
            @click="saveUser" 
            class="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-dark"
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? 'Сохранение...' : 'Сохранить' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useUsersApi } from '@/api/users';
import { useFundsApi } from '@/api/funds';
import type { User, Fund, CreateUserRequest, UpdateUserRequest } from '@/types/models';

// API клиенты
const usersApi = useUsersApi();
const fundsApi = useFundsApi();

// Состояние
const users = ref<User[]>([]);
const funds = ref<Fund[]>([]);
const loading = ref(true);
const showCreateModal = ref(false);
const showEditModal = ref(false);
const isSubmitting = ref(false);
const currentUserId = ref<string | null>(null);

// Форма
const defaultFormData: CreateUserRequest = {
  email: '',
  password: '',
  full_name: '',
  fund_id: '',
  role: 'manager',
  is_active: true
};

const formData = ref<CreateUserRequest | UpdateUserRequest>({ ...defaultFormData });

// Получение данных
async function fetchUsers() {
  loading.value = true;
  try {
    users.value = await usersApi.getUsers();
  } catch (error) {
    console.error('Ошибка при получении пользователей:', error);
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

// Обработчики для CRUD
function editUser(user: User) {
  currentUserId.value = user.id;
  formData.value = {
    email: user.email,
    full_name: user.full_name,
    password: '', // Пустой пароль, чтобы не менять его если не нужно
    fund_id: user.fund_id,
    role: user.role,
    is_active: user.is_active
  };
  showEditModal.value = true;
}

async function saveUser() {
  isSubmitting.value = true;
  try {
    if (showEditModal.value && currentUserId.value) {
      // Обновление пользователя
      // Удаляем пустой пароль, если он не был изменен
      const userData = { ...formData.value };
      if (!userData.password) {
        delete userData.password;
      }
      
      await usersApi.updateUser(currentUserId.value, userData as UpdateUserRequest);
    } else {
      // Создание пользователя
      await usersApi.createUser(formData.value as CreateUserRequest);
    }
    
    // Перезагрузка списка пользователей
    await fetchUsers();
    closeModal();
  } catch (error: any) {
    alert(`Ошибка: ${error.response?.data?.detail || 'Что-то пошло не так'}`);
  } finally {
    isSubmitting.value = false;
  }
}

async function toggleUserStatus(user: User) {
  try {
    await usersApi.toggleUserStatus(user.id, !user.is_active);
    // Обновляем статус в локальном состоянии
    const index = users.value.findIndex(u => u.id === user.id);
    if (index !== -1) {
      users.value[index].is_active = !user.is_active;
    }
  } catch (error: any) {
    alert(`Ошибка: ${error.response?.data?.detail || 'Что-то пошло не так'}`);
  }
}

function closeModal() {
  showCreateModal.value = false;
  showEditModal.value = false;
  currentUserId.value = null;
  formData.value = { ...defaultFormData };
}

// Вспомогательные функции
function getFundName(fundId: string): string {
  const fund = funds.value.find(f => f.id === fundId);
  return fund ? fund.name : 'Неизвестный фонд';
}

// Загрузка данных при монтировании
onMounted(async () => {
  await Promise.all([fetchUsers(), fetchFunds()]);
});
</script> 