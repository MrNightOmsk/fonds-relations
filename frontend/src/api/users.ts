import { useApiClient } from '@/composables/useApiClient';
import type { User, CreateUserRequest, UpdateUserRequest } from '@/types/models';

export function useUsersApi() {
  const api = useApiClient();
  const baseUrl = '/api/v1/users';

  const getUsers = async (): Promise<User[]> => {
    try {
      const response = await api.get(baseUrl);
      return response.data;
    } catch (error) {
      console.error('Ошибка при получении пользователей:', error);
      throw error;
    }
  };

  const getUserById = async (id: string): Promise<User> => {
    try {
      const response = await api.get(`${baseUrl}/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Ошибка при получении пользователя ${id}:`, error);
      throw error;
    }
  };

  const createUser = async (userData: CreateUserRequest): Promise<User> => {
    try {
      const response = await api.post(baseUrl, userData);
      return response.data;
    } catch (error) {
      console.error('Ошибка при создании пользователя:', error);
      throw error;
    }
  };

  const updateUser = async (id: string, userData: UpdateUserRequest): Promise<User> => {
    try {
      const response = await api.put(`${baseUrl}/${id}`, userData);
      return response.data;
    } catch (error) {
      console.error(`Ошибка при обновлении пользователя ${id}:`, error);
      throw error;
    }
  };

  const deleteUser = async (id: string): Promise<void> => {
    try {
      await api.delete(`${baseUrl}/${id}`);
    } catch (error) {
      console.error(`Ошибка при удалении пользователя ${id}:`, error);
      throw error;
    }
  };

  const toggleUserStatus = async (id: string, isActive: boolean): Promise<User> => {
    try {
      const response = await api.patch(`${baseUrl}/${id}/status`, { is_active: isActive });
      return response.data;
    } catch (error) {
      console.error(`Ошибка при изменении статуса пользователя ${id}:`, error);
      throw error;
    }
  };

  return {
    getUsers,
    getUserById,
    createUser,
    updateUser,
    deleteUser,
    toggleUserStatus
  };
} 