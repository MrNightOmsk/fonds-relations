<template>
  <div class="player-new min-h-screen bg-gray-50 py-6">
    <div class="container mx-auto px-4">
      <!-- Шапка с информацией о создании и кнопками -->
      <div class="bg-white rounded-xl shadow-md mb-8 overflow-hidden">
        <div class="px-6 py-5 flex flex-col md:flex-row justify-between items-center bg-gradient-to-r from-blue-500 to-indigo-600 text-white">
          <div>
            <h1 class="text-2xl font-bold">Создание нового игрока</h1>
            <p class="text-blue-100 mt-1">Заполните информацию о новом игроке</p>
          </div>
          <div class="flex space-x-3 mt-4 md:mt-0">
            <button 
              @click="$router.push('/players')" 
              class="px-4 py-2 bg-white/20 backdrop-blur-sm rounded-lg text-white hover:bg-white/30 transition-all duration-200"
            >
              Отмена
            </button>
            <button 
              @click="createPlayer" 
              class="px-6 py-2 bg-white rounded-lg text-blue-600 hover:bg-blue-50 transition-all duration-200 font-medium"
            >
              Сохранить
            </button>
          </div>
        </div>
        
        <!-- Прогресс-бар и переключение шагов -->
        <div class="px-6 py-4 border-b border-gray-100">
          <div class="flex justify-between mb-2">
            <div class="text-sm text-gray-500">Прогресс заполнения</div>
            <div class="text-sm font-medium text-blue-600">Шаг {{ currentStep }} из {{ totalSteps }}</div>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2.5">
            <div class="bg-blue-600 h-2.5 rounded-full transition-all duration-300" :style="{ width: `${(currentStep / totalSteps) * 100}%` }"></div>
          </div>
          <div class="flex justify-between mt-4 overflow-x-auto pb-1 hide-scrollbar">
            <button 
              v-for="step in steps" 
              :key="step.id"
              @click="currentStep = step.id"
              class="px-4 py-2 rounded-lg text-sm whitespace-nowrap transition-all duration-200"
              :class="currentStep === step.id ? 'bg-blue-100 text-blue-700 font-medium' : 'text-gray-500 hover:text-blue-600'"
            >
              {{ step.title }}
            </button>
          </div>
        </div>
      </div>
      
      <!-- Шаг 1: Основная информация -->
      <div v-if="currentStep === 1" class="space-y-6 transition-all duration-300">
        <div class="bg-white rounded-xl shadow-sm overflow-hidden">
          <div class="p-6">
            <h2 class="text-xl font-semibold text-gray-800 mb-6">Основная информация</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="form-group">
                <label class="block text-sm font-medium text-gray-700 mb-2">Имя</label>
                <input 
                  v-model="player.first_name" 
                  type="text" 
                  class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                  placeholder="Введите имя"
                />
              </div>
              
              <div class="form-group">
                <label class="block text-sm font-medium text-gray-700 mb-2">Фамилия</label>
                <input 
                  v-model="player.last_name" 
                  type="text" 
                  class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                  placeholder="Введите фамилию"
                />
              </div>
              
              <div class="form-group">
                <label class="block text-sm font-medium text-gray-700 mb-2">Отчество</label>
                <input 
                  v-model="player.middle_name" 
                  type="text" 
                  class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                  placeholder="Введите отчество"
                />
              </div>
            </div>
            
            <div class="mt-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">Примечания</label>
              <textarea 
                v-model="player.health_notes" 
                rows="4" 
                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                placeholder="Введите примечания"
              ></textarea>
            </div>
          </div>
        </div>
        
        <div class="flex justify-end">
          <button 
            @click="nextStep" 
            class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all duration-200 flex items-center"
          >
            Далее
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Шаг 2: Никнеймы и контакты -->
      <div v-if="currentStep === 2" class="space-y-6 transition-all duration-300">
        <div class="bg-white rounded-xl shadow-sm overflow-hidden">
          <div class="p-6">
            <h2 class="text-xl font-semibold text-gray-800 mb-6">Никнеймы</h2>
            
            <div class="form-group">
              <div class="flex flex-col md:flex-row gap-4">
                <div class="w-full md:w-1/2">
                  <label class="block text-sm font-medium text-gray-700 mb-2">Никнейм</label>
                  <input 
                    v-model="nickname.nickname" 
                    type="text" 
                    class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                    placeholder="Введите никнейм"
                  />
                </div>
                
                <div class="w-full md:w-1/2">
                  <label class="block text-sm font-medium text-gray-700 mb-2">Покер-рум</label>
                  <input 
                    v-model="nickname.room" 
                    type="text" 
                    class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                    placeholder="Введите название покер-рума"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-xl shadow-sm overflow-hidden">
          <div class="p-6">
            <h2 class="text-xl font-semibold text-gray-800 mb-6">Контактная информация</h2>
            
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
              <div class="flex">
                <span class="inline-flex items-center px-3 rounded-l-lg border border-r-0 border-gray-300 bg-gray-50 text-gray-500">
                  ✉️
                </span>
                <input 
                  v-model="email" 
                  type="email" 
                  class="w-full p-3 border border-gray-300 rounded-r-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                  placeholder="username@example.com"
                />
              </div>
            </div>
            
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">Телефон</label>
              <div class="flex">
                <span class="inline-flex items-center px-3 rounded-l-lg border border-r-0 border-gray-300 bg-gray-50 text-gray-500">
                  📱
                </span>
                <input 
                  v-model="phone.value" 
                  type="text" 
                  class="flex-1 p-3 border border-gray-300 rounded-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                  placeholder="+7 (XXX) XXX-XX-XX"
                />
                <input 
                  v-model="phone.description" 
                  type="text" 
                  class="w-1/3 p-3 border border-l-0 border-gray-300 rounded-r-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                  placeholder="Например, 'Мобильный'"
                />
              </div>
            </div>
          </div>
        </div>
        
        <div class="flex justify-between">
          <button 
            @click="prevStep" 
            class="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-all duration-200 flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M7.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l2.293 2.293a1 1 0 010 1.414z" clip-rule="evenodd" />
            </svg>
            Назад
          </button>
          <button 
            @click="nextStep" 
            class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all duration-200 flex items-center"
          >
            Далее
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Шаг 3: Адрес -->
      <div v-if="currentStep === 3" class="space-y-6 transition-all duration-300">
        <div class="bg-white rounded-xl shadow-sm overflow-hidden">
          <div class="p-6">
            <h2 class="text-xl font-semibold text-gray-800 mb-6">Адрес</h2>
            
            <div class="form-group mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">Полный адрес</label>
              <textarea 
                v-model="location.address" 
                rows="2" 
                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                placeholder="Введите адрес (улица, дом, квартира)"
              ></textarea>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="form-group">
                <label class="block text-sm font-medium text-gray-700 mb-2">Город</label>
                <input 
                  v-model="location.city" 
                  type="text" 
                  class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                  placeholder="Город"
                />
              </div>
              
              <div class="form-group">
                <label class="block text-sm font-medium text-gray-700 mb-2">Страна</label>
                <input 
                  v-model="location.country" 
                  type="text" 
                  class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                  placeholder="Страна"
                />
              </div>
              
              <div class="form-group">
                <label class="block text-sm font-medium text-gray-700 mb-2">Почтовый индекс</label>
                <input 
                  v-model="location.postal_code" 
                  type="text" 
                  class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                  placeholder="Почтовый индекс"
                />
              </div>
            </div>
          </div>
        </div>
        
        <div class="flex justify-between">
          <button 
            @click="prevStep" 
            class="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-all duration-200 flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M7.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l2.293 2.293a1 1 0 010 1.414z" clip-rule="evenodd" />
            </svg>
            Назад
          </button>
          <button 
            @click="nextStep" 
            class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all duration-200 flex items-center"
          >
            Далее
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Шаг 4: Социальные сети и методы оплаты -->
      <div v-if="currentStep === 4" class="space-y-6 transition-all duration-300">
        <div class="bg-white rounded-xl shadow-sm overflow-hidden">
          <div class="p-6">
            <h2 class="text-xl font-semibold text-gray-800 mb-6">Социальные сети</h2>
            
            <div class="form-group mb-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Платформа</label>
                  <div class="relative">
                    <select 
                      v-model="socialMedia.platform" 
                      class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all appearance-none pr-10"
                    >
                      <option value="" disabled>Выберите платформу</option>
                      <option value="telegram">Telegram</option>
                      <option value="whatsapp">WhatsApp</option>
                      <option value="instagram">Instagram</option>
                      <option value="facebook">Facebook</option>
                      <option value="vk">VK</option>
                      <option value="other">Другое</option>
                    </select>
                    <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                      <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                      </svg>
                    </div>
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Имя пользователя</label>
                  <input 
                    v-model="socialMedia.username" 
                    type="text" 
                    class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                    placeholder="Имя пользователя"
                  />
                </div>
              </div>
            </div>
            
            <div class="form-group mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">URL</label>
              <div class="flex">
                <span class="inline-flex items-center px-3 rounded-l-lg border border-r-0 border-gray-300 bg-gray-50 text-gray-500">
                  🔗
                </span>
                <input 
                  v-model="socialMedia.url" 
                  type="text" 
                  class="w-full p-3 border border-gray-300 rounded-r-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                  placeholder="https://example.com/username"
                />
              </div>
            </div>
            
            <div class="form-group">
              <label class="block text-sm font-medium text-gray-700 mb-2">Описание</label>
              <input 
                v-model="socialMedia.description" 
                type="text" 
                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                placeholder="Дополнительное описание"
              />
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-xl shadow-sm overflow-hidden">
          <div class="p-6">
            <h2 class="text-xl font-semibold text-gray-800 mb-6">Метод оплаты</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-4">
              <div class="form-group">
                <label class="block text-sm font-medium text-gray-700 mb-2">Тип метода</label>
                <div class="relative">
                  <select 
                    v-model="paymentMethod.type" 
                    class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all appearance-none pr-10"
                  >
                    <option value="" disabled>Выберите тип метода</option>
                    <option value="bank_card">Банковская карта</option>
                    <option value="crypto">Криптовалюта</option>
                    <option value="paypal">PayPal</option>
                    <option value="other">Другое</option>
                  </select>
                  <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                  </div>
                </div>
              </div>
              
              <div class="form-group">
                <label class="block text-sm font-medium text-gray-700 mb-2">Значение</label>
                <input 
                  v-model="paymentMethod.value" 
                  type="text" 
                  class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                  placeholder="Номер карты, адрес кошелька и т.д."
                />
              </div>
            </div>
            
            <div class="form-group">
              <label class="block text-sm font-medium text-gray-700 mb-2">Описание</label>
              <input 
                v-model="paymentMethod.description" 
                type="text" 
                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                placeholder="Дополнительное описание"
              />
            </div>
          </div>
        </div>
        
        <div class="flex justify-between">
          <button 
            @click="prevStep" 
            class="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-all duration-200 flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M7.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l2.293 2.293a1 1 0 010 1.414z" clip-rule="evenodd" />
            </svg>
            Назад
          </button>
          <button 
            @click="createPlayer" 
            class="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-all duration-200 flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            Создать игрока
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { usePlayerStore } from '@/stores/player';
import type { 
  CreatePlayerRequest, 
  PlayerNickname,
  PlayerContact,
  PlayerLocation,
  PlayerSocialMedia,
  PlayerPaymentMethod
} from '@/types/models';

const router = useRouter();
const playerStore = usePlayerStore();

// Пошаговый интерфейс
const currentStep = ref(1);
const totalSteps = 4;
const steps = [
  { id: 1, title: 'Основная информация' },
  { id: 2, title: 'Контакты' },
  { id: 3, title: 'Адрес' },
  { id: 4, title: 'Соцсети и оплата' }
];

// Функции для навигации по шагам
const nextStep = () => {
  if (currentStep.value < totalSteps) {
    currentStep.value++;
  }
};

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--;
  }
};

// Основная информация игрока
const player = ref({
  first_name: '',
  last_name: '',
  middle_name: '',
  health_notes: ''
});

// Никнейм
const nickname = ref<Partial<PlayerNickname>>({
  nickname: '',
  room: '',
  discipline: ''
});

// Email контакт
const email = ref('');

// Телефон
const phone = ref<Partial<PlayerContact>>({
  type: 'phone',
  value: '',
  description: ''
});

// Адрес
const location = ref<Partial<PlayerLocation>>({
  address: '',
  city: '',
  country: '',
  postal_code: ''
});

// Социальная сеть
const socialMedia = ref<Partial<PlayerSocialMedia>>({
  platform: '',
  username: '',
  url: '',
  description: ''
});

// Метод оплаты
const paymentMethod = ref<Partial<PlayerPaymentMethod>>({
  type: '',
  value: '',
  description: ''
});

// Функция для создания игрока
const createPlayer = async () => {
  try {
    // Формируем объект для отправки
    const playerData: CreatePlayerRequest = {
      ...player.value,
      nicknames: nickname.value.nickname ? [nickname.value] : [],
      contacts: [],
      locations: [],
      social_media: [],
      payment_methods: []
    };
    
    // Добавляем email, если указан
    if (email.value) {
      playerData.contacts?.push({
        type: 'email',
        value: email.value
      });
    }
    
    // Добавляем телефон, если указан
    if (phone.value.value) {
      playerData.contacts?.push({
        type: 'phone',
        value: phone.value.value,
        description: phone.value.description
      });
    }
    
    // Добавляем адрес, если указан
    if (location.value.address || location.value.city) {
      playerData.locations?.push(location.value);
    }
    
    // Добавляем социальную сеть, если указана
    if (socialMedia.value.platform && (socialMedia.value.username || socialMedia.value.url)) {
      playerData.social_media?.push(socialMedia.value);
    }
    
    // Добавляем метод оплаты, если указан
    if (paymentMethod.value.type && paymentMethod.value.value) {
      playerData.payment_methods?.push(paymentMethod.value);
    }
    
    // Отправляем запрос на создание игрока
    const createdPlayer = await playerStore.createPlayer(playerData);
    
    if (createdPlayer && createdPlayer.id) {
      // Перенаправляем на страницу созданного игрока
      router.push(`/players/${createdPlayer.id}`);
    } else {
      throw new Error('Не удалось создать игрока');
    }
  } catch (error) {
    console.error('Ошибка при создании игрока:', error);
    alert('Произошла ошибка при создании игрока. Пожалуйста, попробуйте снова.');
  }
};
</script>

<style scoped>
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style> 