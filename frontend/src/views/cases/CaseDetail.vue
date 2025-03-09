<template>
  <div class="case-detail p-4">
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
      <!-- Заголовок дела -->
      <div class="bg-white p-6 rounded-lg shadow-sm mb-6">
        <div class="flex justify-between items-start">
          <div>
            <h1 class="text-2xl font-medium">
              Дело #{{ currentCase.case_number || currentCase.id.substring(0, 8) }}
              <span class="ml-2 px-3 py-1 text-sm rounded-full bg-yellow-100 text-yellow-800">
                {{ currentCase.status }}
              </span>
            </h1>
            <p class="text-gray-600 mt-1">
              ID: {{ currentCase.id }}
            </p>
          </div>
          <button
            @click="isDebugMode = !isDebugMode"
            class="px-4 py-2 border rounded-lg text-gray-700 hover:bg-gray-50"
          >
            {{ isDebugMode ? 'Скрыть отладку' : 'Показать отладку' }}
          </button>
        </div>
      </div>
      
      <!-- Основная информация -->
      <div class="bg-white p-6 rounded-lg shadow-sm mb-6">
        <h2 class="text-lg font-medium mb-4">Основная информация</h2>
        
        <div class="space-y-4">
          <div>
            <h3 class="font-medium text-gray-700">Название дела:</h3>
            <p class="p-2 bg-gray-50 rounded mt-1">
              {{ currentCase.title || 'Название отсутствует' }}
            </p>
          </div>
          
          <div>
            <h3 class="font-medium text-gray-700">Описание:</h3>
            <p class="p-2 bg-gray-50 rounded mt-1 whitespace-pre-line">
              {{ currentCase.description || 'Описание отсутствует' }}
            </p>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 class="font-medium text-gray-700">Тип дела:</h3>
              <p class="p-2 bg-gray-50 rounded mt-1">
                {{ currentCase.case_type || 'Не указан' }}
              </p>
            </div>
            
            <div>
              <h3 class="font-medium text-gray-700">Статус:</h3>
              <p class="p-2 bg-gray-50 rounded mt-1">
                {{ currentCase.status || 'Не указан' }}
              </p>
            </div>
          </div>
          
          <div>
            <h3 class="font-medium text-gray-700">Сумма:</h3>
            <p class="p-2 bg-gray-50 rounded mt-1">
              {{ formatAmount(currentCase.amount, currentCase.currency) }}
            </p>
          </div>
          
          <!-- Арбитраж -->
          <div v-if="currentCase.arbitrage_type">
            <h3 class="font-medium text-gray-700">Информация об арбитраже:</h3>
            <div class="p-2 bg-gray-50 rounded mt-1 space-y-2">
              <p><strong>Тип арбитража:</strong> {{ currentCase.arbitrage_type }}</p>
              <p v-if="currentCase.arbitrage_amount">
                <strong>Сумма арбитража:</strong> {{ formatAmount(currentCase.arbitrage_amount, currentCase.arbitrage_currency) }}
              </p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Информация об игроке и фонде -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div class="bg-white p-6 rounded-lg shadow-sm">
          <h2 class="text-lg font-medium mb-4">Игрок</h2>
          
          <div v-if="currentCase.player" class="space-y-3">
            <div class="flex items-center">
              <div class="w-10 h-10 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center font-medium mr-3">
                {{ getPlayerInitials(currentCase.player) }}
              </div>
              <div>
                <div class="font-medium">{{ getPlayerFullName(currentCase.player) }}</div>
                <div class="text-sm text-gray-500">ID: {{ currentCase.player.id }}</div>
              </div>
            </div>
            
            <!-- Дополнительная информация об игроке -->
            <div class="mt-3 pt-3 border-t border-gray-100">
              <p v-if="currentCase.player.email" class="text-sm text-gray-500">
                Email: {{ currentCase.player.email }}
              </p>
              <p v-if="currentCase.player.created_at" class="text-sm text-gray-500">
                Зарегистрирован: {{ formatDate(currentCase.player.created_at) }}
              </p>
            </div>
          </div>
          <div v-else-if="currentCase.player_id" class="text-gray-500">
            <p>ID игрока: {{ currentCase.player_id }}</p>
            <p>Детальная информация об игроке недоступна</p>
          </div>
          <div v-else class="text-gray-500">
            Информация об игроке недоступна
          </div>
        </div>
        
        <div class="bg-white p-6 rounded-lg shadow-sm">
          <h2 class="text-lg font-medium mb-4">Фонд</h2>
          
          <div v-if="currentCase.fund" class="space-y-3">
            <div class="font-medium">{{ currentCase.fund.name }}</div>
            <div class="text-sm text-gray-600">{{ currentCase.fund.description }}</div>
            
            <!-- Дополнительная информация о фонде -->
            <div class="mt-3 pt-3 border-t border-gray-100">
              <p class="text-sm text-gray-500">ID фонда: {{ currentCase.fund.id }}</p>
              <p class="text-sm text-gray-500" v-if="currentCase.fund.created_at">
                Создан: {{ formatDate(currentCase.fund.created_at) }}
              </p>
            </div>
          </div>
          <div v-else-if="currentCase.created_by_fund_id" class="text-gray-500">
            <p>ID фонда: {{ currentCase.created_by_fund_id }}</p>
            <p>Детальная информация о фонде недоступна</p>
          </div>
          <div v-else class="text-gray-500">
            Информация о фонде недоступна
          </div>
        </div>
      </div>
      
      <!-- Отладочная информация -->
      <div v-if="isDebugMode" class="mt-8 p-4 bg-gray-100 rounded-lg space-y-4">
        <h3 class="text-lg font-medium mb-2">Отладочная информация (Debug Mode)</h3>
        
        <div>
          <h4 class="font-medium mb-1">Данные кейса:</h4>
          <pre class="text-xs overflow-auto p-2 bg-gray-200 rounded">{{ JSON.stringify(currentCase, null, 2) }}</pre>
        </div>
      </div>
    </div>
    
    <div v-else class="bg-white p-6 rounded-lg shadow-sm text-center my-8">
      <h2 class="text-xl font-medium text-gray-600">Дело не найдено</h2>
      <p class="mt-2 text-gray-500">Запрошенное дело не существует или было удалено</p>
      <a 
        href="/cases" 
        class="mt-4 inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Вернуться к списку дел
      </a>
    </div>
  </div>
</template>

<script>
import { useRoute } from 'vue-router';
import { defineComponent, ref, onMounted, watch } from 'vue';
import { useCasesApi } from '@/api/cases';

export default defineComponent({
  name: 'CaseDetail',
  
  setup() {
    const route = useRoute();
    const casesApi = useCasesApi();
    
    // Состояние
    const loading = ref(false);
    const error = ref(null);
    const currentCase = ref(null);
    const isDebugMode = ref(false);
    
    // Инициализация
    onMounted(async () => {
      const caseId = route.params.id;
      if (caseId) {
        await fetchCase();
      }
      console.log('Component mounted, caseId:', route.params.id);
    });
    
    // Обновление при изменении ID
    watch(() => route.params.id, async (newId) => {
      console.log('Route param changed to:', newId);
      if (newId) {
        await fetchCase();
      }
    });
    
    // Функция обновления данных
    async function fetchCase() {
      const caseId = route.params.id;
      if (!caseId) return;
      
      console.log('Fetching case with ID:', caseId);
      loading.value = true;
      error.value = null;
      
      try {
        // Получаем данные
        const caseData = await casesApi.getCaseById(caseId);
        console.log('Case data received:', caseData);
        
        // Устанавливаем значение
        currentCase.value = caseData;
        console.log('Current case set:', currentCase.value);
      } catch (err) {
        console.error('Error fetching case:', err);
        error.value = 'Не удалось загрузить дело. Пожалуйста, попробуйте позже.';
      } finally {
        loading.value = false;
        console.log('Fetch complete, loading:', loading.value);
      }
    }
    
    // Функции форматирования
    function formatAmount(amount, currency) {
      if (amount === null || amount === undefined || amount === 0) {
        return '0 ' + (currency || 'USD');
      }
      return `${amount.toFixed(2)} ${currency || 'USD'}`;
    }
    
    function formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleDateString();
    }
    
    function getPlayerInitials(player) {
      if (!player || !player.full_name) return '';
      const initials = player.full_name.split(' ').map(name => name.charAt(0)).join('');
      return initials.toUpperCase();
    }
    
    function getPlayerFullName(player) {
      if (!player || !player.full_name) return 'Имя не указано';
      return player.full_name;
    }
    
    return {
      loading,
      error,
      currentCase,
      isDebugMode,
      fetchCase,
      formatAmount,
      formatDate,
      getPlayerInitials,
      getPlayerFullName
    };
  }
});
</script>

<style scoped>
.case-detail {
  position: relative;
}
</style> 