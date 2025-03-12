<template>
  <div class="flex items-center space-x-2">
    <button 
      @click="switchToTheme('neutralGray')" 
      class="theme-button" 
      :class="{ 'active': currentTheme === 'neutralGray' }"
      title="Мягкий нейтральный серый"
    >
      <div class="flex flex-col items-center">
        <div class="w-6 h-6 rounded-full bg-[#f4f5f7] border border-[#e2e8f0] mb-1"></div>
        <span class="text-xs">Нейтральный</span>
      </div>
    </button>
    
    <button 
      @click="switchToTheme('warmOffWhite')" 
      class="theme-button" 
      :class="{ 'active': currentTheme === 'warmOffWhite' }"
      title="Теплый офф-вайт"
    >
      <div class="flex flex-col items-center">
        <div class="w-6 h-6 rounded-full bg-[#f8f7f4] border border-[#e6e2d9] mb-1"></div>
        <span class="text-xs">Теплый</span>
      </div>
    </button>
    
    <button 
      @click="switchToTheme('modernCool')" 
      class="theme-button" 
      :class="{ 'active': currentTheme === 'modernCool' }"
      title="Современный холодный"
    >
      <div class="flex flex-col items-center">
        <div class="w-6 h-6 rounded-full bg-[#eef2f6] border border-[#dbe4ee] mb-1"></div>
        <span class="text-xs">Холодный</span>
      </div>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

// Определяем типы для тем
type Theme = 'neutralGray' | 'warmOffWhite' | 'modernCool';

// Текущая тема
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

// Функция для переключения темы
const switchToTheme = (theme: Theme) => {
  currentTheme.value = theme;
  
  // Применяем CSS переменные к документу
  applyThemeVariables(theme);
  
  // Создаем CSS-стили прямо в документе для переопределения tailwind классов
  injectGlobalStyles(theme);
  
  // Сохраняем выбор в localStorage
  localStorage.setItem('selectedLightTheme', theme);
};

// Применяем переменные CSS
function applyThemeVariables(theme: Theme) {
  Object.entries(themes[theme]).forEach(([property, value]) => {
    document.documentElement.style.setProperty(property, value);
  });
}

// Создаем глобальные стили для переопределения tailwind-классов
function injectGlobalStyles(theme: Theme) {
  // Найдем или создадим элемент style для наших глобальных стилей
  let styleElement = document.getElementById('theme-styles');
  if (!styleElement) {
    styleElement = document.createElement('style');
    styleElement.id = 'theme-styles';
    document.head.appendChild(styleElement);
  }
  
  // Получаем цвета из темы
  const bgColor = themes[theme]['--color-background-light'];
  const surfaceColor = themes[theme]['--color-surface-light'];
  const borderColor = themes[theme]['--color-border-light'];
  const textColor = themes[theme]['--color-text-light'];
  const textSecondaryColor = themes[theme]['--color-text-secondary-light'];
  
  // Создаем CSS для переопределения стандартных классов tailwind
  const css = `
    :root:not(.dark) {
      --tw-bg-opacity: 1;
      --tw-text-opacity: 1;
      --tw-border-opacity: 1;
    }
    
    :root:not(.dark) .bg-background-light {
      background-color: ${bgColor} !important;
    }
    
    :root:not(.dark) .bg-surface-light {
      background-color: ${surfaceColor} !important;
    }
    
    :root:not(.dark) .border-border-light {
      border-color: ${borderColor} !important;
    }
    
    :root:not(.dark) .text-text-light {
      color: ${textColor} !important;
    }
    
    :root:not(.dark) .text-text-secondary-light {
      color: ${textSecondaryColor} !important;
    }
    
    /* Исправление header бэкграунда */
    :root:not(.dark) header.bg-white {
      background-color: ${surfaceColor} !important;
    }
    
    /* Исправление глобального бэкграунда */
    :root:not(.dark) main.bg-background-light {
      background-color: ${bgColor} !important;
    }
    
    /* Исправление footer бэкграунда */
    :root:not(.dark) footer.bg-surface-light {
      background-color: ${surfaceColor} !important;
    }
  `;
  
  styleElement.textContent = css;
}

// При монтировании компонента загружаем сохраненную тему
onMounted(() => {
  const savedTheme = localStorage.getItem('selectedLightTheme') as Theme;
  
  if (savedTheme && Object.keys(themes).includes(savedTheme)) {
    currentTheme.value = savedTheme;
    switchToTheme(savedTheme);
  } else {
    // Если нет сохраненной темы, применяем стандартную
    switchToTheme('neutralGray');
  }
});
</script>

<style scoped>
.theme-button {
  padding: 0.5rem;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.theme-button:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.theme-button.active {
  border-color: var(--color-border-light);
  background-color: rgba(0, 0, 0, 0.05);
}
</style> 