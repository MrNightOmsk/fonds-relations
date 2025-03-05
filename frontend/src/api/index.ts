// @ts-ignore
import axios, { AxiosInstance } from 'axios';
// @ts-ignore
import { useAuthStore } from '@/stores/auth';

// Создаем экземпляр Axios с базовой конфигурацией
const api: AxiosInstance = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  }
});

console.log('API клиент настроен с baseURL: /api/v1');

// Добавляем интерцептор для добавления токена авторизации к запросам
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Обработчик ответов с ошибками аутентификации
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      const authStore = useAuthStore();
      // Если токен истек или недействителен, выходим из системы
      authStore.logout();
    }
    return Promise.reject(error);
  }
);

export default api;