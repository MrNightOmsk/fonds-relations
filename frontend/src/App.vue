<template>
  <div class="min-h-screen flex flex-col">
    <header v-if="isAuthenticated" class="bg-white dark:bg-background-dark border-b border-border-light dark:border-border-dark shadow-sm">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center">
        <div class="flex items-center">
          <router-link to="/" class="text-2xl font-bold text-primary dark:text-primary-dark hover:opacity-90 transition-opacity">
            Fonds Relations
          </router-link>
        </div>
        
        <!-- Навигационное меню -->
        <nav class="hidden md:flex items-center space-x-6">
          <router-link 
            v-for="link in navLinks" 
            :key="link.to" 
            :to="link.to"
            class="text-text-light dark:text-text-dark hover:text-primary dark:hover:text-primary-dark px-3 py-2 transition-colors duration-200"
            :class="{ 'border-b-2 border-primary dark:border-primary-dark': isActiveRoute(link.to) }"
          >
            {{ link.text }}
          </router-link>
        </nav>
        
        <div class="flex items-center space-x-4">
          <button 
            @click="toggleDarkMode" 
            class="p-2 rounded-full hover:bg-surface-light dark:hover:bg-surface-dark transition-colors"
            aria-label="Переключить тему"
          >
            <span v-if="isDarkMode" class="text-text-dark">🌞</span>
            <span v-else class="text-text-light">🌙</span>
          </button>
          <!-- Переключатель вариантов светлой темы -->
          <ThemeSwitcher v-if="!isDarkMode" />
          <span class="hidden md:inline text-sm text-text-light dark:text-text-dark">{{ userName }}</span>
          <button 
            @click="logout"
            class="text-white bg-primary dark:bg-primary-dark hover:bg-primary-600 dark:hover:bg-primary-400 px-4 py-2 rounded-md transition-colors duration-200"
          >
            Выйти
          </button>
          
          <!-- Мобильное меню (гамбургер) -->
          <button 
            @click="toggleMobileMenu" 
            class="md:hidden p-2 rounded-md hover:bg-surface-light dark:hover:bg-surface-dark transition-colors"
            aria-label="Меню"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-text-light dark:text-text-dark" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7" />
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Мобильное меню (раскрывающееся) -->
      <div 
        v-if="isMobileMenuOpen" 
        class="md:hidden bg-white dark:bg-surface-dark shadow-lg"
      >
        <div class="container mx-auto px-4 py-2">
          <router-link 
            v-for="link in navLinks" 
            :key="link.to" 
            :to="link.to"
            class="block py-3 text-text-light dark:text-text-dark hover:text-primary dark:hover:text-primary-dark border-b border-gray-100 dark:border-gray-700 last:border-0"
            @click="isMobileMenuOpen = false"
          >
            {{ link.text }}
          </router-link>
        </div>
      </div>
    </header>
    
    <main class="flex-grow bg-background-light dark:bg-background-dark text-text-light dark:text-text-dark">
      <div class="container mx-auto p-4">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
    
    <footer class="bg-surface-light dark:bg-surface-dark text-text-secondary-light dark:text-text-secondary-dark py-6 border-t border-border-light dark:border-border-dark">
      <div class="container mx-auto px-4 text-center">
        <p>&copy; {{ new Date().getFullYear() }} Fonds Relations. Все права защищены.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import ThemeSwitcher from '@/components/ThemeSwitcher.vue';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const isAuthenticated = computed(() => authStore.isAuthenticated);
const isAdmin = computed(() => authStore.isAdmin);
const userName = computed(() => authStore.user?.full_name || authStore.user?.email || '');

// Навигационные ссылки
const navLinks = computed(() => {
  const links = [
    { to: '/dashboard', text: 'Главная' },
    { to: '/cases', text: 'Кейсы' },
    { to: '/players', text: 'Игроки' },
  ];
  
  if (isAdmin.value) {
    links.push({ to: '/admin', text: 'Администрирование' });
  }
  
  // Добавляем ссылку на демо-тему (только для разработки)
  if (import.meta.env.DEV) {
    links.push({ to: '/theme-demo', text: 'Темы' });
  }
  
  return links;
});

// Мобильное меню
const isMobileMenuOpen = ref(false);
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

// Определение активного маршрута
const isActiveRoute = (path: string) => {
  return route.path === path || route.path.startsWith(`${path}/`);
};

// Темная тема
const isDarkMode = ref(false);

// Применить тему к HTML элементу
const applyTheme = (dark: boolean) => {
  if (dark) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
};

onMounted(() => {
  // Загрузка предпочтений темы из localStorage
  const savedTheme = localStorage.getItem('theme');
  
  console.log('Saved theme:', savedTheme);
  
  if (savedTheme === 'dark') {
    isDarkMode.value = true;
  } else if (savedTheme === 'light') {
    isDarkMode.value = false;
  } else {
    // Если предпочтений нет, используем системные настройки
    isDarkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  
  // Применяем тему
  applyTheme(isDarkMode.value);
});

// Следим за изменением темы
watch(isDarkMode, (newValue) => {
  applyTheme(newValue);
  localStorage.setItem('theme', newValue ? 'dark' : 'light');
  console.log('Theme changed to:', newValue ? 'dark' : 'light');
});

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value;
  console.log('Toggling theme to:', isDarkMode.value ? 'dark' : 'light');
};

const logout = () => {
  authStore.logout();
  router.push('/login');
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  font-family: 'Inter', sans-serif;
  
  /* Базовые цвета для светлой темы */
  --color-background-light: #f4f5f7;
  --color-surface-light: #ffffff;
  --color-border-light: #e2e8f0;
  --color-text-light: #1e293b;
  --color-text-secondary-light: #4b5563;
}

/* Темная тема */
.dark {
  color-scheme: dark;
}

/* Анимация перехода между страницами */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 