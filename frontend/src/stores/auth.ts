import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { jwtDecode } from 'jwt-decode';
import router from '@/router';
import { login as apiLogin } from '@/api/auth';

interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  fund_id: string;
}

interface LoginCredentials {
  username: string;
  password: string;
}

interface JwtPayload {
  sub: string;
  exp: number;
  fund_id: string;
  role: string;
}

export const useAuthStore = defineStore('auth', () => {
  // Состояние
  const token = ref<string | null>(localStorage.getItem('token'));
  const user = ref<User | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Геттеры
  const isAuthenticated = computed(() => !!token.value);
  
  const isAdmin = computed(() => {
    try {
      // Прямая проверка токена для определения роли администратора
      if (!token.value) return false;
      
      const decoded = jwtDecode<JwtPayload>(token.value);
      console.log('isAdmin проверка, токен:', token.value);
      console.log('isAdmin проверка, декодированный токен:', decoded);
      console.log('isAdmin проверка, роль:', decoded.role);
      
      return decoded.role === 'admin';
    } catch (e) {
      console.error('Ошибка при проверке роли администратора:', e);
      return false;
    }
  });

  // Инициализация пользователя из токена
  const initializeFromToken = () => {
    if (token.value) {
      try {
        console.log('Инициализация из токена:', token.value);
        const decoded = jwtDecode<JwtPayload>(token.value);
        console.log('Декодированный токен:', decoded);
        
        // Проверка срока действия токена
        const currentTime = Date.now() / 1000;
        if (decoded.exp < currentTime) {
          // Токен истек
          console.log('Токен истек');
          logout();
          return;
        }
        
        // Создаем объект пользователя из данных токена
        user.value = {
          id: decoded.sub,
          email: '', // Эти поля в токене отсутствуют
          full_name: '',
          role: decoded.role,
          fund_id: decoded.fund_id
        };
        
        console.log('Пользователь инициализирован:', user.value);
        console.log('Роль пользователя в токене:', decoded.role);
        console.log('isAdmin вернет:', decoded.role === 'admin');
      } catch (e) {
        console.error('Ошибка декодирования токена:', e);
        logout();
      }
    } else {
      console.log('Токен отсутствует');
    }
  };

  // Вызываем инициализацию при создании хранилища
  initializeFromToken();

  // Действия
  const login = async (credentials: LoginCredentials) => {
    loading.value = true;
    error.value = null;
    
    try {
      console.log('Попытка входа с учетными данными:', credentials.username);
      const response = await apiLogin(credentials);
      console.log('Получен ответ от API:', response);
      token.value = response.access_token;
      localStorage.setItem('token', response.access_token);
      console.log('Токен сохранен в localStorage');
      initializeFromToken();
      router.push('/dashboard');
    } catch (e: any) {
      console.error('Ошибка входа:', e);
      error.value = e.response?.data?.detail || 'Ошибка аутентификации';
    } finally {
      loading.value = false;
    }
  };

  const logout = () => {
    console.log('Выход из системы');
    token.value = null;
    user.value = null;
    localStorage.removeItem('token');
    router.push('/login');
  };

  return {
    token,
    user,
    loading,
    error,
    isAuthenticated,
    isAdmin,
    login,
    logout
  };
}); 