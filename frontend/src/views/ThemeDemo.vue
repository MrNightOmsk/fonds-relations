<template>
  <div class="max-w-6xl mx-auto p-6">
    <h1 class="text-3xl font-bold text-text-light dark:text-text-dark mb-6">Демонстрация вариантов светлой темы</h1>
    
    <div class="grid grid-cols-1 xl:grid-cols-3 gap-8 mb-12">
      <!-- Вариант 1: Мягкий нейтральный серый -->
      <div class="theme-variant">
        <h2 class="text-xl font-semibold mb-3">Вариант 1: Мягкий нейтральный</h2>
        <p class="text-sm text-text-secondary-light mb-4">Мягкий серый фон с белыми карточками и аккуратными тенями</p>
        
        <div class="bg-[#f4f5f7] p-4 rounded-lg border border-[#e2e8f0] shadow-sm">
          <h3 class="text-[#1e293b] font-medium mb-2">Основной контент</h3>
          
          <!-- Карточка -->
          <div class="bg-white rounded-xl p-4 shadow-md border border-[#e2e8f0]/40 mb-4">
            <h4 class="text-[#1e293b] font-medium mb-2">Карточка</h4>
            <p class="text-[#4b5563] text-sm mb-3">Пример текста в карточке на светлом фоне.</p>
            <div class="flex space-x-2">
              <button class="px-3 py-1 bg-[#0891b2] text-white rounded-md text-sm">Кнопка</button>
              <button class="px-3 py-1 bg-[#f4f5f7] text-[#1e293b] border border-[#e2e8f0] rounded-md text-sm">Еще</button>
            </div>
          </div>
          
          <!-- Панель с тегами -->
          <div class="flex flex-wrap gap-2 mb-4">
            <span class="text-sm">Теги:</span>
            <span class="px-2 py-1 bg-[#f4f5f7] text-[#4b5563] rounded-md text-sm border border-[#e2e8f0]">Нейтральный</span>
            <span class="px-2 py-1 bg-[#f4f5f7] text-[#4b5563] rounded-md text-sm border border-[#e2e8f0]">Спокойный</span>
          </div>
        </div>
      </div>
      
      <!-- Вариант 2: Теплый оффвайт -->
      <div class="theme-variant">
        <h2 class="text-xl font-semibold mb-3">Вариант 2: Теплый офф-вайт</h2>
        <p class="text-sm text-text-secondary-light mb-4">Кремовый фон с теплыми акцентами и мягкими тенями</p>
        
        <div class="bg-[#f8f7f4] p-4 rounded-lg border border-[#e6e2d9] shadow-sm">
          <h3 class="text-[#2d3748] font-medium mb-2">Основной контент</h3>
          
          <!-- Карточка -->
          <div class="bg-white rounded-xl p-4 shadow-md border border-[#e6e2d9]/40 mb-4">
            <h4 class="text-[#2d3748] font-medium mb-2">Карточка</h4>
            <p class="text-[#718096] text-sm mb-3">Пример текста в карточке на светлом фоне.</p>
            <div class="flex space-x-2">
              <button class="px-3 py-1 bg-[#0891b2] text-white rounded-md text-sm">Кнопка</button>
              <button class="px-3 py-1 bg-[#f8f7f4] text-[#2d3748] border border-[#e6e2d9] rounded-md text-sm">Еще</button>
            </div>
          </div>
          
          <!-- Панель с тегами -->
          <div class="flex flex-wrap gap-2 mb-4">
            <span class="text-sm">Теги:</span>
            <span class="px-2 py-1 bg-[#f8f7f4] text-[#718096] rounded-md text-sm border border-[#e6e2d9]">Теплый</span>
            <span class="px-2 py-1 bg-[#f8f7f4] text-[#718096] rounded-md text-sm border border-[#e6e2d9]">Уютный</span>
          </div>
        </div>
      </div>
      
      <!-- Вариант 3: Современный холодный -->
      <div class="theme-variant">
        <h2 class="text-xl font-semibold mb-3">Вариант 3: Современный холодный</h2>
        <p class="text-sm text-text-secondary-light mb-4">Голубовато-серый фон с чистыми линиями и четкими границами</p>
        
        <div class="bg-[#eef2f6] p-4 rounded-lg border border-[#dbe4ee] shadow-sm">
          <h3 class="text-[#1a202c] font-medium mb-2">Основной контент</h3>
          
          <!-- Карточка -->
          <div class="bg-white rounded-xl p-4 shadow-md border border-[#dbe4ee]/40 mb-4">
            <h4 class="text-[#1a202c] font-medium mb-2">Карточка</h4>
            <p class="text-[#4a5568] text-sm mb-3">Пример текста в карточке на светлом фоне.</p>
            <div class="flex space-x-2">
              <button class="px-3 py-1 bg-[#0891b2] text-white rounded-md text-sm">Кнопка</button>
              <button class="px-3 py-1 bg-[#eef2f6] text-[#1a202c] border border-[#dbe4ee] rounded-md text-sm">Еще</button>
            </div>
          </div>
          
          <!-- Панель с тегами -->
          <div class="flex flex-wrap gap-2 mb-4">
            <span class="text-sm">Теги:</span>
            <span class="px-2 py-1 bg-[#eef2f6] text-[#4a5568] rounded-md text-sm border border-[#dbe4ee]">Современный</span>
            <span class="px-2 py-1 bg-[#eef2f6] text-[#4a5568] rounded-md text-sm border border-[#dbe4ee]">Четкий</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Панели управления полного размера -->
    <h2 class="text-2xl font-bold text-text-light dark:text-text-dark mb-6">Примеры компонентов</h2>
    
    <div class="grid grid-cols-1 xl:grid-cols-3 gap-8 mb-12">
      <!-- Вариант 1: Мягкий нейтральный серый -->
      <div>
        <h3 class="text-lg font-semibold mb-3">Вариант 1: Панель поиска</h3>
        <div class="bg-[#f4f5f7] p-4 rounded-lg">
          <div class="bg-white rounded-xl p-4 shadow-md border border-[#e2e8f0]/40">
            <h4 class="text-[#1e293b] font-medium mb-3">Поиск</h4>
            <div class="relative mb-3">
              <input 
                type="text" 
                class="w-full px-3 py-2 border border-[#e2e8f0] rounded-md focus:outline-none focus:ring-2 focus:ring-[#0891b2]/30 text-[#1e293b]" 
                placeholder="Введите запрос..."
              />
              <button class="absolute right-2 top-2 text-[#4b5563]">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
            </div>
            <div class="flex flex-wrap gap-2">
              <button class="px-2 py-1 bg-[#f4f5f7] text-[#4b5563] rounded-md text-sm">мультиаккаунт</button>
              <button class="px-2 py-1 bg-[#f4f5f7] text-[#4b5563] rounded-md text-sm">сговор</button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Вариант 2: Теплый офф-вайт -->
      <div>
        <h3 class="text-lg font-semibold mb-3">Вариант 2: Панель поиска</h3>
        <div class="bg-[#f8f7f4] p-4 rounded-lg">
          <div class="bg-white rounded-xl p-4 shadow-md border border-[#e6e2d9]/40">
            <h4 class="text-[#2d3748] font-medium mb-3">Поиск</h4>
            <div class="relative mb-3">
              <input 
                type="text" 
                class="w-full px-3 py-2 border border-[#e6e2d9] rounded-md focus:outline-none focus:ring-2 focus:ring-[#0891b2]/30 text-[#2d3748]" 
                placeholder="Введите запрос..."
              />
              <button class="absolute right-2 top-2 text-[#718096]">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
            </div>
            <div class="flex flex-wrap gap-2">
              <button class="px-2 py-1 bg-[#f8f7f4] text-[#718096] rounded-md text-sm">мультиаккаунт</button>
              <button class="px-2 py-1 bg-[#f8f7f4] text-[#718096] rounded-md text-sm">сговор</button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Вариант 3: Современный холодный -->
      <div>
        <h3 class="text-lg font-semibold mb-3">Вариант 3: Панель поиска</h3>
        <div class="bg-[#eef2f6] p-4 rounded-lg">
          <div class="bg-white rounded-xl p-4 shadow-md border border-[#dbe4ee]/40">
            <h4 class="text-[#1a202c] font-medium mb-3">Поиск</h4>
            <div class="relative mb-3">
              <input 
                type="text" 
                class="w-full px-3 py-2 border border-[#dbe4ee] rounded-md focus:outline-none focus:ring-2 focus:ring-[#0891b2]/30 text-[#1a202c]" 
                placeholder="Введите запрос..."
              />
              <button class="absolute right-2 top-2 text-[#4a5568]">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
            </div>
            <div class="flex flex-wrap gap-2">
              <button class="px-2 py-1 bg-[#eef2f6] text-[#4a5568] rounded-md text-sm">мультиаккаунт</button>
              <button class="px-2 py-1 bg-[#eef2f6] text-[#4a5568] rounded-md text-sm">сговор</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Таблица сравнения -->
    <div class="overflow-x-auto mb-12">
      <table class="min-w-full border-collapse border border-border-light">
        <thead>
          <tr class="bg-background-light">
            <th class="border border-border-light p-3 text-left">Критерий</th>
            <th class="border border-border-light p-3 text-left">Вариант 1: Мягкий нейтральный</th>
            <th class="border border-border-light p-3 text-left">Вариант 2: Теплый офф-вайт</th>
            <th class="border border-border-light p-3 text-left">Вариант 3: Современный холодный</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="border border-border-light p-3 font-medium">Фон</td>
            <td class="border border-border-light p-3 bg-[#f4f5f7]">#f4f5f7</td>
            <td class="border border-border-light p-3 bg-[#f8f7f4]">#f8f7f4</td>
            <td class="border border-border-light p-3 bg-[#eef2f6]">#eef2f6</td>
          </tr>
          <tr>
            <td class="border border-border-light p-3 font-medium">Границы</td>
            <td class="border border-[#e2e8f0] p-3">#e2e8f0</td>
            <td class="border border-[#e6e2d9] p-3">#e6e2d9</td>
            <td class="border border-[#dbe4ee] p-3">#dbe4ee</td>
          </tr>
          <tr>
            <td class="border border-border-light p-3 font-medium">Основной текст</td>
            <td class="border border-border-light p-3 text-[#1e293b]">#1e293b</td>
            <td class="border border-border-light p-3 text-[#2d3748]">#2d3748</td>
            <td class="border border-border-light p-3 text-[#1a202c]">#1a202c</td>
          </tr>
          <tr>
            <td class="border border-border-light p-3 font-medium">Вторичный текст</td>
            <td class="border border-border-light p-3 text-[#4b5563]">#4b5563</td>
            <td class="border border-border-light p-3 text-[#718096]">#718096</td>
            <td class="border border-border-light p-3 text-[#4a5568]">#4a5568</td>
          </tr>
          <tr>
            <td class="border border-border-light p-3 font-medium">Настроение</td>
            <td class="border border-border-light p-3">Нейтральное, профессиональное</td>
            <td class="border border-border-light p-3">Теплое, уютное</td>
            <td class="border border-border-light p-3">Чистое, современное</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="flex justify-end space-x-4">
      <button 
        @click="switchToTheme('neutralGray')" 
        class="px-4 py-2 bg-[#f4f5f7] text-[#1e293b] border border-[#e2e8f0] rounded-md"
      >
        Вариант 1
      </button>
      <button 
        @click="switchToTheme('warmOffWhite')" 
        class="px-4 py-2 bg-[#f8f7f4] text-[#2d3748] border border-[#e6e2d9] rounded-md"
      >
        Вариант 2
      </button>
      <button 
        @click="switchToTheme('modernCool')" 
        class="px-4 py-2 bg-[#eef2f6] text-[#1a202c] border border-[#dbe4ee] rounded-md"
      >
        Вариант 3
      </button>
      <button 
        @click="applyTheme"
        class="px-4 py-2 bg-primary text-white rounded-md"
      >
        Применить выбранную тему
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

// Определяем типы для тем
type Theme = 'neutralGray' | 'warmOffWhite' | 'modernCool';

// Текущая тема для демонстрации
const currentTheme = ref<Theme>('neutralGray');

// Определение CSS переменных для каждой темы
const themes = {
  neutralGray: {
    '--color-background-light': '#f4f5f7',
    '--color-surface-light': '#ffffff',
    '--color-border-light': '#e2e8f0',
    '--color-text-light': '#1e293b',
    '--color-text-secondary-light': '#4b5563'
  },
  warmOffWhite: {
    '--color-background-light': '#f8f7f4',
    '--color-surface-light': '#ffffff',
    '--color-border-light': '#e6e2d9',
    '--color-text-light': '#2d3748',
    '--color-text-secondary-light': '#718096'
  },
  modernCool: {
    '--color-background-light': '#eef2f6',
    '--color-surface-light': '#ffffff',
    '--color-border-light': '#dbe4ee',
    '--color-text-light': '#1a202c',
    '--color-text-secondary-light': '#4a5568'
  }
};

// Функция для предварительного просмотра темы (только для демо)
const switchToTheme = (theme: Theme) => {
  currentTheme.value = theme;
};

// Функция для применения и сохранения выбранной темы
const applyTheme = () => {
  // Применяем CSS переменные
  Object.entries(themes[currentTheme.value]).forEach(([property, value]) => {
    document.documentElement.style.setProperty(property, value);
  });
  
  // Сохраняем выбор в localStorage
  localStorage.setItem('selectedLightTheme', currentTheme.value);
  
  // Показываем уведомление
  alert(`Тема "${currentTheme.value}" успешно применена!`);
};

// При монтировании компонента загружаем сохраненную тему
onMounted(() => {
  const savedTheme = localStorage.getItem('selectedLightTheme') as Theme;
  if (savedTheme && Object.keys(themes).includes(savedTheme)) {
    currentTheme.value = savedTheme;
  }
});
</script>

<style scoped>
.theme-variant {
  transition: transform 0.2s ease;
}

.theme-variant:hover {
  transform: translateY(-2px);
}
</style> 