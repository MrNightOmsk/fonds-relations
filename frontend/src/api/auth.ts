import axios from 'axios';
import apiClient from './config';

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
  const formData = new FormData();
  formData.append('username', credentials.username);
  formData.append('password', credentials.password);

  // Для логина используем обычный axios, так как токена еще нет
  const response = await axios.post<LoginResponse>(`/api/v1/login/access-token`, formData);
  return response.data;
};

/**
 * Получает информацию о текущем пользователе
 * @returns Информация о пользователе
 */
export const getCurrentUser = async () => {
  const response = await apiClient.get(`/users/me`);
  return response.data;
}; 