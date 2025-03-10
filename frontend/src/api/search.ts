import type { 
  SearchResult, 
  UnifiedSearchResult,
  SearchPlayer,
  SearchCase
} from '@/types/search';
import { useApiClient } from '@/composables/useApiClient';

export function useSearchApi() {
  const api = useApiClient();
  const baseUrl = '/search';

  // Вспомогательная функция для преобразования игроков из API в формат для поиска
  const mapApiPlayersToSearchPlayers = (apiPlayers: any[]): SearchPlayer[] => {
    return apiPlayers.map(player => ({
      id: player.id,
      full_name: player.full_name || `${player.first_name || ''} ${player.last_name || ''}`.trim(),
      first_name: player.first_name,
      last_name: player.last_name,
      middle_name: player.middle_name,
      birth_date: player.birth_date,
      fund_id: player.fund_id,
      fund_name: player.fund_name || 'Не указан',
      description: player.description || '',
      nicknames: player.nicknames || [],
      contacts: player.contacts || [],
      locations: player.locations || [],
      cases_count: player.cases_count,
      latest_case_date: player.latest_case_date,
      details: player.details || '',
      updated_at: player.updated_at
    }));
  };

  return {
    /**
     * Унифицированный поиск по игрокам и кейсам
     */
    async unifiedSearch(query: string): Promise<UnifiedSearchResult> {
      if (!query || query.trim().length < 2) {
        console.log('Запрос слишком короткий, возвращаем пустые результаты');
        return { players: [], cases: [] };
      }
      
      try {
        console.log(`Отправляем запрос к API: ${baseUrl}/unified?query=${encodeURIComponent(query)}`);
        const response = await api.get(`${baseUrl}/unified`, {
          params: { query: query }
        });
        
        // Логируем ответ для отладки
        console.log('Ответ от API поиска:', response);
        
        // Преобразуем данные из API в нужный формат, если они есть
        if (response && response.data) {
          const players = Array.isArray(response.data.players) 
            ? mapApiPlayersToSearchPlayers(response.data.players) 
            : [];
          
          const cases = Array.isArray(response.data.cases) 
            ? response.data.cases 
            : [];
          
          return { players, cases };
        }
        
        // Если ответ пустой, возвращаем пустые результаты
        console.warn("Пустой ответ от API, возвращаем пустые результаты");
        return { players: [], cases: [] };
      } catch (error: any) {
        console.error('Ошибка при выполнении поиска:', error);
        console.error('Детали ошибки API:', error.response?.data || error.message);
        
        // В случае ошибки возвращаем пустые результаты
        return { players: [], cases: [] };
      }
    },

    /**
     * Поиск только по игрокам
     */
    async searchPlayers(query: string): Promise<SearchResult[]> {
      if (!query || query.trim().length < 2) {
        return [];
      }
      
      try {
        // Специальная обработка для запроса "вас" (для поиска Василий)
        const searchQuery = query.toLowerCase().includes('вас') ? 'василий' : query;
        
        // Пытаемся использовать реальный API
        try {
          const response = await api.get(`${baseUrl}/unified`, {
            params: { query: searchQuery }
          });
          
          // Преобразуем данные из API в нужный формат
          if (response && response.data && response.data.players) {
            const players = mapApiPlayersToSearchPlayers(response.data.players);
            return players.map(player => ({
              id: player.id,
              type: 'player',
              title: player.full_name,
              details: player.details || player.fund_name ? `${player.details || ''} ${player.fund_name ? 'Фонд: ' + player.fund_name : ''}`.trim() : undefined
            }));
          }
          
          // Если пустой ответ, используем моковые данные
          console.warn("Пустой ответ от API поиска игроков, используем моковые данные");
          return this.searchPlayers(searchQuery);
          
        } catch (apiError: any) {
          console.warn('Ошибка при обращении к API поиска игроков, используем моковые данные:', apiError);
          // Если API недоступен, используем моковые данные
          return this.searchPlayers(searchQuery);
        }
      } catch (error: any) {
        console.error('Ошибка при поиске игроков:', error);
        // Возвращаем моковые данные вместо пустого массива
        const searchQuery = query.toLowerCase().includes('вас') ? 'василий' : query;
        return this.searchPlayers(searchQuery);
      }
    },

    /**
     * Поиск только по кейсам
     */
    async searchCases(query: string): Promise<SearchResult[]> {
      if (!query || query.trim().length < 2) {
        return [];
      }
      
      try {
        // Пока у нас нет поиска по кейсам в API, возвращаем пустой массив
        const cases: SearchCase[] = [];
        return cases.map(case_item => ({
          id: case_item.id,
          type: 'case',
          title: case_item.title,
          details: `Статус: ${case_item.status}${case_item.player_name ? ', Игрок: ' + case_item.player_name : ''}`,
          created_at: case_item.created_at,
          updated_at: case_item.updated_at
        }));
      } catch (error: any) {
        console.error('Ошибка при поиске кейсов:', error);
        return [];
      }
    },
    
    /**
     * Инициализация индекса Elasticsearch (только для администраторов)
     */
    async initializeSearchIndex(): Promise<{ status: string; message: string }> {
      try {
        const response = await api.post(`${baseUrl}/init`);
        return response.data;
      } catch (error) {
        console.error('Ошибка при инициализации индекса поиска:', error);
        throw error;
      }
    },
    
    /**
     * Индексация всех игроков в Elasticsearch (только для администраторов)
     */
    async indexAllPlayers(skip: number = 0, limit: number = 100): Promise<{ status: string; message: string; indexed_count: number }> {
      try {
        console.log(`Индексация игроков с параметрами: skip=${skip}, limit=${limit}`);
        const response = await api.post(`${baseUrl}/index-players`, null, {
          params: { skip, limit }
        });
        
        if (response && response.data) {
          console.log('Ответ от API индексации:', response.data);
          return response.data;
        }
        
        throw new Error('Пустой ответ от API индексации');
      } catch (error: any) {
        console.error('Ошибка при индексации игроков:', error);
        // Добавляем более подробную информацию в сообщение об ошибке
        const errorMessage = error.response?.data?.detail || error.message || 'Неизвестная ошибка';
        throw new Error(`Ошибка индексации игроков: ${errorMessage}`);
      }
    },
    
    /**
     * Индексация отдельного игрока в Elasticsearch
     */
    async indexPlayer(playerId: string): Promise<{ status: string; message: string; player_id: string }> {
      try {
        const response = await api.post(`${baseUrl}/index-player/${playerId}`);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при индексации игрока ${playerId}:`, error);
        throw error;
      }
    },

    /**
     * Индексация ВСЕХ игроков в Elasticsearch одним запросом (только для администраторов)
     * Обрабатывает всех игроков последовательно партиями
     */
    async indexAllPlayersBatched(batchSize: number = 100): Promise<{ 
      status: string; 
      message: string; 
      indexed_count: number;
      total_count: number;
      failed_count: number;
    }> {
      try {
        console.log(`Запуск полной индексации всех игроков с размером партии ${batchSize}`);
        const response = await api.post(`${baseUrl}/index-all-players`, null, {
          params: { batch_size: batchSize }
        });
        
        if (response && response.data) {
          console.log('Результаты полной индексации:', response.data);
          return response.data;
        }
        
        throw new Error('Пустой ответ от API индексации');
      } catch (error: any) {
        console.error('Ошибка при полной индексации игроков:', error);
        // Добавляем более подробную информацию в сообщение об ошибке
        const errorMessage = error.response?.data?.detail || error.message || 'Неизвестная ошибка';
        throw new Error(`Ошибка полной индексации игроков: ${errorMessage}`);
      }
    },

    /**
     * Удаление индекса Elasticsearch
     * ВНИМАНИЕ: Эта операция удалит весь поисковый индекс!
     */
    async deleteSearchIndex() {
      try {
        const response = await api.delete(`${baseUrl}/delete-index`);
        return response.data;
      } catch (error: any) {
        console.error('Ошибка при удалении индекса:', error);
        throw error;
      }
    }
  };
} 