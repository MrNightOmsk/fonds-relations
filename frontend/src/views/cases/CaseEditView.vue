<template>
  <div class="case-edit p-4">
    <div v-if="loading" class="text-center py-16">
      <div class="animate-spin h-12 w-12 border-4 border-primary dark:border-primary-dark rounded-full border-t-transparent mx-auto"></div>
      <p class="mt-4 text-text-secondary-light dark:text-text-secondary-dark">Загрузка дела...</p>
    </div>
    
    <div v-else-if="error" class="p-6 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 rounded-lg my-4">
      <h3 class="text-lg font-medium mb-2">Ошибка загрузки</h3>
      <p>{{ error }}</p>
      <button 
        @click="fetchCase" 
        class="mt-4 px-4 py-2 bg-red-600 dark:bg-red-800 text-white rounded hover:bg-red-700 dark:hover:bg-red-700"
      >
        Попробовать снова
      </button>
    </div>
    
    <div v-else>
      <!-- Заголовок страницы -->
      <div class="bg-white dark:bg-background-dark p-6 rounded-lg shadow-sm mb-6 border border-border-light dark:border-border-dark">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-medium text-text-light dark:text-text-dark">
            Редактирование дела #{{ caseData.case_number || caseData.id?.substring(0, 8) }}
          </h1>
          <div class="flex space-x-2">
            <button 
              @click="navigateBack" 
              class="px-4 py-2 border border-border-light dark:border-border-dark rounded-lg text-text-light dark:text-text-dark hover:bg-surface-light dark:hover:bg-surface-dark"
            >
              Отмена
            </button>
            <button 
              @click="saveCase" 
              class="px-4 py-2 bg-primary dark:bg-primary-dark text-white rounded-lg hover:bg-primary-600 dark:hover:bg-primary-500"
              :disabled="saving"
            >
              <span v-if="saving">Сохранение...</span>
              <span v-else>Сохранить изменения</span>
            </button>
          </div>
        </div>
      </div>
      
      <!-- Форма редактирования -->
      <div class="bg-white dark:bg-background-dark p-6 rounded-lg shadow-sm mb-6 border border-border-light dark:border-border-dark">
        <h2 class="text-lg font-medium mb-4 text-text-light dark:text-text-dark">Основная информация</h2>
        
        <div class="space-y-4">
          <!-- Название дела -->
          <div>
            <label for="title" class="block font-medium text-text-light dark:text-text-dark mb-1">Название дела:</label>
            <input 
              id="title" 
              v-model="caseData.title" 
              type="text" 
              class="w-full p-2 border border-border-light dark:border-border-dark rounded bg-white dark:bg-background-dark text-text-light dark:text-text-dark"
              placeholder="Введите название дела"
            />
          </div>
          
          <!-- Описание -->
          <div>
            <label for="description" class="block font-medium text-text-light dark:text-text-dark mb-1">Описание:</label>
            <textarea 
              id="description" 
              v-model="caseData.description" 
              rows="5" 
              class="w-full p-2 border border-border-light dark:border-border-dark rounded bg-white dark:bg-background-dark text-text-light dark:text-text-dark"
              placeholder="Введите описание дела"
            ></textarea>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Тип дела -->
            <div>
              <label for="case_type" class="block font-medium text-text-light dark:text-text-dark mb-1">Тип дела:</label>
              <select 
                id="case_type" 
                v-model="caseData.case_type" 
                class="w-full p-2 border border-border-light dark:border-border-dark rounded bg-white dark:bg-background-dark text-text-light dark:text-text-dark"
              >
                <option value="scam">Скам</option>
                <option value="debt">Долг</option>
                <option value="multi_accounting">Мультиаккаунтинг</option>
                <option value="collusion">Сговор</option>
                <option value="software">Запрещенное ПО</option>
                <option value="other">Другое</option>
              </select>
            </div>
            
            <!-- Статус -->
            <div>
              <label for="status" class="block font-medium text-text-light dark:text-text-dark mb-1">Статус:</label>
              <select 
                id="status" 
                v-model="caseData.status" 
                class="w-full p-2 border border-border-light dark:border-border-dark rounded bg-white dark:bg-background-dark text-text-light dark:text-text-dark"
              >
                <option value="open">Открыт</option>
                <option value="in_progress">В работе</option>
                <option value="resolved">Решён</option>
                <option value="closed">Закрыт</option>
              </select>
            </div>
          </div>
          
          <!-- Сумма и валюта -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label for="amount" class="block font-medium text-text-light dark:text-text-dark mb-1">Сумма:</label>
              <input 
                id="amount" 
                v-model.number="caseData.amount" 
                type="number" 
                min="0" 
                step="0.01" 
                class="w-full p-2 border border-border-light dark:border-border-dark rounded bg-white dark:bg-background-dark text-text-light dark:text-text-dark"
                placeholder="Введите сумму"
              />
            </div>
            
            <div>
              <label for="currency" class="block font-medium text-text-light dark:text-text-dark mb-1">Валюта:</label>
              <select 
                id="currency" 
                v-model="caseData.currency" 
                class="w-full p-2 border border-border-light dark:border-border-dark rounded bg-white dark:bg-background-dark text-text-light dark:text-text-dark"
              >
                <option value="USD">USD</option>
                <option value="EUR">EUR</option>
                <option value="RUB">RUB</option>
              </select>
            </div>
          </div>
          
          <!-- Арбитраж -->
          <div class="border-t border-border-light dark:border-border-dark pt-4 mt-4">
            <h3 class="font-medium text-text-light dark:text-text-dark mb-2">Информация об арбитраже</h3>
            
            <div class="space-y-4">
              <div>
                <label for="arbitrage_type" class="block font-medium text-text-light dark:text-text-dark mb-1">Тип арбитража:</label>
                <select 
                  id="arbitrage_type" 
                  v-model="caseData.arbitrage_type" 
                  class="w-full p-2 border border-border-light dark:border-border-dark rounded bg-white dark:bg-background-dark text-text-light dark:text-text-dark"
                >
                  <option value="">Не указан</option>
                  <option value="pending">В ожидании</option>
                  <option value="in_progress">В процессе</option>
                  <option value="completed">Завершен</option>
                  <option value="rejected">Отклонен</option>
                </select>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label for="arbitrage_amount" class="block font-medium text-text-light dark:text-text-dark mb-1">Сумма арбитража:</label>
                  <input 
                    id="arbitrage_amount" 
                    v-model.number="caseData.arbitrage_amount" 
                    type="number" 
                    min="0" 
                    step="0.01" 
                    class="w-full p-2 border border-border-light dark:border-border-dark rounded bg-white dark:bg-background-dark text-text-light dark:text-text-dark"
                    placeholder="Введите сумму арбитража"
                  />
                </div>
                
                <div>
                  <label for="arbitrage_currency" class="block font-medium text-text-light dark:text-text-dark mb-1">Валюта арбитража:</label>
                  <select 
                    id="arbitrage_currency" 
                    v-model="caseData.arbitrage_currency" 
                    class="w-full p-2 border border-border-light dark:border-border-dark rounded bg-white dark:bg-background-dark text-text-light dark:text-text-dark"
                  >
                    <option value="USD">USD</option>
                    <option value="EUR">EUR</option>
                    <option value="RUB">RUB</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Кнопки действий -->
      <div class="flex justify-end space-x-2">
        <button 
          @click="navigateBack" 
          class="px-4 py-2 border border-border-light dark:border-border-dark rounded-lg text-text-light dark:text-text-dark hover:bg-surface-light dark:hover:bg-surface-dark"
        >
          Отмена
        </button>
        <button 
          @click="saveCase" 
          class="px-4 py-2 bg-primary dark:bg-primary-dark text-white rounded-lg hover:bg-primary-600 dark:hover:bg-primary-500"
          :disabled="saving"
        >
          <span v-if="saving">Сохранение...</span>
          <span v-else>Сохранить изменения</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import type { CaseExtended, CaseUpdate } from '@/types/models';

// Роутер и параметры маршрута
const router = useRouter();
const route = useRoute();
const caseId = route.params.id as string;

// Состояние компонента
const loading = ref(true);
const saving = ref(false);
const error = ref<string | null>(null);
const caseData = ref<Partial<CaseExtended>>({});
const casesApi = ref<any>(null);

// Загрузка данных кейса
const fetchCase = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    if (!casesApi.value) {
      casesApi.value = (await import('@/api/cases')).useCasesApi();
    }
    
    const caseDetails = await casesApi.value.getCaseById(caseId);
    caseData.value = { ...caseDetails };
    
    console.log('Загружены данные кейса:', caseData.value);
  } catch (err: any) {
    console.error('Ошибка при загрузке кейса:', err);
    error.value = err.message || 'Не удалось загрузить данные кейса';
  } finally {
    loading.value = false;
  }
};

// Сохранение изменений
const saveCase = async () => {
  saving.value = true;
  error.value = null;
  
  try {
    if (!casesApi.value) {
      casesApi.value = (await import('@/api/cases')).useCasesApi();
    }
    
    // Подготавливаем данные для обновления
    const updateData: CaseUpdate = {
      title: caseData.value.title,
      description: caseData.value.description,
      status: caseData.value.status as 'open' | 'closed',
      arbitrage_type: caseData.value.arbitrage_type,
      arbitrage_amount: caseData.value.arbitrage_amount,
      arbitrage_currency: caseData.value.arbitrage_currency
    };
    
    // Если есть поле case_type, добавляем его
    if (caseData.value.case_type) {
      // @ts-ignore - Добавляем поле, которого нет в типе CaseUpdate
      updateData.case_type = caseData.value.case_type;
    }
    
    // Если есть поля amount и currency, добавляем их
    if (caseData.value.amount !== undefined) {
      // @ts-ignore
      updateData.amount = caseData.value.amount;
    }
    
    if (caseData.value.currency) {
      // @ts-ignore
      updateData.currency = caseData.value.currency;
    }
    
    console.log('Отправка данных для обновления:', updateData);
    
    // Отправляем запрос на обновление
    const updatedCase = await casesApi.value.updateCase(caseId, updateData);
    
    console.log('Кейс успешно обновлен:', updatedCase);
    
    // Показываем уведомление об успешном сохранении
    alert('Кейс успешно обновлен');
    
    // Переходим на страницу просмотра кейса
    router.push(`/cases/${caseId}`);
  } catch (err: any) {
    console.error('Ошибка при сохранении кейса:', err);
    error.value = err.message || 'Не удалось сохранить изменения';
    alert(`Ошибка при сохранении: ${error.value}`);
  } finally {
    saving.value = false;
  }
};

// Навигация назад
const navigateBack = () => {
  router.push(`/cases/${caseId}`);
};

// Форматирование суммы
const formatAmount = (amount?: number, currency?: string): string => {
  if (amount === undefined || amount === null) return 'Не указана';
  
  const formatter = new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: currency || 'USD',
    minimumFractionDigits: 2
  });
  
  return formatter.format(amount);
};

// Загрузка данных при монтировании компонента
onMounted(() => {
  fetchCase();
});
</script>

<style scoped>
.case-edit {
  max-width: 1200px;
  margin: 0 auto;
}
</style> 