<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">Управление фондами</h2>
      <button @click="showCreateModal = true" class="btn-primary">
        Создать фонд
      </button>
    </div>

    <!-- Таблица фондов -->
    <div class="overflow-x-auto bg-white rounded-lg shadow">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Название
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Описание
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Пользователей
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Дата создания
            </th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              Действия
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-if="loading">
            <td colspan="5" class="px-6 py-4 text-center">Загрузка...</td>
          </tr>
          <tr v-else-if="funds.length === 0">
            <td colspan="5" class="px-6 py-4 text-center">Фонды не найдены</td>
          </tr>
          <tr v-for="fund in funds" :key="fund.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">
              {{ fund.name }}
            </td>
            <td class="px-6 py-4">
              <div class="text-sm text-gray-900 max-w-xs truncate">
                {{ fund.description || 'Нет описания' }}
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                {{ getUserCountByFund(fund.id) }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ new Date(fund.created_at).toLocaleDateString() }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button @click="editFund(fund)" class="text-blue-600 hover:text-blue-900 mr-3">
                Изменить
              </button>
              <button 
                @click="confirmDeleteFund(fund)" 
                class="text-red-600 hover:text-red-900"
                :disabled="getUserCountByFund(fund.id) > 0"
                :class="{ 'opacity-50 cursor-not-allowed': getUserCountByFund(fund.id) > 0 }"
              >
                Удалить
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Модальное окно создания/редактирования фонда -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full">
        <h3 class="text-lg font-semibold mb-4">
          {{ showEditModal ? 'Редактирование фонда' : 'Создание фонда' }}
        </h3>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Название фонда</label>
          <input 
            type="text" 
            v-model="formData.name" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
            required
          >
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Описание</label>
          <textarea 
            v-model="formData.description" 
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md"
          ></textarea>
        </div>
        
        <div class="flex justify-end space-x-2">
          <button 
            @click="closeModal" 
            class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
          >
            Отмена
          </button>
          <button 
            @click="saveFund" 
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
          Вы уверены, что хотите удалить фонд "{{ fundToDelete?.name }}"? Это действие необратимо.
        </p>
        <div class="flex justify-end space-x-2">
          <button 
            @click="showDeleteConfirm = false" 
            class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
          >
            Отмена
          </button>
          <button 
            @click="deleteFund" 
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
import { ref, onMounted, computed } from 'vue';
import { useFundsApi } from '@/api/funds';
import { useUsersApi } from '@/api/users';
import type { Fund, User, CreateFundRequest, UpdateFundRequest } from '@/types/models';

// API клиенты
const fundsApi = useFundsApi();
const usersApi = useUsersApi();

// Состояние
const funds = ref<Fund[]>([]);
const users = ref<User[]>([]);
const loading = ref(true);
const showCreateModal = ref(false);
const showEditModal = ref(false);
const showDeleteConfirm = ref(false);
const isSubmitting = ref(false);
const currentFundId = ref<string | null>(null);
const fundToDelete = ref<Fund | null>(null);

// Форма
const defaultFormData: CreateFundRequest = {
  name: '',
  description: ''
};

const formData = ref<CreateFundRequest | UpdateFundRequest>({ ...defaultFormData });

// Получение данных
async function fetchFunds() {
  loading.value = true;
  try {
    funds.value = await fundsApi.getFunds();
  } catch (error) {
    console.error('Ошибка при получении фондов:', error);
  } finally {
    loading.value = false;
  }
}

async function fetchUsers() {
  try {
    users.value = await usersApi.getUsers();
  } catch (error) {
    console.error('Ошибка при получении пользователей:', error);
  }
}

// Обработчики для CRUD
function editFund(fund: Fund) {
  currentFundId.value = fund.id;
  formData.value = {
    name: fund.name,
    description: fund.description || ''
  };
  showEditModal.value = true;
}

function confirmDeleteFund(fund: Fund) {
  if (getUserCountByFund(fund.id) > 0) {
    alert('Невозможно удалить фонд, к которому привязаны пользователи');
    return;
  }
  
  fundToDelete.value = fund;
  showDeleteConfirm.value = true;
}

async function saveFund() {
  isSubmitting.value = true;
  try {
    if (showEditModal.value && currentFundId.value) {
      // Обновление фонда
      await fundsApi.updateFund(currentFundId.value, formData.value as UpdateFundRequest);
    } else {
      // Создание фонда
      await fundsApi.createFund(formData.value as CreateFundRequest);
    }
    
    // Перезагрузка списка фондов
    await fetchFunds();
    closeModal();
  } catch (error: any) {
    alert(`Ошибка: ${error.response?.data?.detail || 'Что-то пошло не так'}`);
  } finally {
    isSubmitting.value = false;
  }
}

async function deleteFund() {
  if (!fundToDelete.value) return;
  
  isSubmitting.value = true;
  try {
    await fundsApi.deleteFund(fundToDelete.value.id);
    
    // Удаление из локального состояния
    funds.value = funds.value.filter(fund => fund.id !== fundToDelete.value?.id);
    closeDeleteModal();
  } catch (error: any) {
    alert(`Ошибка: ${error.response?.data?.detail || 'Что-то пошло не так'}`);
  } finally {
    isSubmitting.value = false;
  }
}

function closeModal() {
  showCreateModal.value = false;
  showEditModal.value = false;
  currentFundId.value = null;
  formData.value = { ...defaultFormData };
}

function closeDeleteModal() {
  showDeleteConfirm.value = false;
  fundToDelete.value = null;
}

// Вспомогательные функции
function getUserCountByFund(fundId: string): number {
  return users.value.filter(user => user.fund_id === fundId).length;
}

// Загрузка данных при монтировании
onMounted(async () => {
  await Promise.all([fetchFunds(), fetchUsers()]);
});
</script> 