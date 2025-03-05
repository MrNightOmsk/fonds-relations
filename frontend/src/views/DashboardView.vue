<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Панель управления</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Карточка с информацией о пользователе -->
      <div class="card">
        <h2 class="text-xl font-semibold mb-4">Информация о пользователе</h2>
        <div v-if="authStore.user">
          <p><span class="font-medium">Имя:</span> {{ authStore.user.full_name }}</p>
          <p><span class="font-medium">Email:</span> {{ authStore.user.email }}</p>
          <p><span class="font-medium">Роль:</span> {{ authStore.user.role }}</p>
        </div>
        <div v-else class="text-gray-500">
          Загрузка информации...
        </div>
      </div>
      
      <!-- Карточка с быстрыми действиями -->
      <div class="card">
        <h2 class="text-xl font-semibold mb-4">Быстрые действия</h2>
        <div class="space-y-2">
          <router-link to="/admin/players" class="btn-primary block text-center">
            Управление игроками
          </router-link>
          <router-link to="/admin/cases" class="btn-secondary block text-center">
            Управление кейсами
          </router-link>
        </div>
      </div>
      
      <!-- Карточка со статистикой -->
      <div class="card">
        <h2 class="text-xl font-semibold mb-4">Статистика</h2>
        <div v-if="loading" class="text-gray-500">
          Загрузка статистики...
        </div>
        <div v-else class="space-y-2">
          <p><span class="font-medium">Всего игроков:</span> {{ stats.totalPlayers }}</p>
          <p><span class="font-medium">Активных кейсов:</span> {{ stats.activeCases }}</p>
          <p><span class="font-medium">Закрытых кейсов:</span> {{ stats.closedCases }}</p>
        </div>
      </div>
    </div>
    
    <!-- Последние активности -->
    <div class="card mt-6">
      <h2 class="text-xl font-semibold mb-4">Последние активности</h2>
      <div v-if="loading" class="text-gray-500">
        Загрузка активностей...
      </div>
      <div v-else-if="activities.length === 0" class="text-gray-500">
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const loading = ref(true);

// Заглушка для статистики
const stats = ref({
  totalPlayers: 0,
  activeCases: 0,
  closedCases: 0
});

// Заглушка для активностей
const activities = ref([]);

// Форматирование даты
const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date);
};

// Загрузка данных при монтировании компонента
onMounted(async () => {
  try {
    // Здесь будут запросы к API для получения статистики и активностей
    // Временно используем моковые данные
    setTimeout(() => {
      stats.value = {
        totalPlayers: 24,
        activeCases: 8,
        closedCases: 16
      };
      
      activities.value = [
        { id: 1, description: 'Создан новый кейс для игрока Иванов И.И.', created_at: '2023-03-01T10:30:00Z' },
        { id: 2, description: 'Закрыт кейс #12345', created_at: '2023-02-28T15:45:00Z' },
        { id: 3, description: 'Добавлен новый игрок Петров П.П.', created_at: '2023-02-27T09:15:00Z' }
      ];
      
      loading.value = false;
    }, 1000);
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
    loading.value = false;
  }
});
</script> 