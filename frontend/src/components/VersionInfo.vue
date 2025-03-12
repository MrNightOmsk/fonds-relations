<template>
  <div class="version-info-container">
    <!-- Иконка уведомления о новой версии -->
    <div 
      v-if="showNotification" 
      class="notification-badge"
      :class="{ 'animate-pulse': animateBadge }"
      @click="openChangelogModal"
    >
      <span class="notification-dot"></span>
      <span class="notification-icon">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09Z" />
        </svg>
      </span>
    </div>

    <!-- Кнопка информации о версии -->
    <button 
      @click="openChangelogModal" 
      class="version-button"
      title="Информация о версии"
    >
      v{{ version }}
    </button>

    <!-- Модальное окно с чанджлогом -->
    <div v-if="isModalOpen" class="changelog-modal-overlay" @click="closeChangelogModal">
      <div class="changelog-modal" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">История изменений</h2>
          <button @click="closeChangelogModal" class="close-button">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="modal-content">
          <div class="version-info">
            <div class="current-version">
              <span class="version-label">Текущая версия:</span>
              <span class="version-number">{{ version }}</span>
            </div>
            <div class="backend-version">
              <span class="version-label">Версия бэкенда:</span>
              <span class="version-number">{{ backendVersion }}</span>
            </div>
          </div>

          <div class="changelog-entries">
            <div 
              v-for="(entry, index) in changelogEntries" 
              :key="index" 
              class="changelog-entry"
              :class="{ 'current-version-entry': entry.version === version }"
            >
              <div class="entry-header">
                <h3 class="entry-version">
                  {{ entry.version }}
                  <span v-if="entry.version === version" class="current-tag">текущая</span>
                </h3>
                <span class="entry-date">{{ entry.date }}</span>
              </div>
              <div class="entry-sections">
                <div v-for="(section, sectionIndex) in entry.sections" :key="sectionIndex" class="entry-section">
                  <h4 class="section-title">{{ section.title }}</h4>
                  <ul class="section-items">
                    <li v-for="(item, itemIndex) in section.items" :key="itemIndex" class="section-item">
                      {{ item }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';

const props = defineProps({
  version: {
    type: String,
    default: '0.3.1'
  },
  backendVersion: {
    type: String,
    default: '0.3.13'
  },
  showNotification: {
    type: Boolean,
    default: true
  }
});

const isModalOpen = ref(false);
const animateBadge = ref(true);
const userHasSeenLatestVersion = ref(false);

// Форматируем данные чанджлога для отображения
const changelogEntries = computed(() => {
  return [
    {
      version: '0.3.1',
      date: '18 марта 2025',
      sections: [
        {
          title: 'Изменено',
          items: [
            'Удалена фильтрация игроков по фонду - теперь менеджеры всех фондов могут видеть информацию о всех игроках',
            'Исправлена проблема, из-за которой на странице /players список игроков был пустой, хотя API возвращал данные'
          ]
        }
      ]
    },
    {
      version: '0.3.0',
      date: '15 марта 2025',
      sections: [
        {
          title: 'Добавлено',
          items: [
            'Реализованы три варианта светлой темы: нейтральный серый, теплый офф-вайт и современный холодный',
            'Создана демо-страница для сравнения и тестирования тем',
            'Добавлен визуальный селектор тем в шапке сайта (рядом с переключателем день/ночь)',
            'Реализовано сохранение выбранной светлой темы в localStorage'
          ]
        },
        {
          title: 'Изменено',
          items: [
            'Улучшены тени и контраст интерфейса для лучшей читаемости',
            'Обновлены стили карточек и элементов управления',
            'Оптимизированы CSS-переменные для более гибкой настройки тем',
            'Основной цвет фона заменен с чисто белого на более мягкий серый'
          ]
        }
      ]
    },
    {
      version: '0.2.0',
      date: '13 марта 2025',
      sections: [
        {
          title: 'Добавлено',
          items: [
            'Реализована поддержка темной темы во всем приложении',
            'Добавлено автоматическое определение предпочтений системной темы',
            'Добавлена кнопка переключения между светлой и темной темой в шапке',
            'Сохранение предпочтений темы в localStorage'
          ]
        },
        {
          title: 'Изменено',
          items: [
            'Обновлена цветовая палитра для поддержки двух тем',
            'Обновлена конфигурация Tailwind для поддержки темной темы',
            'Все компоненты адаптированы для работы с темной темой'
          ]
        }
      ]
    }
  ];
});

// Проверяет, видел ли пользователь последнюю версию
function checkIfUserHasSeenLatestVersion() {
  const lastSeenVersion = localStorage.getItem('lastSeenVersion');
  const currentVersion = String(props.version);
  if (lastSeenVersion === currentVersion) {
    userHasSeenLatestVersion.value = true;
    animateBadge.value = false;
  } else {
    userHasSeenLatestVersion.value = false;
    animateBadge.value = true;
  }
}

// Открывает модальное окно с чанджлогом
function openChangelogModal() {
  isModalOpen.value = true;
  localStorage.setItem('lastSeenVersion', String(props.version));
  animateBadge.value = false;
  userHasSeenLatestVersion.value = true;
}

// Закрывает модальное окно
function closeChangelogModal() {
  isModalOpen.value = false;
}

// При монтировании компонента проверяем, видел ли пользователь последнюю версию
onMounted(() => {
  checkIfUserHasSeenLatestVersion();
  
  // Останавливаем анимацию через 5 секунд, чтобы не раздражать пользователя
  setTimeout(() => {
    animateBadge.value = false;
  }, 5000);
});
</script>

<style scoped>
.version-info-container {
  position: relative;
  display: inline-block;
}

.version-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
  background-color: rgba(var(--color-primary-rgb), 0.1);
  color: var(--color-primary);
  cursor: pointer;
  transition: all 0.2s;
}

.version-button:hover {
  background-color: rgba(var(--color-primary-rgb), 0.2);
}

.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  width: 16px;
  height: 16px;
  background-color: var(--color-primary);
  border-radius: 50%;
  color: white;
  font-size: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 1;
}

.notification-dot {
  width: 6px;
  height: 6px;
  background-color: white;
  border-radius: 50%;
}

.notification-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
}

.changelog-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.changelog-modal {
  width: calc(100% - 2rem);
  max-width: 600px;
  max-height: calc(100vh - 2rem);
  background-color: var(--color-background-light);
  border-radius: 0.5rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 1rem;
  border-bottom: 1px solid var(--color-border-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-light);
}

.close-button {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-text-secondary-light);
  transition: color 0.2s;
}

.close-button:hover {
  color: var(--color-text-light);
}

.modal-content {
  padding: 1rem;
  overflow-y: auto;
  flex: 1;
}

.version-info {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-border-light);
}

.current-version, .backend-version {
  padding: 0.5rem 0.75rem;
  background-color: var(--color-surface-light);
  border-radius: 0.375rem;
}

.version-label {
  font-size: 0.875rem;
  color: var(--color-text-secondary-light);
  margin-right: 0.5rem;
}

.version-number {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text-light);
}

.changelog-entries {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.changelog-entry {
  padding: 1rem;
  background-color: var(--color-surface-light);
  border-radius: 0.375rem;
  border: 1px solid var(--color-border-light);
}

.current-version-entry {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 1px var(--color-primary-light);
}

.entry-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.entry-version {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text-light);
  display: flex;
  align-items: center;
}

.current-tag {
  font-size: 0.75rem;
  padding: 0.125rem 0.375rem;
  background-color: var(--color-primary);
  color: white;
  border-radius: 0.25rem;
  margin-left: 0.5rem;
}

.entry-date {
  font-size: 0.75rem;
  color: var(--color-text-secondary-light);
}

.entry-sections {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text-light);
  margin-bottom: 0.5rem;
}

.section-items {
  padding-left: 1.5rem;
  list-style-type: disc;
}

.section-item {
  font-size: 0.875rem;
  color: var(--color-text-light);
  margin-bottom: 0.25rem;
  line-height: 1.4;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Поддержка тёмной темы */
@media (prefers-color-scheme: dark) {
  .changelog-modal {
    background-color: var(--color-background-dark);
  }
  
  .modal-header {
    border-color: var(--color-border-dark);
  }
  
  .modal-title {
    color: var(--color-text-dark);
  }
  
  .close-button {
    color: var(--color-text-secondary-dark);
  }
  
  .close-button:hover {
    color: var(--color-text-dark);
  }
  
  .version-info {
    border-color: var(--color-border-dark);
  }
  
  .current-version, .backend-version {
    background-color: var(--color-surface-dark);
  }
  
  .version-label {
    color: var(--color-text-secondary-dark);
  }
  
  .version-number {
    color: var(--color-text-dark);
  }
  
  .changelog-entry {
    background-color: var(--color-surface-dark);
    border-color: var(--color-border-dark);
  }
  
  .entry-version {
    color: var(--color-text-dark);
  }
  
  .entry-date {
    color: var(--color-text-secondary-dark);
  }
  
  .section-title {
    color: var(--color-text-dark);
  }
  
  .section-item {
    color: var(--color-text-dark);
  }
}
</style> 