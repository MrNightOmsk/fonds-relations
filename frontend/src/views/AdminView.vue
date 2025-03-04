<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-bold mb-6">Панель администратора</h1>
    
    <!-- Панель навигации -->
    <div class="flex mb-6 border-b">
      <button @click="activeTab = 'users'" 
        :class="['px-4 py-2 mr-2', activeTab === 'users' ? 'border-b-2 border-primary text-primary font-semibold' : 'text-gray-600']">
        Пользователи
      </button>
      <button @click="activeTab = 'funds'" 
        :class="['px-4 py-2 mr-2', activeTab === 'funds' ? 'border-b-2 border-primary text-primary font-semibold' : 'text-gray-600']">
        Фонды
      </button>
      <button @click="navigateTo('/admin/players')" 
        :class="['px-4 py-2 mr-2', $route.path.includes('/admin/players') ? 'border-b-2 border-primary text-primary font-semibold' : 'text-gray-600']">
        Игроки
      </button>
      <button @click="navigateTo('/admin/cases')" 
        :class="['px-4 py-2 mr-2', $route.path.includes('/admin/cases') ? 'border-b-2 border-primary text-primary font-semibold' : 'text-gray-600']">
        Кейсы
      </button>
    </div>

    <!-- Содержимое вкладки -->
    <div v-if="$route.path === '/admin'">
      <div v-if="activeTab === 'users'">
        <UsersManagement />
      </div>
      <div v-else-if="activeTab === 'funds'">
        <FundsManagement />
      </div>
    </div>
    
    <!-- Отображение дочерних маршрутов -->
    <router-view v-else></router-view>
  </div>
</template>

<script setup lang="ts">
// @ts-ignore
import { ref, onMounted, watch } from 'vue';
// @ts-ignore
import { useRoute, useRouter } from 'vue-router';
import UsersManagement from '@/components/admin/UsersManagement.vue';
import FundsManagement from '@/components/admin/FundsManagement.vue';

const route = useRoute();
const router = useRouter();
const activeTab = ref('users');

// Функция для перехода по маршруту
const navigateTo = (path: string) => {
  console.log('Переход по маршруту:', path);
  router.push(path);
};

// Установка активной вкладки в зависимости от маршрута
onMounted(() => {
  console.log('Текущий маршрут при монтировании:', route.path);
  updateActiveTab();
});

// Обновление активной вкладки при изменении маршрута
watch(() => route.path, (newPath) => {
  console.log('Маршрут изменился на:', newPath);
  updateActiveTab();
});

// Функция для обновления активной вкладки
const updateActiveTab = () => {
  const path = route.path;
  if (path === '/admin') {
    activeTab.value = 'users';
  } else if (path.includes('/admin/players')) {
    activeTab.value = 'players';
  } else if (path.includes('/admin/cases')) {
    activeTab.value = 'cases';
  }
  console.log('Активная вкладка установлена:', activeTab.value);
};
</script> 