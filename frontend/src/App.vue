<template>
  <div class="app-container">
    <header v-if="isAuthenticated" class="bg-primary text-white p-4 shadow-md">
      <div class="container mx-auto flex justify-between items-center">
        <div class="flex items-center">
          <router-link to="/" class="text-2xl font-bold m-0 hover:text-gray-200">Fonds Relations</router-link>
        </div>
        
        <!-- Навигационное меню -->
        <nav class="hidden md:flex items-center space-x-6">
          <router-link to="/dashboard" class="text-white hover:text-gray-200 px-3 py-2">
            Главная
          </router-link>
          <router-link to="/admin" v-if="isAdmin" class="text-white hover:text-gray-200 px-3 py-2">
            Администрирование
          </router-link>
        </nav>
        
        <div class="flex items-center space-x-4">
          <span class="hidden md:inline text-sm">{{ userName }}</span>
          <button @click="logout" class="text-white hover:text-gray-200 px-3 py-2 rounded hover:bg-primary-dark">
            Выйти
          </button>
        </div>
      </div>
    </header>
    
    <main class="container mx-auto p-4 flex-grow">
      <router-view></router-view>
    </main>
    
    <footer class="bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 p-4 mt-8">
      <div class="container mx-auto text-center">
        <p>&copy; {{ new Date().getFullYear() }} Fonds Relations. Все права защищены.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const isAuthenticated = computed(() => authStore.isAuthenticated);
const isAdmin = computed(() => authStore.isAdmin);
const userName = computed(() => authStore.user?.full_name || authStore.user?.email || '');

const logout = () => {
  authStore.logout();
  router.push('/login');
};
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
}
</style> 