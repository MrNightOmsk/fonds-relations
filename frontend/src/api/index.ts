import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

// Создаем экземпляр axios с базовыми настройками
const apiClient: AxiosInstance = axios.create({
  // Используем относительный базовый URL для работы через прокси
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

console.log('API клиент настроен с базовым URL /api/v1');

// Интерцептор для добавления токена к запросам
apiClient.interceptors.request.use(
  (config) => {
    const url = config.url || '';
    // Убеждаемся, что URL заканчивается слешем, если это не параметризованный URL
    if (url && !url.includes('?') && !url.endsWith('/')) {
      config.url = `${url}/`;
    }
    
    console.log('Отправка запроса к:', config.baseURL + config.url);
    
    // Получаем токен из localStorage
    const token = localStorage.getItem('token');
    
    // Если токен существует, добавляем его в заголовки
    if (token) {
      console.log('Добавляем токен авторизации к запросу');
      config.headers.Authorization = `Bearer ${token}`;
    } else {
      console.log('Токен не найден, запрос будет отправлен без авторизации');
    }
    
    return config;
  },
  (error) => {
    console.error('Ошибка в интерцепторе запросов:', error);
    return Promise.reject(error);
  }
);

// Интерцептор для обработки ответов
apiClient.interceptors.response.use(
  (response) => {
    console.log('Успешный ответ от:', response.config.url);
    return response;
  },
  (error) => {
    console.error('Ошибка ответа:', error.config?.url, error.response?.status, error.message);
    
    // Обработка ошибки 401 (Unauthorized)
    if (error.response && error.response.status === 401) {
      console.log('Получен ответ 401, перенаправляем на страницу входа');
      // Очищаем токен и перенаправляем на страницу входа
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    
    return Promise.reject(error);
  }
);

// Типизированные методы для работы с API
export const api = {
  get: <T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.get<T>(url, config);
  },
  
  post: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.post<T>(url, data, config);
  },
  
  put: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.put<T>(url, data, config);
  },
  
  patch: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.patch<T>(url, data, config);
  },
  
  delete: <T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.delete<T>(url, config);
  },
};

export default api;