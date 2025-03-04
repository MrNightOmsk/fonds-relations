import type { Player, CreatePlayerRequest, UpdatePlayerRequest } from '@/types/models';
import { useApiClient } from '@/composables/useApiClient';

export function usePlayersApi() {
  const api = useApiClient();
  const baseUrl = '/players';

  return {
    /**
     * Получить список всех игроков
     */
    async getPlayers() {
      try {
        console.log('Запрос списка игроков: ' + baseUrl);
        const response = await api.get<Player[]>(baseUrl);
        return response.data;
      } catch (error) {
        console.error('Ошибка при получении списка игроков:', error);
        throw error;
      }
    },

    /**
     * Получить игрока по ID
     */
    async getPlayerById(id: number) {
      try {
        const response = await api.get<Player>(`${baseUrl}/${id}`);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при получении игрока с ID ${id}:`, error);
        throw error;
      }
    },

    /**
     * Создать нового игрока
     */
    async createPlayer(playerData: any) {
      try {
        const response = await api.post<Player>(baseUrl, playerData);
        return response.data;
      } catch (error) {
        console.error('Ошибка при создании игрока:', error);
        throw error;
      }
    },

    /**
     * Обновить данные игрока
     */
    async updatePlayer(id: number, playerData: any) {
      try {
        const response = await api.put<Player>(`${baseUrl}/${id}`, playerData);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при обновлении игрока с ID ${id}:`, error);
        throw error;
      }
    },

    /**
     * Удалить игрока
     */
    async deletePlayer(id: number) {
      try {
        const response = await api.delete<{ success: boolean }>(`${baseUrl}/${id}`);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при удалении игрока с ID ${id}:`, error);
        throw error;
      }
    }
  };
} 