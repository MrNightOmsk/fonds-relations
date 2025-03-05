// Базовый URL для API запросов
export const API_URL = '/api/v1';

// Таймаут для запросов в миллисекундах
export const REQUEST_TIMEOUT = 30000;

// Функция для формирования полного URL для запроса
export const getFullUrl = (endpoint: string) => {
  // Убедимся, что endpoint начинается с /
  if (!endpoint.startsWith('/')) {
    endpoint = `/${endpoint}`;
  }
  
  return `${API_URL}${endpoint}`;
};

// Настройка Axios с перехватчиком для добавления токена
import axios from 'axios';

// Создаем экземпляр axios с базовыми настройками
export const apiClient = axios.create({
  baseURL: API_URL,
  timeout: REQUEST_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Добавляем перехватчик для запросов
apiClient.interceptors.request.use(
  (config) => {
    // Получаем токен из localStorage
    const token = localStorage.getItem('token');
    
    // Если токен существует, добавляем его в заголовки
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Экспортируем настроенный экземпляр
export default apiClient; 