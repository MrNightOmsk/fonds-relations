<template>
  <div class="cases-list">
    <div class="page-header mb-6">
      <h1 class="text-2xl font-bold text-text-light dark:text-text-dark">Список кейсов</h1>
      <div class="mt-2 text-gray-600 dark:text-gray-400">Управление и просмотр всех кейсов в системе</div>
    </div>
    
    <!-- Панель фильтров и поиска -->
    <div class="filters-panel bg-white dark:bg-background-dark p-4 rounded-lg shadow-sm mb-6 border border-border-light dark:border-border-dark">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="search-box">
          <label for="search" class="block text-sm font-medium text-text-light dark:text-text-dark mb-1">Поиск</label>
          <input 
            type="text" 
            id="search" 
            v-model="searchQuery" 
            placeholder="Поиск по названию или игроку..." 
            class="w-full px-3 py-2 border border-border-light dark:border-border-dark rounded-md text-text-light dark:text-text-dark bg-white dark:bg-background-dark"
          >
        </div>
        
        <div class="status-filter">
          <label for="status" class="block text-sm font-medium text-text-light dark:text-text-dark mb-1">Статус</label>
          <select 
            id="status" 
            v-model="statusFilter" 
            class="w-full px-3 py-2 border border-border-light dark:border-border-dark rounded-md text-text-light dark:text-text-dark bg-white dark:bg-background-dark"
          >
            <option value="">Все статусы</option>
            <option value="open">Открыт</option>
            <option value="in_progress">В работе</option>
            <option value="resolved">Решён</option>
            <option value="closed">Закрыт</option>
          </select>
        </div>
        
        <div class="date-filter">
          <label for="date" class="block text-sm font-medium text-text-light dark:text-text-dark mb-1">Период</label>
          <select 
            id="date" 
            v-model="dateFilter" 
            class="w-full px-3 py-2 border border-border-light dark:border-border-dark rounded-md text-text-light dark:text-text-dark bg-white dark:bg-background-dark"
          >
            <option value="">Все время</option>
            <option value="today">Сегодня</option>
            <option value="week">Эта неделя</option>
            <option value="month">Этот месяц</option>
            <option value="year">Этот год</option>
          </select>
        </div>
      </div>
      
      <!-- Кнопки управления -->
      <div class="flex justify-between items-center mt-4">
        <div class="text-sm text-text-secondary-light dark:text-text-secondary-dark">
          Найдено кейсов: <span class="font-medium">{{ totalCasesCount }}</span>
        </div>
        <div class="flex space-x-2">
          <button @click="showCreateCaseModal = true" class="px-3 py-2 bg-primary dark:bg-primary-dark text-white rounded-md hover:bg-primary-600 dark:hover:bg-primary-500">
            <span class="hidden md:inline">Создать новый кейс</span>
            <span class="md:hidden">+ Кейс</span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Список кейсов -->
    <div class="cases-container">
      <div v-if="loading" class="text-center py-8">
        <div class="inline-block animate-spin h-6 w-6 border-2 border-primary dark:border-primary-dark rounded-full border-t-transparent mb-2"></div>
        <p class="text-text-secondary-light dark:text-text-secondary-dark">Загрузка кейсов...</p>
      </div>
      
      <div v-else-if="cases.length === 0" class="text-center py-8 bg-white dark:bg-background-dark rounded-lg shadow-sm border border-border-light dark:border-border-dark">
        <p class="text-lg text-text-secondary-light dark:text-text-secondary-dark">Нет кейсов, соответствующих выбранным фильтрам</p>
        <button 
          @click="clearFilters" 
          class="mt-2 text-primary dark:text-primary-dark hover:underline"
        >
          Сбросить фильтры
        </button>
      </div>
      
      <div v-else class="bg-white dark:bg-background-dark rounded-lg shadow-sm overflow-hidden border border-border-light dark:border-border-dark">
        <!-- Заголовок таблицы -->
        <div class="hidden md:grid md:grid-cols-6 bg-surface-light dark:bg-surface-dark p-3 border-b border-border-light dark:border-border-dark text-sm font-medium text-text-light dark:text-text-dark">
          <div class="col-span-2">Название</div>
          <div>Игрок</div>
          <div>Статус</div>
          <div>Создан</div>
          <div>Действия</div>
        </div>
        
        <!-- Строки таблицы -->
        <div v-for="case_item in cases" :key="case_item.id" class="border-b border-border-light dark:border-border-dark last:border-b-0">
          <!-- Мобильный вид -->
          <div class="md:hidden p-3">
            <div class="flex justify-between items-start mb-2">
              <h3 class="font-medium text-text-light dark:text-text-dark">{{ case_item.title }}</h3>
              <span :class="getStatusClass(case_item.status)" class="text-xs px-2 py-1 rounded-full">
                {{ getStatusText(case_item.status) }}
              </span>
            </div>
            <div class="text-sm text-text-secondary-light dark:text-text-secondary-dark">
              <p v-if="case_item.player_name">Игрок: {{ case_item.player_name }}</p>
              <p>Создан: {{ formatDate(case_item.created_at) }}</p>
            </div>
            <div class="mt-2 flex space-x-2">
              <button 
                @click="navigateToCase(case_item.id)" 
                class="px-2 py-1 text-sm bg-primary/10 dark:bg-primary-dark/20 text-primary dark:text-primary-dark rounded hover:bg-primary/20 dark:hover:bg-primary-dark/30"
              >
                Просмотр
              </button>
              <button 
                v-if="canEditCase(case_item)"
                @click="editCase(case_item)" 
                class="px-2 py-1 text-sm bg-surface-light dark:bg-surface-dark text-text-light dark:text-text-dark rounded hover:bg-gray-200 dark:hover:bg-gray-700"
              >
                Редактировать
              </button>
            </div>
          </div>
          
          <!-- Десктопный вид -->
          <div class="hidden md:grid md:grid-cols-6 p-3 items-center hover:bg-surface-light dark:hover:bg-surface-dark">
            <div class="col-span-2 font-medium text-text-light dark:text-text-dark">{{ case_item.title }}</div>
            <div class="text-text-light dark:text-text-dark">{{ case_item.player_name || 'Не указан' }}</div>
            <div>
              <span :class="getStatusClass(case_item.status)" class="text-xs px-2 py-1 rounded-full">
                {{ getStatusText(case_item.status) }}
              </span>
            </div>
            <div class="text-sm text-text-secondary-light dark:text-text-secondary-dark">{{ formatDate(case_item.created_at) }}</div>
            <div class="flex space-x-2">
              <button 
                @click="navigateToCase(case_item.id)" 
                class="px-2 py-1 text-sm bg-primary/10 dark:bg-primary-dark/20 text-primary dark:text-primary-dark rounded hover:bg-primary/20 dark:hover:bg-primary-dark/30"
              >
                Просмотр
              </button>
              <button 
                v-if="canEditCase(case_item)"
                @click="editCase(case_item)" 
                class="px-2 py-1 text-sm bg-surface-light dark:bg-surface-dark text-text-light dark:text-text-dark rounded hover:bg-gray-200 dark:hover:bg-gray-700"
              >
                Редактировать
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Пагинация -->
    <div v-if="totalPages > 1" class="pagination mt-4 flex justify-center">
      <div class="flex space-x-1">
        <button 
          @click="currentPage = 1" 
          :disabled="currentPage === 1"
          class="pagination-btn bg-white dark:bg-background-dark border border-border-light dark:border-border-dark text-text-light dark:text-text-dark" 
          :class="{'opacity-50 cursor-not-allowed': currentPage === 1}"
        >
          &laquo;
        </button>
        <button 
          @click="currentPage--" 
          :disabled="currentPage === 1"
          class="pagination-btn bg-white dark:bg-background-dark border border-border-light dark:border-border-dark text-text-light dark:text-text-dark" 
          :class="{'opacity-50 cursor-not-allowed': currentPage === 1}"
        >
          &lsaquo;
        </button>
        
        <template v-for="page in displayedPages" :key="page">
          <button 
            v-if="page === '...'" 
            class="pagination-btn bg-white dark:bg-background-dark border border-border-light dark:border-border-dark text-text-light dark:text-text-dark opacity-50 cursor-default"
          >
            ...
          </button>
          <button 
            v-else
            @click="currentPage = page" 
            class="pagination-btn border border-border-light dark:border-border-dark" 
            :class="{'bg-primary dark:bg-primary-dark text-white': currentPage === page, 'bg-white dark:bg-background-dark text-text-light dark:text-text-dark': currentPage !== page}"
          >
            {{ page }}
          </button>
        </template>
        
        <button 
          @click="currentPage++" 
          :disabled="currentPage === totalPages"
          class="pagination-btn bg-white dark:bg-background-dark border border-border-light dark:border-border-dark text-text-light dark:text-text-dark" 
          :class="{'opacity-50 cursor-not-allowed': currentPage === totalPages}"
        >
          &rsaquo;
        </button>
        <button 
          @click="currentPage = totalPages" 
          :disabled="currentPage === totalPages"
          class="pagination-btn bg-white dark:bg-background-dark border border-border-light dark:border-border-dark text-text-light dark:text-text-dark" 
          :class="{'opacity-50 cursor-not-allowed': currentPage === totalPages}"
        >
          &raquo;
        </button>
      </div>
    </div>
    
    <!-- Модальное окно создания кейса -->
    <CreateCaseModal :show="showCreateCaseModal" @close="showCreateCaseModal = false" @created="handleCaseCreated" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import CreateCaseModal from '@/components/case/CreateCaseModal.vue';
import { useAuthStore } from '@/stores/auth';

interface Case {
  id: string;
  title: string;
  status: string;
  player_name?: string;
  player_id?: string;
  created_at?: string;
  updated_at?: string;
}

// Роутер
const router = useRouter();
const authStore = useAuthStore();

// Состояние компонента
const loading = ref(true);
const cases = ref<Case[]>([]);
const searchQuery = ref('');
const statusFilter = ref('');
const dateFilter = ref('');
const currentPage = ref(1);
const itemsPerPage = 10;
const showCreateCaseModal = ref(false);
const totalCasesCount = ref(0);
const casesApi = ref<any>(null);

// Загрузка данных с сервера с учетом фильтров и пагинации
const loadCases = async () => {
  if (!casesApi.value) {
    casesApi.value = (await import('@/api/cases')).useCasesApi();
  }

  loading.value = true;
  
  try {
    // Проверяем, является ли пользователь менеджером для установки правильного лимита
    const isManager = authStore.user && authStore.user.role === 'manager';
    
    // Формируем параметры запроса
    const params: any = {
      page: currentPage.value,
      limit: isManager ? 100 : itemsPerPage, // Для менеджеров увеличиваем лимит
      offset: (currentPage.value - 1) * (isManager ? 100 : itemsPerPage)
    };
    
    // Добавляем фильтры, если они заданы
    if (searchQuery.value.trim()) {
      params.search = searchQuery.value.trim();
    }
    
    if (statusFilter.value) {
      params.status = statusFilter.value;
    }
    
    if (dateFilter.value) {
      params.period = dateFilter.value;
    }
    
    console.log('Загрузка кейсов с параметрами:', params);
    
    // Запрашиваем данные с учетом фильтров и пагинации
    const response = await casesApi.value.getAccessibleCases(params);
    
    // Обновляем данные и общее количество
    cases.value = response.results || [];
    totalCasesCount.value = response.count || 0;
    
    console.log(`Загружено ${cases.value.length} кейсов из ${totalCasesCount.value}`);
  } catch (error) {
    console.error('Ошибка при загрузке кейсов:', error);
    cases.value = [];
    totalCasesCount.value = 0;
  } finally {
    loading.value = false;
  }
};

// Фильтрация кейсов больше не нужна, так как фильтры работают на сервере
// Но пока оставим для обратной совместимости
const filteredCases = computed(() => cases.value);

// Пагинация
const totalPages = computed(() => {
  return Math.max(1, Math.ceil(totalCasesCount.value / itemsPerPage));
});

// Определение отображаемых страниц для пагинации
const displayedPages = computed(() => {
  const total = totalPages.value;
  const current = currentPage.value;
  
  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1);
  }
  
  // Когда много страниц, показываем только часть с многоточиями
  const pages = [];
  
  if (current <= 3) {
    // В начале списка
    for (let i = 1; i <= 5; i++) {
      pages.push(i);
    }
    pages.push('...');
    pages.push(total);
  } else if (current >= total - 2) {
    // В конце списка
    pages.push(1);
    pages.push('...');
    for (let i = total - 4; i <= total; i++) {
      pages.push(i);
    }
  } else {
    // В середине списка
    pages.push(1);
    pages.push('...');
    for (let i = current - 1; i <= current + 1; i++) {
      pages.push(i);
    }
    pages.push('...');
    pages.push(total);
  }
  
  return pages;
});

// Сброс фильтров
const clearFilters = () => {
  searchQuery.value = '';
  statusFilter.value = '';
  dateFilter.value = '';
  currentPage.value = 1;
  
  // После сброса фильтров загружаем данные заново
  loadCases();
};

// Действия с кейсами
const navigateToCase = (caseId: string) => {
  router.push(`/cases/${caseId}`);
};

const editCase = (case_item: Case) => {
  router.push(`/cases/${case_item.id}/edit`);
};

const handleCaseCreated = (newCase: Case) => {
  showCreateCaseModal.value = false;
  cases.value.unshift(newCase);
  router.push(`/cases/${newCase.id}`);
};

// Вспомогательные функции
const formatDate = (dateString?: string): string => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString('ru-RU', { 
    day: '2-digit', 
    month: '2-digit', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const getStatusText = (status: string): string => {
  const statusMap: Record<string, string> = {
    'open': 'Открыт',
    'in_progress': 'В работе',
    'resolved': 'Решён',
    'closed': 'Закрыт'
  };
  return statusMap[status] || status;
};

const getStatusClass = (status: string): string => {
  const statusClasses: Record<string, string> = {
    'open': 'bg-yellow-100 text-yellow-800',
    'in_progress': 'bg-blue-100 text-blue-800',
    'resolved': 'bg-green-100 text-green-800',
    'closed': 'bg-gray-100 text-gray-800'
  };
  return statusClasses[status] || 'bg-gray-100 text-gray-800';
};

const canEditCase = (case_item: Case): boolean => {
  // Получаем текущего пользователя из хранилища аутентификации
  const authStore = useAuthStore();
  if (!authStore.user) return false;
  
  // Админы могут редактировать любые кейсы
  if (authStore.user.role === 'admin') return true;
  
  // Менеджеры могут редактировать только кейсы своего фонда
  return case_item.created_by_fund_id === authStore.user.fund_id;
};

// Сброс текущей страницы при изменении фильтров и загрузка данных
watch([searchQuery, statusFilter, dateFilter], () => {
  currentPage.value = 1;
  loadCases();
});

// Загрузка данных при изменении страницы
watch(currentPage, () => {
  loadCases();
});

// Загрузка данных при монтировании компонента
onMounted(async () => {
  // Инициализируем API и загружаем данные
  await loadCases();
});
</script>

<style scoped>
.cases-list {
  padding: 1.5rem;
}

.pagination-btn {
  @apply px-3 py-1 rounded-md text-sm font-medium transition-colors;
}
</style> 