<template>
  <div class="dashboard-container">
    <!-- Главный заголовок и описание -->
    <div class="mb-8 text-center">
      <h1 class="text-3xl font-bold text-text-light dark:text-text-dark mb-2">Система Fonds Relations</h1>
      <p class="text-text-secondary-light dark:text-text-secondary-dark max-w-2xl mx-auto">
        Единая база данных для обмена информацией о недобросовестных игроках между покерными фондами
      </p>
    </div>

    <!-- Блок поиска -->
    <div class="search-block bg-surface-light dark:bg-surface-dark rounded-xl shadow-lg p-6 mb-8 border border-border-light dark:border-border-dark">
      <h2 class="text-xl font-semibold text-text-light dark:text-text-dark mb-4">Умный поиск</h2>
      <div class="mb-4">
        <UnifiedSearch ref="searchComponent" />
      </div>
      <div class="flex flex-wrap gap-2 text-sm text-text-secondary-light dark:text-text-secondary-dark">
        <span>Популярные запросы:</span>
        <button @click="setSearchQuery('мультиаккаунт')" class="px-2 py-1 bg-background-light dark:bg-background-dark rounded-md hover:bg-primary/10 transition-colors">мультиаккаунт</button>
        <button @click="setSearchQuery('сговор')" class="px-2 py-1 bg-background-light dark:bg-background-dark rounded-md hover:bg-primary/10 transition-colors">сговор</button>
        <button @click="setSearchQuery('ПО')" class="px-2 py-1 bg-background-light dark:bg-background-dark rounded-md hover:bg-primary/10 transition-colors">запрещенное ПО</button>
      </div>
    </div>

    <!-- Блоки быстрых действий -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
      <!-- Создание нового игрока -->
      <div class="action-block bg-surface-light dark:bg-surface-dark rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow border border-border-light/40 dark:border-border-dark">
        <div class="flex items-start">
          <div class="mr-4 p-3 rounded-full bg-primary/10 text-primary dark:text-primary-dark">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-text-light dark:text-text-dark mb-2">Добавить нового игрока</h3>
            <p class="text-text-secondary-light dark:text-text-secondary-dark mb-4">
              Создайте профиль нового игрока с полной информацией о нём
            </p>
            <Button 
              variant="primary" 
              @click="navigateTo('/players/new')"
              class="w-full md:w-auto"
            >
              Создать игрока
            </Button>
          </div>
        </div>
      </div>

      <!-- Создание нового кейса -->
      <div class="action-block bg-surface-light dark:bg-surface-dark rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow border border-border-light/40 dark:border-border-dark">
        <div class="flex items-start">
          <div class="mr-4 p-3 rounded-full bg-warning/10 text-warning">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-text-light dark:text-text-dark mb-2">Создать новый кейс</h3>
            <p class="text-text-secondary-light dark:text-text-secondary-dark mb-4">
              Зафиксируйте случай нарушения и прикрепите доказательства
            </p>
            <Button 
              variant="warning" 
              @click="showNewCaseModal = true"
              class="w-full md:w-auto"
            >
              Создать кейс
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Статистика и информация -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Статистика -->
      <div class="bg-surface-light dark:bg-surface-dark rounded-xl shadow-md p-6 border border-border-light/40 dark:border-border-dark">
        <h3 class="text-lg font-semibold text-text-light dark:text-text-dark mb-4">Статистика</h3>
        <div class="grid grid-cols-2 gap-4">
          <div v-for="(stat, index) in statistics" :key="index" class="stat-item p-3 rounded-lg" :class="stat.bgColor">
            <div class="flex items-center">
              <component :is="stat.icon" class="h-6 w-6 mr-3" :class="stat.iconColor" />
              <div>
                <div class="text-lg font-bold text-text-light dark:text-text-dark">{{ stat.value }}</div>
                <div class="text-xs text-text-secondary-light dark:text-text-secondary-dark">{{ stat.label }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Недавние действия -->
      <div class="bg-surface-light dark:bg-surface-dark rounded-xl shadow-md p-6 border border-border-light/40 dark:border-border-dark">
        <h3 class="text-lg font-semibold text-text-light dark:text-text-dark mb-4">Недавние действия</h3>
        <div v-if="isLoading">
          <div v-for="i in 3" :key="i" class="mb-3">
            <Skeleton height="24px" class="mb-1" />
            <Skeleton width="60%" height="16px" />
          </div>
        </div>
        <div v-else-if="recentActions.length === 0" class="py-4 text-center text-text-secondary-light dark:text-text-secondary-dark">
          Нет недавних действий
        </div>
        <div v-else class="space-y-3">
          <div v-for="(action, index) in recentActions.slice(0, 3)" :key="index" class="p-3 rounded-lg bg-background-light dark:bg-background-dark">
            <div class="flex items-center">
              <Avatar :text="action.user" size="sm" class="mr-3" />
              <div>
                <p class="text-sm text-text-light dark:text-text-dark">
                  <span class="font-medium">{{ action.user }}</span> 
                  {{ action.action }}
                  <span class="font-medium">{{ action.target }}</span>
                </p>
                <p class="text-xs text-text-secondary-light dark:text-text-secondary-dark">
                  {{ action.time }}
                </p>
              </div>
            </div>
          </div>
        </div>
        <div class="mt-4 text-center">
          <Button variant="outline" size="sm" @click="navigateTo('/activity')">Показать все</Button>
        </div>
      </div>

      <!-- Мои кейсы -->
      <div class="bg-surface-light dark:bg-surface-dark rounded-xl shadow-md p-6 border border-border-light/40 dark:border-border-dark">
        <h3 class="text-lg font-semibold text-text-light dark:text-text-dark mb-4">Мои активные кейсы</h3>
        <div v-if="isLoading">
          <div v-for="i in 3" :key="i" class="mb-3">
            <Skeleton height="24px" class="mb-1" />
            <Skeleton width="80%" height="16px" />
          </div>
        </div>
        <div v-else-if="myCases.length === 0" class="py-4 text-center text-text-secondary-light dark:text-text-secondary-dark">
          У вас нет активных кейсов
        </div>
        <div v-else class="space-y-3">
          <div v-for="(item, index) in myCases.slice(0, 3)" :key="index" class="p-3 rounded-lg bg-background-light dark:bg-background-dark">
            <div class="flex justify-between items-start">
              <div>
                <h4 class="font-medium text-text-light dark:text-text-dark">{{ item.title }}</h4>
                <p class="text-xs text-text-secondary-light dark:text-text-secondary-dark">{{ item.description }}</p>
              </div>
              <Badge :variant="item.status === 'active' ? 'primary' : item.status === 'resolved' ? 'success' : 'warning'">
                {{ item.status === 'active' ? 'Активен' : item.status === 'resolved' ? 'Решен' : 'В ожидании' }}
              </Badge>
            </div>
          </div>
        </div>
        <div class="mt-4 text-center">
          <Button variant="outline" size="sm" @click="navigateTo('/cases')">Все кейсы</Button>
        </div>
      </div>
    </div>

    <!-- Модальное окно для создания нового кейса -->
    <Modal 
      :is-open="showNewCaseModal" 
      title="Создать новый кейс" 
      @close="showNewCaseModal = false"
    >
      <div class="space-y-4">
        <Input 
          v-model="newCase.title" 
          label="Заголовок" 
          placeholder="Введите заголовок кейса" 
          required 
        />
        
        <Input 
          v-model="newCase.description" 
          label="Описание" 
          placeholder="Введите описание кейса" 
          type="textarea" 
        />
        
        <Select 
          v-model="newCase.priority" 
          label="Приоритет" 
          :options="[
            { value: 'low', label: 'Низкий' },
            { value: 'medium', label: 'Средний' },
            { value: 'high', label: 'Высокий' }
          ]"
        />
      </div>
      
      <template #footer>
        <Button variant="outline" @click="showNewCaseModal = false">Отмена</Button>
        <Button variant="primary" @click="createNewCase">Создать</Button>
      </template>
    </Modal>

    <!-- Футер с версией -->
    <div class="mt-8 pt-4 border-t border-border-light dark:border-border-dark text-right">
      <VersionInfo :version="appVersion" :backend-version="backendVersion" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

import Card from '@/components/ui/Card.vue';
import Button from '@/components/ui/Button.vue';
import Badge from '@/components/ui/Badge.vue';
import Avatar from '@/components/ui/Avatar.vue';
import Modal from '@/components/ui/Modal.vue';
import Input from '@/components/ui/Input.vue';
import Select from '@/components/ui/Select.vue';
import Skeleton from '@/components/ui/Skeleton.vue';

import UnifiedSearch from '@/components/search/UnifiedSearch.vue';
import VersionInfo from '@/components/VersionInfo.vue';

const router = useRouter();

// Версии приложения
const appVersion = '0.3.1';
const backendVersion = '0.3.13';

// Иконки для статистики
const IconUsers = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
  </svg>`
};

const IconCases = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
  </svg>`
};

const IconComments = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
  </svg>`
};

const IconResolved = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>`
};

// Состояние загрузки
const isLoading = ref(true);

// Статистика
const statistics = ref([
  { label: 'Всего игроков', value: '1,254', icon: IconUsers, bgColor: 'bg-primary/10', iconColor: 'text-primary dark:text-primary-dark' },
  { label: 'Активные кейсы', value: '42', icon: IconCases, bgColor: 'bg-warning/10', iconColor: 'text-warning' },
  { label: 'Комментарии', value: '891', icon: IconComments, bgColor: 'bg-secondary/10', iconColor: 'text-secondary dark:text-secondary' },
  { label: 'Решенные кейсы', value: '156', icon: IconResolved, bgColor: 'bg-success/10', iconColor: 'text-success' }
]);

// Недавние действия
const recentActions = ref([
  { user: 'Иван Петров', action: 'добавил комментарий к кейсу', target: 'Подозрение на мультиаккаунт', time: '2 часа назад' },
  { user: 'Анна Смирнова', action: 'создала новый кейс', target: 'Подозрение на сговор', time: '4 часа назад' },
  { user: 'Дмитрий Иванов', action: 'обновил статус кейса', target: 'Подозрение на использование ПО', time: '6 часов назад' },
  { user: 'Елена Козлова', action: 'добавила доказательство к кейсу', target: 'Подозрение на мультиаккаунт', time: '1 день назад' },
  { user: 'Сергей Сидоров', action: 'закрыл кейс', target: 'Подозрение на сговор', time: '2 дня назад' }
]);

// Мои кейсы
const myCases = ref([
  { 
    title: 'Подозрение на мультиаккаунт', 
    description: 'Игрок использует несколько аккаунтов на одном устройстве', 
    status: 'active' 
  },
  { 
    title: 'Подозрение на сговор', 
    description: 'Группа игроков координирует свои действия для получения преимущества', 
    status: 'pending' 
  },
  { 
    title: 'Использование запрещенного ПО', 
    description: 'Игрок использует программное обеспечение для анализа игры', 
    status: 'resolved' 
  }
]);

// Модальное окно для создания нового кейса
const showNewCaseModal = ref(false);
const newCase = ref({
  title: '',
  description: '',
  priority: 'medium'
});

// Функция для установки поискового запроса
const searchComponent = ref<InstanceType<typeof UnifiedSearch> | null>(null);

const setSearchQuery = (query: string) => {
  if (searchComponent.value) {
    // Устанавливаем значение в компоненте поиска
    searchComponent.value.searchQuery = query;
    // Вызываем поиск
    searchComponent.value.debouncedSearch();
  }
};

// Навигация
const navigateTo = (path: string) => {
  router.push(path);
};

// Создание нового кейса
const createNewCase = () => {
  // Здесь будет логика создания нового кейса
  console.log('Создание нового кейса:', newCase.value);
  
  // Добавляем новый кейс в список
  myCases.value.unshift({
    title: newCase.value.title,
    description: newCase.value.description,
    status: 'active'
  });
  
  // Сбрасываем форму и закрываем модальное окно
  newCase.value = {
    title: '',
    description: '',
    priority: 'medium'
  };
  
  showNewCaseModal.value = false;
};

// Имитация загрузки данных
onMounted(() => {
  setTimeout(() => {
    isLoading.value = false;
  }, 1500);
});
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background-color: var(--color-background-light);
  position: relative;
}

.action-block {
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: all 0.2s ease-in-out;
}

.action-block:hover {
  transform: translateY(-2px);
}

.version-info-wrapper {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  z-index: 50;
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 1rem;
  }
  
  .version-info-wrapper {
    bottom: 0.5rem;
    right: 0.5rem;
  }
}
</style> 