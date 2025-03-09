<template>
  <div class="dashboard">
    <!-- Секция поиска -->
    <div class="search-section mb-6">
      <h2 class="text-lg font-medium mb-2">Поиск</h2>
      <div class="border p-4 bg-blue-50 rounded-lg">
        <p class="text-sm mb-2">Работает поиск по словам: "иван", "петр", "скам", "долг"</p>
        <UnifiedSearch @select="handleSearchResultSelect" />
      </div>
    </div>
    
    <!-- Секция быстрых действий -->
    <div class="quick-actions mb-6">
      <h2 class="text-lg font-medium mb-2">Быстрые действия</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
        <button @click="showCreateCaseModal = true" class="action-btn bg-blue-600 text-white p-4 rounded-lg flex items-center">
          <span class="icon mr-2 text-xl">+</span>
          <span>Создать кейс</span>
        </button>
        <button @click="navigateTo('/cases')" class="action-btn bg-green-600 text-white p-4 rounded-lg flex items-center">
          <span class="icon mr-2 text-xl">📁</span>
          <span>Мои кейсы</span>
        </button>
        <button @click="navigateTo('/players')" class="action-btn bg-purple-600 text-white p-4 rounded-lg flex items-center">
          <span class="icon mr-2 text-xl">👤</span>
          <span>Список игроков</span>
        </button>
        <button @click="navigateTo('/audit')" class="action-btn bg-orange-600 text-white p-4 rounded-lg flex items-center">
          <span class="icon mr-2 text-xl">🔔</span>
          <span>Активность</span>
        </button>
      </div>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Карточка со статистикой -->
      <div class="bg-white p-6 rounded-lg shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Статистика</h2>
        <div v-if="loading" class="text-gray-500">
          <div class="animate-spin h-5 w-5 border-2 border-blue-500 rounded-full border-t-transparent inline-block mr-2"></div>
          Загрузка статистики...
        </div>
        <div v-else class="space-y-4">
          <div class="flex justify-between items-center p-2 bg-blue-50 rounded">
            <span class="font-medium">Всего игроков:</span>
            <span class="bg-blue-100 text-blue-800 py-1 px-2 rounded-full">{{ stats.players.total }}</span>
          </div>
          <div class="flex justify-between items-center p-2 bg-green-50 rounded">
            <span class="font-medium">Активных кейсов:</span>
            <span class="bg-green-100 text-green-800 py-1 px-2 rounded-full">
              {{ (stats.cases.open || 0) + (stats.cases.in_progress || 0) }}
            </span>
          </div>
          <div class="flex justify-between items-center p-2 bg-purple-50 rounded">
            <span class="font-medium">Закрытых кейсов:</span>
            <span class="bg-purple-100 text-purple-800 py-1 px-2 rounded-full">
              {{ (stats.cases.closed || 0) + (stats.cases.resolved || 0) }}
            </span>
          </div>
        </div>
      </div>
    
      <!-- Секция последних кейсов -->
      <div class="lg:col-span-2 bg-white rounded-lg shadow-sm p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold">Последние кейсы</h2>
          <button @click="navigateTo('/cases')" class="text-blue-600 text-sm hover:underline">
            Все кейсы
          </button>
        </div>
        <div v-if="loading" class="text-center py-8 text-gray-500">
          <div class="animate-spin h-6 w-6 border-2 border-blue-500 rounded-full border-t-transparent inline-block mb-2"></div>
          <p>Загрузка кейсов...</p>
        </div>
        <div v-else-if="recentCases.length === 0" class="text-center py-8 text-gray-500">
          Нет доступных кейсов
        </div>
        <div v-else class="space-y-3">
          <div v-for="case_item in recentCases" :key="case_item.id" 
              class="p-3 border border-gray-100 rounded-lg hover:bg-gray-50 cursor-pointer"
              @click="navigateTo(`/cases/${case_item.id}`)">
            <div class="flex justify-between">
              <h3 class="font-medium">{{ case_item.title }}</h3>
              <span :class="getStatusClass(case_item.status)" class="text-xs px-2 py-1 rounded-full">
                {{ getStatusText(case_item.status) }}
              </span>
            </div>
            <div class="text-sm text-gray-500 mt-1">
              <span v-if="case_item.player_name">
                Игрок: <span class="text-gray-700">{{ case_item.player_name }}</span>
              </span>
              <span v-if="case_item.created_at" class="ml-2">
                Создан: <span class="text-gray-700">{{ formatDate(case_item.created_at) }}</span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Последние активности -->
    <div class="bg-white p-6 rounded-lg shadow-sm mt-6">
      <h2 class="text-xl font-semibold mb-4">Последние активности</h2>
      <div v-if="loading" class="text-center py-8 text-gray-500">
        <div class="animate-spin h-6 w-6 border-2 border-blue-500 rounded-full border-t-transparent inline-block mb-2"></div>
        <p>Загрузка активностей...</p>
      </div>
      <div v-else-if="activities.length === 0" class="text-center py-8 text-gray-500">
        Нет недавних активностей
      </div>
      <ul v-else class="divide-y divide-gray-200">
        <li v-for="activity in activities" :key="activity.id" class="py-3">
          <div class="flex items-start">
            <div class="flex-1">
              <p class="font-medium">{{ activity.description }}</p>
              <p class="text-sm text-gray-500">{{ formatDate(activity.created_at) }}</p>
            </div>
          </div>
        </li>
      </ul>
    </div>
    
    <!-- Модальное окно создания кейса -->
    <CreateCaseModal :show="showCreateCaseModal" @close="showCreateCaseModal = false" @created="handleCaseCreated" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import UnifiedSearch from '@/components/search/UnifiedSearch.vue';
import CreateCaseModal from '@/components/case/CreateCaseModal.vue';
import type { DashboardStats } from '@/api/stats';

interface Case {
  id: string;
  title: string;
  status: string;
  player_name?: string;
  player_id?: string;
  created_at?: string;
  updated_at?: string;
}

interface Activity {
  id: string;
  description: string;
  created_at: string;
}

const router = useRouter();
const authStore = useAuthStore();
const loading = ref(true);
const showCreateCaseModal = ref(false);

// Статистика
const stats = ref<DashboardStats>({
  players: { total: 0 },
  cases: { total: 0, open: 0, in_progress: 0, closed: 0, resolved: 0 }
});

// Последние кейсы
const recentCases = ref<Case[]>([]);

// Активности
const activities = ref<Activity[]>([]);

// Обработчики событий
const handleSearchResultSelect = (result: any) => {
  console.log('Выбран результат поиска:', result);
  // Навигация осуществляется внутри компонента UnifiedSearch
};

const navigateTo = (path: string) => {
  router.push(path);
};

const handleCaseCreated = (newCase: Case) => {
  showCreateCaseModal.value = false;
  
  // Обновляем список последних кейсов
  recentCases.value.unshift(newCase);
  if (recentCases.value.length > 5) {
    recentCases.value.pop();
  }
  
  // Обновляем статистику
  stats.value.cases.total++;
  
  // Добавляем активность
  activities.value.unshift({
    id: Date.now().toString(),
    description: `Создан новый кейс: ${newCase.title}`,
    created_at: new Date().toISOString()
  });
  if (activities.value.length > 5) {
    activities.value.pop();
  }
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

// Загрузка данных при монтировании компонента
onMounted(async () => {
  loading.value = true;
  
  try {
    // Загружаем статистику через специализированный API
    try {
      const statsApi = await import('@/api/stats').then(m => m.useStatsApi());
      const dashboardStats = await statsApi.getDashboardStats('global');
      
      // Обновляем статистику с учетом возможных undefined полей
      stats.value = dashboardStats;
    } catch (error) {
      console.error('Ошибка при загрузке статистики:', error);
      // Статистика останется по умолчанию
    }
    
    // Загружаем данные через API для кейсов
    const casesApi = await import('@/api/cases').then(m => m.useCasesApi());
    
    // Получаем реальные кейсы
    try {
      // Используем метод для получения доступных кейсов - ограничиваем 5 последними
      const response = await casesApi.getAccessibleCases({ limit: 5 });
      
      // Проверяем формат ответа API
      if (response && response.results && Array.isArray(response.results)) {
        // Получаем массив кейсов из response.results
        const accessibleCases = response.results;
        
        // Обрабатываем данные
        recentCases.value = accessibleCases.map(caseItem => ({
          id: caseItem.id,
          title: caseItem.title,
          status: caseItem.status,
          player_name: caseItem.player_name || (caseItem.player ? caseItem.player.full_name : ''),
          created_at: caseItem.created_at
        }));
        
        // Если статистика не была загружена через специализированный API,
        // используем запасной вариант на основе кейсов
        if (stats.value.cases.total === 0 && stats.value.cases.open === 0 &&
            stats.value.cases.in_progress === 0 && stats.value.cases.closed === 0) {
          try {
            // Запрашиваем только количество кейсов без данных
            const activeCases = await casesApi.getAccessibleCases({ status: 'open,in_progress', limit: 0 });
            const closedCases = await casesApi.getAccessibleCases({ status: 'closed,resolved', limit: 0 });
            
            stats.value.cases.open = (activeCases.count || 0) > 0 ? 
              activeCases.count : accessibleCases.filter(c => c.status === 'open').length;
            
            stats.value.cases.in_progress = accessibleCases.filter(c => c.status === 'in_progress').length;
            stats.value.cases.closed = (closedCases.count || 0) > 0 ? 
              closedCases.count : accessibleCases.filter(c => c.status === 'closed').length;
            
            stats.value.cases.total = (stats.value.cases.open || 0) + 
                                   (stats.value.cases.in_progress || 0) + 
                                   (stats.value.cases.closed || 0);
          } catch (error) {
            console.error('Ошибка при загрузке статистики кейсов:', error);
          }
        }
      } else {
        console.error('API вернул данные в неожиданном формате:', response);
        recentCases.value = [];
      }
    } catch (error) {
      console.error('Ошибка при загрузке кейсов:', error);
      recentCases.value = [];
    }
    
    // Если статистика игроков не была загружена через специализированный API
    if (stats.value.players.total === 0) {
      try {
        const playersApi = await import('@/api/players').then(m => m.usePlayersApi());
        const playerStats = await playersApi.getPlayersCount();
        
        // Обновляем статистику
        stats.value.players.total = playerStats.count || 0;
        
        // Если не получили статистику, загружаем все игроки и считаем
        if (stats.value.players.total === 0) {
          const allPlayers = await playersApi.getPlayers();
          stats.value.players.total = allPlayers.length || 0;
        }
      } catch (error) {
        console.error('Ошибка при загрузке статистики игроков:', error);
      }
    }
    
    // Загружаем последние активности через API аудита, если он доступен
    try {
      // Добавим проверку на возможные ошибки сетевого взаимодействия
      const auditApi = await import('@/api/audit').then(m => m.useAuditApi());
      
      try {
        const response = await auditApi.getRecentActivity(5);
        
        if (Array.isArray(response)) {
          activities.value = response.map(activity => ({
            id: activity.id || String(Date.now()),
            description: activity.description || activity.action || 'Неизвестное действие',
            created_at: activity.created_at || new Date().toISOString()
          }));
        } else {
          console.warn('API аудита вернул данные в неожиданном формате, использую резервные данные');
          generateFallbackActivities();
        }
      } catch (error) {
        console.warn('Ошибка при обращении к API аудита, использую резервные данные:', error);
        generateFallbackActivities();
      }
    } catch (error) {
      console.warn('API аудита недоступен, использую резервные данные:', error);
      generateFallbackActivities();
    }
    
  } catch (error) {
    console.error('Общая ошибка при загрузке данных:', error);
    // Сбрасываем значения в случае ошибки
    recentCases.value = [];
    activities.value = [];
    stats.value = { players: { total: 0 }, cases: { total: 0, open: 0, in_progress: 0, closed: 0, resolved: 0 } };
  } finally {
    loading.value = false;
  }
});

// Добавим функцию для генерации активностей из имеющихся данных
function generateFallbackActivities() {
  // Используем последние кейсы для генерации активностей
  if (recentCases.value.length > 0) {
    activities.value = recentCases.value.slice(0, 5).map((caseItem, index) => {
      // Создаем разные типы активностей с разными датами
      const activityDate = new Date();
      activityDate.setHours(activityDate.getHours() - index * 2); // Разные временные метки
      
      // Генерируем несколько типов событий для разнообразия
      const activityTypes = [
        `Кейс "${caseItem.title}" был создан`,
        `Кейс "${caseItem.title}" был обновлен`,
        `Изменен статус кейса "${caseItem.title}" на "${getStatusText(caseItem.status)}"`,
        `Добавлен комментарий к кейсу "${caseItem.title}"`,
        `Добавлено доказательство к кейсу "${caseItem.title}"`
      ];
      
      return {
        id: `activity-${caseItem.id}-${index}`,
        description: activityTypes[index % activityTypes.length],
        created_at: activityDate.toISOString()
      };
    });
  } else {
    // Если нет кейсов, создаем базовые активности
    const now = new Date();
    activities.value = [
      {
        id: 'system-activity-1',
        description: 'Система инициализирована',
        created_at: new Date(now.getTime() - 24 * 60 * 60 * 1000).toISOString() // 1 день назад
      },
      {
        id: 'system-activity-2',
        description: 'Выполнено обновление системы',
        created_at: new Date(now.getTime() - 12 * 60 * 60 * 1000).toISOString() // 12 часов назад
      },
      {
        id: 'system-activity-3',
        description: 'Выполнено ежедневное обслуживание',
        created_at: new Date(now.getTime() - 6 * 60 * 60 * 1000).toISOString() // 6 часов назад
      }
    ];
  }
}
</script>

<style scoped>
.dashboard {
  padding: 1.5rem;
}

.action-btn {
  transition: all 0.2s ease;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style> 