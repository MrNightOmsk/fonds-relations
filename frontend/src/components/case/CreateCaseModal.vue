<template>
  <div v-if="show" class="modal-backdrop" @mousedown="onBackdropMouseDown" @mouseup="onBackdropMouseUp">
    <div class="modal-content bg-white dark:bg-background-dark border border-border-light dark:border-border-dark">
      <div class="modal-header border-b border-border-light dark:border-border-dark">
        <h3 class="text-lg font-medium text-text-light dark:text-text-dark">Создать новый кейс</h3>
        <button @click="close" class="close-btn text-text-secondary-light dark:text-text-secondary-dark hover:text-text-light dark:hover:text-text-dark">
          <span>×</span>
        </button>
      </div>
      
      <div class="modal-body">
        <form @submit.prevent="submitForm">
          <!-- Заголовок кейса -->
          <div class="form-group">
            <label class="form-label text-text-light dark:text-text-dark">Заголовок</label>
            <input 
              v-model="form.title" 
              type="text" 
              class="form-input text-text-light dark:text-text-dark bg-white dark:bg-background-dark border-border-light dark:border-border-dark" 
              placeholder="Введите заголовок кейса" 
              required
            />
          </div>
          
          <!-- Поиск игрока -->
          <div class="form-group">
            <label class="form-label text-text-light dark:text-text-dark">Игрок</label>
            <div class="relative">
              <input 
                v-model="playerSearch" 
                type="text" 
                class="form-input text-text-light dark:text-text-dark bg-white dark:bg-background-dark border-border-light dark:border-border-dark" 
                placeholder="Найти игрока..." 
                @input="debouncedSearchPlayers"
              />
              
              <div v-if="playersLoading" class="absolute right-3 top-2.5">
                <div class="inline-block animate-spin h-4 w-4 border-2 border-primary dark:border-primary-dark rounded-full border-t-transparent"></div>
              </div>
              
              <!-- Результаты поиска игроков -->
              <div v-if="playerResults.length > 0 && playerSearch" 
                class="results-container mt-1 absolute z-10 w-full shadow-lg rounded-lg border border-border-light dark:border-border-dark overflow-hidden bg-white dark:bg-background-dark">
                <div v-for="player in playerResults" :key="player.id" 
                    @click="selectPlayer(player)" 
                    class="result-item p-2 hover:bg-surface-light dark:hover:bg-surface-dark cursor-pointer">
                  <div class="font-medium text-text-light dark:text-text-dark">{{ player.title }}</div>
                  <div class="text-xs text-text-secondary-light dark:text-text-secondary-dark" v-if="player.details">{{ player.details }}</div>
                </div>
              </div>
            </div>
            
            <!-- Выбранный игрок -->
            <div v-if="form.player_id" class="mt-2 p-2 bg-blue-50 rounded flex justify-between items-center">
              <span class="text-gray-800">{{ selectedPlayerName }}</span>
              <button @click="form.player_id = ''; selectedPlayerName = ''" class="text-red-500 text-sm" type="button">
                Удалить
              </button>
            </div>
          </div>
          
          <!-- Описание -->
          <div class="form-group">
            <label class="form-label text-text-light dark:text-text-dark">Описание</label>
            <textarea 
              v-model="form.description" 
              class="form-input h-24 text-text-light dark:text-text-dark bg-white dark:bg-background-dark border-border-light dark:border-border-dark" 
              placeholder="Опишите ситуацию..." 
              required
            ></textarea>
          </div>
          
          <!-- Сумма и валюта -->
          <div class="grid grid-cols-2 gap-3">
            <div class="form-group">
              <label class="form-label text-text-light dark:text-text-dark">Сумма</label>
              <input 
                v-model="form.amount" 
                type="number" 
                min="0" 
                step="0.01" 
                class="form-input text-text-light dark:text-text-dark bg-white dark:bg-background-dark border-border-light dark:border-border-dark" 
                placeholder="0.00"
              />
            </div>
            
            <div class="form-group">
              <label class="form-label text-text-light dark:text-text-dark">Валюта</label>
              <select v-model="form.currency" class="form-input text-text-light dark:text-text-dark bg-white dark:bg-background-dark border-border-light dark:border-border-dark">
                <option value="USD">USD</option>
                <option value="EUR">EUR</option>
                <option value="RUB">RUB</option>
              </select>
            </div>
          </div>
          
          <!-- Кнопки -->
          <div class="flex justify-end space-x-3 mt-4">
            <button type="button" @click="close" class="btn btn-secondary">
              Отмена
            </button>
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              <span v-if="submitting">
                <span class="inline-block animate-spin h-4 w-4 border-2 border-white rounded-full border-t-transparent mr-2"></span>
                Сохранение...
              </span>
              <span v-else>Создать кейс</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// @ts-ignore
import { ref, computed, watch } from 'vue';
import { useSearchApi } from '@/api/search';
import type { SearchResult } from '@/types/search';

// Определение пропсов
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
});

// Определение эмиттеров
const emit = defineEmits(['close', 'created']);

// API
const searchApi = useSearchApi();

// Состояние компонента
const form = ref({
  title: '',
  description: '',
  player_id: '',
  amount: '',
  currency: 'USD',
  status: 'open'
});

const playerSearch = ref('');
const playerResults = ref<SearchResult[]>([]);
const playersLoading = ref(false);
const selectedPlayerName = ref('');
const submitting = ref(false);
let searchTimeout: ReturnType<typeof setTimeout> | null = null;
// Для отслеживания места, где была нажата клавиша мыши
const backdropMouseDownTarget = ref<EventTarget | null>(null);

// Методы
const close = () => {
  emit('close');
};

// Отслеживаем где была нажата клавиша мыши
const onBackdropMouseDown = (event: MouseEvent) => {
  if (event.target === event.currentTarget) {
    backdropMouseDownTarget.value = event.target;
  }
};

// Проверяем, что отпускание клавиши произошло на том же элементе, что и нажатие
const onBackdropMouseUp = (event: MouseEvent) => {
  if (backdropMouseDownTarget.value === event.target && event.target === event.currentTarget) {
    close();
  }
  backdropMouseDownTarget.value = null;
};

// Поиск игроков с дебаунсингом
const debouncedSearchPlayers = () => {
  if (searchTimeout) {
    clearTimeout(searchTimeout);
  }
  
  if (playerSearch.value.trim().length < 2) {
    playerResults.value = [];
    return;
  }
  
  searchTimeout = setTimeout(() => {
    searchPlayers();
  }, 300); // 300ms задержка
};

// Поиск игроков
const searchPlayers = async () => {
  if (playerSearch.value.trim().length < 2) {
    playerResults.value = [];
    return;
  }
  
  playersLoading.value = true;
  
  try {
    // Используем API для поиска игроков
    const results = await searchApi.searchPlayers(playerSearch.value);
    playerResults.value = results.filter(result => result.type === 'player');
  } catch (error) {
    console.error('Ошибка при поиске игроков:', error);
    playerResults.value = [];
  } finally {
    playersLoading.value = false;
  }
};

// Выбор игрока из результатов поиска
const selectPlayer = (player: SearchResult) => {
  form.value.player_id = player.id;
  selectedPlayerName.value = player.title;
  playerSearch.value = '';
  playerResults.value = [];
};

// Отправка формы
const submitForm = async () => {
  if (submitting.value) return;
  
  submitting.value = true;
  
  try {
    // Вместо имитации отправки на сервер используем реальный API
    const { useCasesApi } = await import('@/api/cases');
    const { useAuthStore } = await import('@/stores/auth');
    
    const casesApi = useCasesApi();
    const authStore = useAuthStore();
    
    // Проверка наличия пользователя и его фонда
    if (!authStore.user) {
      console.error('Ошибка: Пользователь не авторизован');
      alert('Необходимо войти в систему для создания кейса');
      submitting.value = false;
      return;
    }
    
    if (!authStore.user.fund_id) {
      console.error('Ошибка: У пользователя нет привязки к фонду', authStore.user);
      alert('У вашей учетной записи отсутствует привязка к фонду. Обратитесь к администратору.');
      submitting.value = false;
      return;
    }
    
    // Создаем объект с данными кейса
    const caseData = {
      title: form.value.title,
      description: form.value.description,
      player_id: form.value.player_id || null,
      status: form.value.status,
      arbitrage_amount: form.value.amount ? parseFloat(form.value.amount) : 0.0,
      arbitrage_currency: form.value.currency || 'USD',
      created_by_fund_id: authStore.user.fund_id
    };
    
    console.log('Данные пользователя:', authStore.user);
    console.log('Отправка данных для создания кейса:', caseData);
    
    // Отправляем запрос на создание
    const newCase = await casesApi.createCase(caseData);
    
    console.log('Кейс успешно создан:', newCase);
    
    // Оповещаем родительский компонент о создании с реальным ID от сервера
    emit('created', newCase);
    
    // Сбрасываем форму
    resetForm();
  } catch (error: any) {
    console.error('Ошибка при создании кейса:', error);
    
    // Проверка на ошибку валидации и вывод информативного сообщения
    if (error.response && error.response.data && error.response.data.detail) {
      // Обработка детальной информации об ошибке
      const errorDetails = error.response.data.detail;
      let errorMessage = 'Ошибка при создании кейса: ';
      
      if (Array.isArray(errorDetails)) {
        errorDetails.forEach(detail => {
          const field = detail.loc[detail.loc.length - 1];
          errorMessage += `поле "${field}" - ${detail.msg}; `;
        });
      } else {
        errorMessage += errorDetails;
      }
      
      console.error(errorMessage);
      alert(errorMessage);
    } else {
      alert('Произошла ошибка при создании кейса');
    }
  } finally {
    submitting.value = false;
  }
};

// Сброс формы
const resetForm = () => {
  form.value = {
    title: '',
    description: '',
    player_id: '',
    amount: '',
    currency: 'USD',
    status: 'open'
  };
  playerSearch.value = '';
  selectedPlayerName.value = '';
};

// Очистка при удалении компонента
watch(() => props.show, (newVal) => {
  if (!newVal) {
    resetForm();
  }
});
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
}

.modal-content {
  background-color: white;
  border-radius: 0.5rem;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.close-btn {
  font-size: 1.5rem;
  background: transparent;
  border: none;
  cursor: pointer;
  color: #718096;
}

.modal-body {
  padding: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #cbd5e0;
  border-radius: 0.25rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  font-weight: 500;
  cursor: pointer;
}

.btn-primary {
  background-color: #3182ce;
  color: white;
}

.btn-primary:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #e2e8f0;
  color: #4a5568;
}
</style> 