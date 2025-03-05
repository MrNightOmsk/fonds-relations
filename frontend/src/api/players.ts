import type { 
  Player, 
  CreatePlayerRequest, 
  UpdatePlayerRequest,
  PlayerPaymentMethod,
  PlayerSocialMedia
} from '@/types/models';
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
    async getPlayerById(id: string) {
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
    async createPlayer(playerData: CreatePlayerRequest) {
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
    async updatePlayer(id: string, playerData: UpdatePlayerRequest) {
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
    async deletePlayer(id: string) {
      try {
        const response = await api.delete<{ success: boolean }>(`${baseUrl}/${id}`);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при удалении игрока с ID ${id}:`, error);
        throw error;
      }
    },

    /**
     * Получить методы оплаты игрока
     */
    async getPlayerPaymentMethods(playerId: string) {
      try {
        const response = await api.get<PlayerPaymentMethod[]>(`${baseUrl}/${playerId}/payment-methods`);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при получении методов оплаты игрока с ID ${playerId}:`, error);
        throw error;
      }
    },

    /**
     * Добавить метод оплаты игрока
     */
    async addPlayerPaymentMethod(playerId: string, paymentMethodData: Partial<PlayerPaymentMethod>) {
      try {
        const response = await api.post<PlayerPaymentMethod>(
          `${baseUrl}/${playerId}/payment-methods`, 
          paymentMethodData
        );
        return response.data;
      } catch (error) {
        console.error(`Ошибка при добавлении метода оплаты игроку с ID ${playerId}:`, error);
        throw error;
      }
    },

    /**
     * Удалить метод оплаты игрока
     */
    async deletePlayerPaymentMethod(playerId: string, paymentMethodId: string) {
      try {
        const response = await api.delete<{ success: boolean }>(
          `${baseUrl}/${playerId}/payment-methods/${paymentMethodId}`
        );
        return response.data;
      } catch (error) {
        console.error(`Ошибка при удалении метода оплаты игрока:`, error);
        throw error;
      }
    },

    /**
     * Получить социальные сети игрока
     */
    async getPlayerSocialMedia(playerId: string) {
      try {
        const response = await api.get<PlayerSocialMedia[]>(`${baseUrl}/${playerId}/social-media`);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при получении социальных сетей игрока с ID ${playerId}:`, error);
        throw error;
      }
    },

    /**
     * Добавить социальную сеть игрока
     */
    async addPlayerSocialMedia(playerId: string, socialMediaData: Partial<PlayerSocialMedia>) {
      try {
        const response = await api.post<PlayerSocialMedia>(
          `${baseUrl}/${playerId}/social-media`, 
          socialMediaData
        );
        return response.data;
      } catch (error) {
        console.error(`Ошибка при добавлении социальной сети игроку с ID ${playerId}:`, error);
        throw error;
      }
    },

    /**
     * Удалить социальную сеть игрока
     */
    async deletePlayerSocialMedia(playerId: string, socialMediaId: string) {
      try {
        const response = await api.delete<{ success: boolean }>(
          `${baseUrl}/${playerId}/social-media/${socialMediaId}`
        );
        return response.data;
      } catch (error) {
        console.error(`Ошибка при удалении социальной сети игрока:`, error);
        throw error;
      }
    }
  };
} 