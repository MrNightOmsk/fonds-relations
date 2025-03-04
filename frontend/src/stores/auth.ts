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
  user: User;
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
    return user.value?.role === 'admin';
  });

  // Инициализация пользователя из токена
  const initializeFromToken = () => {
    if (token.value) {
      try {
        const decoded = jwtDecode<JwtPayload>(token.value);
        
        // Проверка срока действия токена
        const currentTime = Date.now() / 1000;
        if (decoded.exp < currentTime) {
          // Токен истек
          logout();
          return;
        }
        
        user.value = decoded.user;
      } catch (e) {
        console.error('Ошибка декодирования токена:', e);
        logout();
      }
    }
  };

  // Вызываем инициализацию при создании хранилища
  initializeFromToken();

  // Действия
  const login = async (credentials: LoginCredentials) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await apiLogin(credentials);
      token.value = response.access_token;
      localStorage.setItem('token', response.access_token);
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