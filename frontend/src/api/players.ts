import type { 
  Player, 
  CreatePlayerRequest, 
  UpdatePlayerRequest,
  PlayerPaymentMethod,
  PlayerSocialMedia
} from '@/types/models';
import { useApiClient } from '@/composables/useApiClient';

// Моковые данные для демонстрации
const mockPlayers: Player[] = [
  {
    id: '1',
    full_name: 'Иванов Иван',
    first_name: 'Иван',
    last_name: 'Иванов',
    phone: '+71234567890',
    status: 'active',
    created_at: '2023-01-15T12:00:00Z',
    updated_at: '2023-01-15T12:00:00Z'
  },
  {
    id: '2',
    full_name: 'Петров Петр',
    first_name: 'Петр',
    last_name: 'Петров',
    status: 'active',
    created_at: '2023-01-20T15:30:00Z',
    updated_at: '2023-01-20T15:30:00Z'
  },
  {
    id: '3',
    full_name: 'Сидоров Сидор',
    first_name: 'Сидор',
    last_name: 'Сидоров',
    status: 'inactive',
    created_at: '2023-01-25T10:00:00Z',
    updated_at: '2023-01-25T10:00:00Z'
  }
];

export function usePlayersApi() {
  const api = useApiClient();
  const baseUrl = '/players';

  return {
    /**
     * Получить список всех игроков
     */
    async getPlayers(): Promise<Player[]> {
      try {
        // В моковом режиме возвращаем локальные данные
        if (import.meta.env.DEV) {
          console.log('Using mock data for getPlayers');
          return [...mockPlayers];
        }
        
        // В реальном режиме используем API
        const response = await api.get<Player[]>(baseUrl);
        return response.data;
      } catch (error) {
        console.error('Ошибка при получении списка игроков:', error);
        throw error;
      }
    },

    /**
     * Получить игроков с поддержкой пагинации, поиска и фильтрации
     * @param params Параметры запроса (skip, limit, search и др.)
     * @returns Объект с результатами и общим количеством
     */
    async getAccessiblePlayers(params?: any): Promise<{ results: Player[], count: number }> {
      try {
        // Настраиваем параметры запроса
        const requestParams = { ...params };
        
        // Если не указан лимит, устанавливаем значение по умолчанию
        if (!requestParams.limit && requestParams.limit !== 0) {
          requestParams.limit = 12; // Значение по умолчанию для игроков
        }
        
        // Убеждаемся, что параметр skip является числом
        if (requestParams.skip !== undefined) {
          requestParams.skip = Number(requestParams.skip);
        }
        
        console.log('Запрос на получение игроков с параметрами:', JSON.stringify(requestParams));
        console.log('URL запроса:', `${baseUrl}?${new URLSearchParams(requestParams).toString()}`);
        
        // Получаем игроков с учетом параметров
        let response;
        try {
          response = await api.get(baseUrl, { params: requestParams });
          console.log('Статус ответа API:', response.status);
          console.log('Тип данных в ответе:', typeof response.data);
          console.log('Получен ответ от API игроков:', 
            Array.isArray(response.data) 
              ? `[Array с ${response.data.length} элементами]` 
              : JSON.stringify(response.data).substring(0, 200) + '...');
        } catch (networkError) {
          console.error('Ошибка сети при получении игроков:', networkError);
          
          if (networkError.response) {
            console.error('Статус ответа:', networkError.response.status);
            console.error('Тело ответа:', JSON.stringify(networkError.response.data).substring(0, 500));
          } else if (networkError.request) {
            console.error('Запрос был отправлен, но ответ не получен');
          } else {
            console.error('Ошибка при настройке запроса:', networkError.message);
          }
          
          // В случае ошибки сети возвращаем пустые данные
          return { results: [], count: 0 };
        }
        
        // Логируем структуру ответа для отладки
        console.log('Структура ответа API:', 
          Array.isArray(response.data) 
            ? 'Array' 
            : Object.keys(response.data).join(', '));
        
        // Если API возвращает массив, преобразуем в нужный формат
        if (Array.isArray(response.data)) {
          console.log('API вернул массив игроков напрямую, конвертируем в ожидаемый формат');
          return {
            results: response.data,
            count: response.headers['x-total-count'] 
              ? parseInt(response.headers['x-total-count'], 10) 
              : response.data.length
          };
        }
        
        // Если API возвращает объект с полями results и count
        if (response.data.results && response.data.count !== undefined) {
          console.log('API вернул объект с полями results и count');
          return {
            results: response.data.results,
            count: response.data.count
          };
        }
        
        // Если API возвращает объект с полями items и total
        if (response.data.items && response.data.total !== undefined) {
          console.log('API вернул объект с полями items и total');
          return {
            results: response.data.items,
            count: response.data.total
          };
        }
        
        // Для других форматов ответа - логируем и возвращаем безопасное значение
        console.warn('API игроков вернул неожиданный формат данных:', JSON.stringify(response.data).substring(0, 200));
        return {
          results: Array.isArray(response.data) ? response.data : [],
          count: Array.isArray(response.data) ? response.data.length : 0
        };
      } catch (error) {
        console.error('Критическая ошибка при получении игроков:', error);
        if (error instanceof Error) {
          console.error('Сообщение ошибки:', error.message);
          console.error('Стек ошибки:', error.stack);
        }
        return { results: [], count: 0 };
      }
    },

    /**
     * Получить игрока по ID
     */
    async getPlayerById(id: string): Promise<Player> {
      try {
        // В моковом режиме возвращаем локальные данные
        if (import.meta.env.DEV) {
          console.log('Using mock data for getPlayerById', id);
          const player = mockPlayers.find(p => p.id === id);
          if (!player) {
            throw new Error(`Игрок с ID ${id} не найден`);
          }
          return { ...player };
        }
        
        // В реальном режиме используем API
        console.log(`Отправка запроса к API: GET ${baseUrl}/${id}`);
        const response = await api.get<Player>(`${baseUrl}/${id}`);
        console.log(`Получен ответ от API для игрока ${id}:`, response.data);
        
        // Проверяем структуру полученных данных
        if (!response.data) {
          console.error('API вернул пустой ответ');
          throw new Error('Пустой ответ от сервера');
        }
        
        // Проверяем наличие необходимых полей
        console.log('Проверка полей игрока:');
        console.log('- first_name:', response.data.first_name);
        console.log('- last_name:', response.data.last_name);
        console.log('- full_name:', response.data.full_name);
        console.log('- nicknames:', response.data.nicknames?.length || 0, 'шт.');
        console.log('- contacts:', response.data.contacts?.length || 0, 'шт.');
        console.log('- locations:', response.data.locations?.length || 0, 'шт.');
        
        // Специальная проверка никнеймов
        if (response.data.nicknames === undefined) {
          console.warn('ВНИМАНИЕ! Поле nicknames отсутствует в ответе API');
          // Создаем пустой массив никнеймов, если его нет в ответе
          response.data.nicknames = [];
        } else if (!Array.isArray(response.data.nicknames)) {
          console.error('ОШИБКА! Поле nicknames не является массивом:', response.data.nicknames);
          // Преобразуем в пустой массив
          response.data.nicknames = [];
        } else {
          console.log('Никнеймы в ответе API:', JSON.stringify(response.data.nicknames));
          // Проверяем структуру каждого никнейма
          for (const nickname of response.data.nicknames) {
            if (!nickname.nickname) {
              console.warn('ВНИМАНИЕ! Найден некорректный никнейм без поля nickname:', nickname);
            }
          }
        }
        
        // Делаем копию данных, чтобы избежать проблем с реактивностью
        return { ...response.data };
      } catch (error) {
        console.error(`Ошибка при получении игрока с ID ${id}:`, error);
        throw error;
      }
    },

    /**
     * Создать нового игрока
     */
    async createPlayer(playerData: CreatePlayerRequest): Promise<Player> {
      try {
        // В моковом режиме симулируем создание
        if (import.meta.env.DEV) {
          console.log('Using mock data for createPlayer', playerData);
          const newPlayer: Player = {
            id: Date.now().toString(),
            full_name: `${playerData.first_name} ${playerData.last_name}`,
            first_name: playerData.first_name,
            last_name: playerData.last_name,
            phone: playerData.phone,
            status: playerData.status || 'active',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
          };
          
          mockPlayers.push(newPlayer);
          return { ...newPlayer };
        }
        
        // В реальном режиме используем API
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
    async updatePlayer(id: string, playerData: UpdatePlayerRequest): Promise<Player> {
      try {
        // В моковом режиме симулируем обновление
        if (import.meta.env.DEV) {
          console.log('Using mock data for updatePlayer', id, playerData);
          const index = mockPlayers.findIndex(p => p.id === id);
          
          if (index === -1) {
            throw new Error(`Игрок с ID ${id} не найден`);
          }
          
          // Обновление full_name при изменении имени или фамилии
          let full_name = mockPlayers[index].full_name;
          if (playerData.first_name || playerData.last_name) {
            const first = playerData.first_name || mockPlayers[index].first_name;
            const last = playerData.last_name || mockPlayers[index].last_name;
            full_name = `${first} ${last}`;
          }
          
          const updatedPlayer = {
            ...mockPlayers[index],
            ...playerData,
            full_name,
            updated_at: new Date().toISOString()
          };
          
          mockPlayers[index] = updatedPlayer;
          return { ...updatedPlayer };
        }
        
        // В реальном режиме используем API
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
    async deletePlayer(id: string): Promise<void> {
      try {
        // В моковом режиме симулируем удаление
        if (import.meta.env.DEV) {
          console.log('Using mock data for deletePlayer', id);
          const index = mockPlayers.findIndex(p => p.id === id);
          
          if (index === -1) {
            throw new Error(`Игрок с ID ${id} не найден`);
          }
          
          mockPlayers.splice(index, 1);
          return;
        }
        
        // В реальном режиме используем API
        await api.delete(`${baseUrl}/${id}`);
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
    },

    /**
     * Получить количество игроков в системе
     */
    async getPlayersCount(): Promise<{ count: number }> {
      try {
        // Используем API с limit=0 для получения только count без данных
        const response = await api.get(baseUrl, { params: { limit: 0 } });
        
        // Проверяем формат ответа API
        if (response.data && typeof response.data.count === 'number') {
          return { count: response.data.count };
        } else if (Array.isArray(response.data)) {
          // Если API возвращает массив, количество равно длине массива
          return { count: response.data.length };
        }
        
        // В случае других форматов возвращаем 0
        return { count: 0 };
      } catch (error) {
        console.error('Ошибка при получении количества игроков:', error);
        return { count: 0 };
      }
    }
  };
} 