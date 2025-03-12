<template>
  <div class="tabs-container">
    <!-- Заголовки вкладок -->
    <div class="tabs-header border-b border-border-light dark:border-border-dark">
      <div class="flex space-x-2">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="selectTab(tab.id)"
          class="px-4 py-2 text-sm font-medium transition-colors duration-200 rounded-t-lg"
          :class="[
            activeTab === tab.id 
              ? 'text-primary dark:text-primary-dark border-b-2 border-primary dark:border-primary-dark' 
              : 'text-text-secondary-light dark:text-text-secondary-dark hover:text-text-light dark:hover:text-text-dark'
          ]"
        >
          {{ tab.title }}
        </button>
      </div>
    </div>
    
    <!-- Содержимое вкладок -->
    <div class="tabs-content py-4">
      <slot v-if="$slots[activeTab]" :name="activeTab"></slot>
      <div v-else class="py-4 text-center text-text-secondary-light dark:text-text-secondary-dark">
        Содержимое для вкладки не найдено
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';

export interface Tab {
  id: string;
  title: string;
}

const props = defineProps({
  tabs: {
    type: Array,
    required: true,
    validator: (value: any[]) => {
      return value.every(tab => typeof tab.id === 'string' && typeof tab.title === 'string');
    }
  },
  defaultTab: {
    type: String,
    default: ''
  },
  persistent: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['change']);

// Активная вкладка
const activeTab = ref('');

// Выбор вкладки
const selectTab = (tabId: string) => {
  activeTab.value = tabId;
  emit('change', tabId);
  
  // Сохраняем выбор в localStorage, если включена опция persistent
  if (props.persistent) {
    try {
      localStorage.setItem(`tab-${window.location.pathname}`, tabId);
    } catch (e) {
      console.error('Не удалось сохранить выбор вкладки в localStorage:', e);
    }
  }
};

// Инициализация активной вкладки
onMounted(() => {
  // Если указана опция persistent, пытаемся восстановить выбор из localStorage
  if (props.persistent) {
    try {
      const savedTab = localStorage.getItem(`tab-${window.location.pathname}`);
      if (savedTab && (props.tabs as any[]).some(tab => tab.id === savedTab)) {
        activeTab.value = savedTab;
        emit('change', savedTab);
        return;
      }
    } catch (e) {
      console.error('Не удалось получить сохраненную вкладку из localStorage:', e);
    }
  }
  
  // Если не удалось восстановить из localStorage или опция не включена,
  // используем defaultTab или первую вкладку
  if (props.defaultTab && (props.tabs as any[]).some(tab => tab.id === props.defaultTab)) {
    activeTab.value = props.defaultTab;
  } else if ((props.tabs as any[]).length > 0) {
    activeTab.value = (props.tabs as any[])[0].id;
  }
  
  // Уведомляем о начальном выборе
  emit('change', activeTab.value);
});

// Следим за изменением списка вкладок
watch(() => props.tabs, (newTabs: any[]) => {
  // Если активная вкладка больше не существует в новом списке, выбираем первую
  if (newTabs.length > 0 && !newTabs.some(tab => tab.id === activeTab.value)) {
    activeTab.value = newTabs[0].id;
    emit('change', activeTab.value);
  }
}, { deep: true });
</script>

<style scoped>
.tabs-container {
  width: 100%;
}
</style> 