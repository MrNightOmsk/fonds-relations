import axios from 'axios';

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

  const response = await axios.post<LoginResponse>(`${API_URL}/login/access-token`, formData);
  return response.data;
};

/**
 * Получает информацию о текущем пользователе
 * @param token JWT токен
 * @returns Информация о пользователе
 */
export const getCurrentUser = async (token: string) => {
  const response = await axios.get(`${API_URL}/users/me`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return response.data;
}; 