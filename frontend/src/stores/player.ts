import { defineStore } from 'pinia';
import { usePlayersApi } from '@/api/players';
import type { 
  Player, 
  CreatePlayerRequest, 
  UpdatePlayerRequest, 
  PlayerPaymentMethod, 
  PlayerSocialMedia 
} from '@/types/models';

export const usePlayerStore = defineStore('player', {
  state: () => ({
    players: [] as Player[],
    currentPlayer: null as Player | null,
    loading: false,
    error: null as string | null
  }),

  getters: {
    getPlayerById: (state) => (id: string) => {
      return state.players.find(player => player.id === id);
    },
    getPlayersByFund: (state) => (fundId: string) => {
      return state.players.filter(player => player.created_by_fund_id === fundId);
    }
  },

  actions: {
    async fetchPlayers() {
      this.loading = true;
      this.error = null;
      try {
        const api = usePlayersApi();
        const players = await api.getPlayers();
        this.players = players;
      } catch (error) {
        console.error('Ошибка при загрузке игроков:', error);
        this.error = 'Не удалось загрузить игроков';
      } finally {
        this.loading = false;
      }
    },

    async fetchPlayer(id: string) {
      this.loading = true;
      this.error = null;
      try {
        const api = usePlayersApi();
        const player = await api.getPlayerById(id);
        this.currentPlayer = player;
        
        // Обновляем игрока в общем списке, если он там есть
        const index = this.players.findIndex(p => p.id === id);
        if (index !== -1) {
          this.players[index] = player;
        }
        
        return player;
      } catch (error) {
        console.error(`Ошибка при загрузке игрока с ID ${id}:`, error);
        this.error = 'Не удалось загрузить игрока';
        return null;
      } finally {
        this.loading = false;
      }
    },

    async createPlayer(playerData: CreatePlayerRequest) {
      this.loading = true;
      this.error = null;
      try {
        const api = usePlayersApi();
        const player = await api.createPlayer(playerData);
        this.players.push(player);
        return player;
      } catch (error) {
        console.error('Ошибка при создании игрока:', error);
        this.error = 'Не удалось создать игрока';
        return null;
      } finally {
        this.loading = false;
      }
    },

    async updatePlayer(id: string, playerData: UpdatePlayerRequest) {
      this.loading = true;
      this.error = null;
      try {
        const api = usePlayersApi();
        const player = await api.updatePlayer(id, playerData);
        
        // Обновляем игрока в общем списке
        const index = this.players.findIndex(p => p.id === id);
        if (index !== -1) {
          this.players[index] = player;
        }
        
        // Обновляем currentPlayer, если это он
        if (this.currentPlayer && this.currentPlayer.id === id) {
          this.currentPlayer = player;
        }
        
        return player;
      } catch (error) {
        console.error(`Ошибка при обновлении игрока с ID ${id}:`, error);
        this.error = 'Не удалось обновить игрока';
        return null;
      } finally {
        this.loading = false;
      }
    },

    async deletePlayer(id: string) {
      this.loading = true;
      this.error = null;
      try {
        const api = usePlayersApi();
        await api.deletePlayer(id);
        
        // Удаляем игрока из списка
        this.players = this.players.filter(player => player.id !== id);
        
        // Сбрасываем currentPlayer, если это был он
        if (this.currentPlayer && this.currentPlayer.id === id) {
          this.currentPlayer = null;
        }
        
        return true;
      } catch (error) {
        console.error(`Ошибка при удалении игрока с ID ${id}:`, error);
        this.error = 'Не удалось удалить игрока';
        return false;
      } finally {
        this.loading = false;
      }
    },

    // Методы для работы с методами оплаты
    async fetchPlayerPaymentMethods(playerId: string) {
      try {
        const api = usePlayersApi();
        return await api.getPlayerPaymentMethods(playerId);
      } catch (error) {
        console.error(`Ошибка при загрузке методов оплаты игрока с ID ${playerId}:`, error);
        throw error;
      }
    },

    async addPlayerPaymentMethod(playerId: string, data: Partial<PlayerPaymentMethod>) {
      try {
        const api = usePlayersApi();
        const paymentMethod = await api.addPlayerPaymentMethod(playerId, data);
        
        // Обновляем список методов оплаты в текущем игроке, если он загружен
        if (this.currentPlayer && this.currentPlayer.id === playerId) {
          if (!this.currentPlayer.payment_methods) {
            this.currentPlayer.payment_methods = [];
          }
          this.currentPlayer.payment_methods.push(paymentMethod);
        }
        
        return paymentMethod;
      } catch (error) {
        console.error(`Ошибка при добавлении метода оплаты для игрока с ID ${playerId}:`, error);
        throw error;
      }
    },

    async deletePlayerPaymentMethod(playerId: string, paymentMethodId: string) {
      try {
        const api = usePlayersApi();
        await api.deletePlayerPaymentMethod(playerId, paymentMethodId);
        
        // Удаляем метод оплаты из списка в текущем игроке, если он загружен
        if (this.currentPlayer && this.currentPlayer.id === playerId && this.currentPlayer.payment_methods) {
          this.currentPlayer.payment_methods = this.currentPlayer.payment_methods.filter(
            pm => pm.id !== paymentMethodId
          );
        }
        
        return true;
      } catch (error) {
        console.error(`Ошибка при удалении метода оплаты с ID ${paymentMethodId} для игрока ${playerId}:`, error);
        throw error;
      }
    },

    // Методы для работы с социальными сетями
    async fetchPlayerSocialMedia(playerId: string) {
      try {
        const api = usePlayersApi();
        return await api.getPlayerSocialMedia(playerId);
      } catch (error) {
        console.error(`Ошибка при загрузке социальных сетей игрока с ID ${playerId}:`, error);
        throw error;
      }
    },

    async addPlayerSocialMedia(playerId: string, data: Partial<PlayerSocialMedia>) {
      try {
        const api = usePlayersApi();
        const socialMedia = await api.addPlayerSocialMedia(playerId, data);
        
        // Обновляем список социальных сетей в текущем игроке, если он загружен
        if (this.currentPlayer && this.currentPlayer.id === playerId) {
          if (!this.currentPlayer.social_media) {
            this.currentPlayer.social_media = [];
          }
          this.currentPlayer.social_media.push(socialMedia);
        }
        
        return socialMedia;
      } catch (error) {
        console.error(`Ошибка при добавлении социальной сети для игрока с ID ${playerId}:`, error);
        throw error;
      }
    },

    async deletePlayerSocialMedia(playerId: string, socialMediaId: string) {
      try {
        const api = usePlayersApi();
        await api.deletePlayerSocialMedia(playerId, socialMediaId);
        
        // Удаляем социальную сеть из списка в текущем игроке, если он загружен
        if (this.currentPlayer && this.currentPlayer.id === playerId && this.currentPlayer.social_media) {
          this.currentPlayer.social_media = this.currentPlayer.social_media.filter(
            sm => sm.id !== socialMediaId
          );
        }
        
        return true;
      } catch (error) {
        console.error(`Ошибка при удалении социальной сети с ID ${socialMediaId} для игрока ${playerId}:`, error);
        throw error;
      }
    }
  }
}); 