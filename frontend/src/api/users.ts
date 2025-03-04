import { useApiClient } from '@/composables/useApiClient';
import type { User } from '@/types/models';

export function useUsersApi() {
  const api = useApiClient();
  const baseUrl = '/users';

  return {
    /**
     * Получить список всех пользователей
     */
    async getUsers() {
      try {
        console.log('Запрос списка пользователей: ' + baseUrl);
        const response = await api.get<User[]>(baseUrl);
        return response.data;
      } catch (error) {
        console.error('Ошибка при получении списка пользователей:', error);
        throw error;
      }
    },

    /**
     * Получить пользователя по ID
     */
    async getUserById(id: number) {
      try {
        const response = await api.get<User>(`${baseUrl}/${id}`);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при получении пользователя с ID ${id}:`, error);
        throw error;
      }
    },

    /**
     * Создать нового пользователя
     */
    async createUser(userData: any) {
      try {
        const response = await api.post<User>(baseUrl, userData);
        return response.data;
      } catch (error) {
        console.error('Ошибка при создании пользователя:', error);
        throw error;
      }
    },

    /**
     * Обновить данные пользователя
     */
    async updateUser(id: number, userData: any) {
      try {
        const response = await api.put<User>(`${baseUrl}/${id}`, userData);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при обновлении пользователя с ID ${id}:`, error);
        throw error;
      }
    },

    /**
     * Удалить пользователя
     */
    async deleteUser(id: number) {
      try {
        const response = await api.delete<{ success: boolean }>(`${baseUrl}/${id}`);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при удалении пользователя с ID ${id}:`, error);
        throw error;
      }
    },

    /**
     * Изменить статус активности пользователя
     */
    async toggleUserStatus(id: number, isActive: boolean) {
      try {
        const response = await api.patch<User>(`${baseUrl}/${id}/toggle-status`, { is_active: isActive });
        return response.data;
      } catch (error) {
        console.error(`Ошибка при изменении статуса пользователя с ID ${id}:`, error);
        throw error;
      }
    }
  };
} 