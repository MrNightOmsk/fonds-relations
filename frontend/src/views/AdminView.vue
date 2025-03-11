<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-bold mb-6 text-text-light dark:text-text-dark">Панель администратора</h1>
    
    <!-- Панель навигации -->
    <div class="flex mb-6 border-b border-border-light dark:border-border-dark">
      <button @click="navigateToTab('users')" 
        :class="['px-4 py-2 mr-2', activeTab === 'users' ? 'border-b-2 border-primary dark:border-primary-dark text-primary dark:text-primary-dark font-semibold' : 'text-text-secondary-light dark:text-text-secondary-dark']">
        Пользователи
      </button>
      <button @click="navigateToTab('funds')" 
        :class="['px-4 py-2 mr-2', activeTab === 'funds' ? 'border-b-2 border-primary dark:border-primary-dark text-primary dark:text-primary-dark font-semibold' : 'text-text-secondary-light dark:text-text-secondary-dark']">
        Фонды
      </button>
      <button @click="navigateToTab('players')" 
        :class="['px-4 py-2 mr-2', activeTab === 'players' ? 'border-b-2 border-primary dark:border-primary-dark text-primary dark:text-primary-dark font-semibold' : 'text-text-secondary-light dark:text-text-secondary-dark']">
        Игроки
      </button>
      <button @click="navigateToTab('cases')" 
        :class="['px-4 py-2 mr-2', activeTab === 'cases' ? 'border-b-2 border-primary dark:border-primary-dark text-primary dark:text-primary-dark font-semibold' : 'text-text-secondary-light dark:text-text-secondary-dark']">
        Кейсы
      </button>
      <button @click="navigateToTab('poker-rooms')" 
        :class="['px-4 py-2 mr-2', activeTab === 'poker-rooms' ? 'border-b-2 border-primary dark:border-primary-dark text-primary dark:text-primary-dark font-semibold' : 'text-text-secondary-light dark:text-text-secondary-dark']">
        Покерные румы
      </button>
      <button @click="navigateToTab('search-index')" 
        :class="['px-4 py-2 mr-2', activeTab === 'search-index' ? 'border-b-2 border-primary dark:border-primary-dark text-primary dark:text-primary-dark font-semibold' : 'text-text-secondary-light dark:text-text-secondary-dark']">
        Поисковый индекс
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

// Функция для перехода по вкладкам
const navigateToTab = (tab: string) => {
  console.log('Переход на вкладку:', tab);
  activeTab.value = tab;
  
  if (tab === 'users' || tab === 'funds') {
    // Для локальных вкладок переходим на базовый маршрут админки
    router.push('/admin');
  } else if (tab === 'players') {
    router.push('/admin/players');
  } else if (tab === 'cases') {
    router.push('/admin/cases');
  } else if (tab === 'poker-rooms') {
    router.push('/admin/poker-rooms');
  } else if (tab === 'search-index') {
    router.push('/admin/search-index');
  }
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
    // Сохраняем активную вкладку для users и funds
    if (activeTab.value !== 'users' && activeTab.value !== 'funds') {
      activeTab.value = 'users';
    }
  } else if (path.includes('/admin/players')) {
    activeTab.value = 'players';
  } else if (path.includes('/admin/cases')) {
    activeTab.value = 'cases';
  } else if (path.includes('/admin/poker-rooms')) {
    activeTab.value = 'poker-rooms';
  } else if (path.includes('/admin/search-index')) {
    activeTab.value = 'search-index';
  }
  console.log('Активная вкладка установлена:', activeTab.value);
};
</script> 