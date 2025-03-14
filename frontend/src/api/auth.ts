import axios from 'axios';
import apiClient from './config';

// Используем относительный путь для API запросов
const API_URL = '/api/v1';

interface LoginCredentials {
  username: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
}

/**
 * Выполняет запрос на аутентификацию пользователя
 * @param credentials Учетные данные пользователя
 * @returns Ответ с токеном доступа
 */
export const login = async (credentials: LoginCredentials): Promise<LoginResponse> => {
  const formData = new URLSearchParams();
  formData.append('username', credentials.username);
  formData.append('password', credentials.password);

  // Добавим более подробное логирование
  console.log('Window location:', window.location);
  console.log('Window location origin:', window.location.origin);
  console.log('API_URL:', API_URL);
  
  // Намеренно убираем слеш в конце URL, так как мы настроили nginx на обработку URL без слеша
  const url = `${API_URL}/login/access-token`;
  console.log('URL для авторизации (без слеша):', url);
  
  try {
    console.log(`Отправка запроса авторизации на ${url}`);
    
    // Используем относительный URL и отключаем редиректы
    const response = await axios.post<LoginResponse>(
      url,
      formData,
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        // Отключаем автоматическое следование за редиректами
        maxRedirects: 0
      }
    );
    console.log('Успешный ответ от сервера:', response);
    return response.data;
  } catch (error) {
    console.error('Ошибка при авторизации:', error);
    
    // Проверяем, если ошибка связана с редиректом (код 307)
    const axiosError = error as any;
    if (axiosError.response && axiosError.response.status === 307) {
      console.log('Получен редирект 307, пробуем отправить запрос на URL со слешем');
      // Пробуем отправить запрос на URL со слешем
      try {
        const urlWithSlash = `${API_URL}/login/access-token/`;
        console.log(`Повторная отправка запроса на ${urlWithSlash}`);
        const response = await axios.post<LoginResponse>(
          urlWithSlash,
          formData,
          {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            },
            maxRedirects: 0
          }
        );
        console.log('Успешный ответ от сервера после повторной попытки:', response);
        return response.data;
      } catch (retryError) {
        console.error('Ошибка при повторной попытке:', retryError);
        throw retryError;
      }
    }
    
    throw error;
  }
};

/**
 * Получает информацию о текущем пользователе
 * @returns Информация о пользователе
 */
export const getCurrentUser = async () => {
  const response = await apiClient.get(`/users/me`);
  return response.data;
}; 