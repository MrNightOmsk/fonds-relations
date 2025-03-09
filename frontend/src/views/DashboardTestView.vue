<template>
  <div class="dashboard">
    <h1 class="text-2xl font-bold mb-4">Улучшенный Дашборд (Тестовая версия)</h1>
    
    <!-- Секция поиска -->
    <div class="search-section mb-6">
      <h2 class="text-lg font-medium mb-2">Поиск</h2>
      <div class="border p-4 bg-blue-50 rounded-lg">
        <p class="text-sm mb-2">Работает поиск по словам: "иван", "петр", "скам", "долг"</p>
        <UnifiedSearch @select="handleSearchResultSelect" />
      </div>
    </div>
    
    <!-- Быстрые действия -->
    <div class="quick-actions mb-6">
      <h2 class="text-lg font-medium mb-2">Быстрые действия</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
        <button @click="showCreateCaseModal = true" class="action-btn bg-blue-600 text-white p-4 rounded-lg flex items-center">
          <span class="icon mr-2 text-xl">+</span>
          <span>Создать кейс</span>
        </button>
        <button @click="navigateTo('/cases')" class="action-btn bg-green-600 text-white p-4 rounded-lg flex items-center">
          <span class="icon mr-2 text-xl">📁</span>
          <span>Мои кейсы</span>
        </button>
      </div>
    </div>

    <!-- Статистика и недавние кейсы -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="bg-white p-6 rounded-lg shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Статистика</h2>
        <div class="space-y-3">
          <div class="flex justify-between items-center p-2 bg-blue-50 rounded">
            <span class="font-medium">Игроков:</span>
            <span class="bg-blue-100 text-blue-800 py-1 px-2 rounded-full">24</span>
          </div>
          <div class="flex justify-between items-center p-2 bg-green-50 rounded">
            <span class="font-medium">Активных кейсов:</span>
            <span class="bg-green-100 text-green-800 py-1 px-2 rounded-full">8</span>
          </div>
          <div class="flex justify-between items-center p-2 bg-purple-50 rounded">
            <span class="font-medium">Закрытых кейсов:</span>
            <span class="bg-purple-100 text-purple-800 py-1 px-2 rounded-full">16</span>
          </div>
        </div>
      </div>
      
      <div class="lg:col-span-2 bg-white rounded-lg shadow-sm p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold">Последние кейсы</h2>
          <button class="text-blue-600 text-sm hover:underline">Смотреть все</button>
        </div>
        <div class="space-y-3">
          <div class="p-3 border border-gray-100 rounded-lg hover:bg-gray-50 cursor-pointer">
            <div class="flex justify-between">
              <h3 class="font-medium">Скам игрока на форуме</h3>
              <span class="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full">Открыт</span>
            </div>
            <div class="text-sm text-gray-500 mt-1">
              <span>Игрок: <span class="text-gray-700">Иванов И.И.</span></span>
              <span class="ml-2">Создан: <span class="text-gray-700">01.03.2023</span></span>
            </div>
          </div>
          <div class="p-3 border border-gray-100 rounded-lg hover:bg-gray-50 cursor-pointer">
            <div class="flex justify-between">
              <h3 class="font-medium">Долг за игру в покер</h3>
              <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">В работе</span>
            </div>
            <div class="text-sm text-gray-500 mt-1">
              <span>Игрок: <span class="text-gray-700">Петров П.П.</span></span>
              <span class="ml-2">Создан: <span class="text-gray-700">28.02.2023</span></span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Модальное окно создания кейса -->
    <CreateCaseModal :show="showCreateCaseModal" @close="showCreateCaseModal = false" @created="handleCaseCreated" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import UnifiedSearch from '@/components/search/UnifiedSearch.vue';
import CreateCaseModal from '@/components/case/CreateCaseModal.vue';

const router = useRouter();
const showCreateCaseModal = ref(false);

// Обработчики
const handleSearchResultSelect = (result) => {
  console.log('Выбран результат поиска:', result);
};

const navigateTo = (path) => {
  router.push(path);
};

const handleCaseCreated = (newCase) => {
  showCreateCaseModal.value = false;
  console.log('Создан новый кейс:', newCase);
  alert('Кейс успешно создан!');
};
</script>

<style scoped>
.dashboard {
  padding: 1.5rem;
}

.action-btn {
  transition: all 0.2s ease;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style> 