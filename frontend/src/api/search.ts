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

  // Моковые данные для демонстрации (оставляем как запасной вариант)
  const getMockPlayers = (query: string): SearchPlayer[] => {
    const lowerQuery = query.toLowerCase();
    
    if (lowerQuery.includes('иван')) {
      return [
        { id: '1', full_name: 'Иванов Иван', details: 'Телефон: +7123456789', fund_name: 'Альфа Фонд' },
        { id: '2', full_name: 'Петров Иван', details: 'Email: ivan@example.com', fund_name: 'Бета Фонд' }
      ];
    } else if (lowerQuery.includes('петр')) {
      return [
        { id: '3', full_name: 'Петров Петр', details: 'Telegram: @petrov', fund_name: 'Гамма Фонд' }
      ];
    }
    
    return [];
  };
  
  const getMockCases = (query: string): SearchCase[] => {
    const lowerQuery = query.toLowerCase();
    
    if (lowerQuery.includes('скам')) {
      return [
        { 
          id: '101', 
          title: 'Скам игрока на форуме', 
          status: 'open',
          player_name: 'Иванов Иван',
          player_id: '1',
          fund_name: 'Альфа Фонд',
          created_at: '2023-03-01T10:30:00Z'
        }
      ];
    } else if (lowerQuery.includes('долг')) {
      return [
        { 
          id: '102', 
          title: 'Долг за онлайн игру', 
          status: 'closed',
          player_name: 'Петров Петр',
          player_id: '3',
          fund_name: 'Гамма Фонд',
          created_at: '2023-02-15T14:20:00Z'
        }
      ];
    }
    
    return [];
  };
  
  // Преобразование игроков из API в формат SearchPlayer
  const mapApiPlayersToSearchPlayers = (apiPlayers: any[]): SearchPlayer[] => {
    return apiPlayers.map(player => ({
      id: player.id,
      full_name: player.full_name,
      details: player.nicknames && player.nicknames.length > 0 
        ? `Никнеймы: ${player.nicknames.map((n: any) => `${n.nickname} (${n.room})`).join(', ')}` 
        : undefined,
      fund_name: player.fund_name
    }));
  };
  
  // Преобразование игроков в общий формат результатов поиска
  const playersToSearchResults = (players: SearchPlayer[]): SearchResult[] => {
    return players.map(player => ({
      id: player.id,
      type: 'player',
      title: player.full_name,
      details: player.details || player.fund_name ? `${player.details || ''} ${player.fund_name ? 'Фонд: ' + player.fund_name : ''}`.trim() : undefined
    }));
  };
  
  // Преобразование кейсов в общий формат результатов поиска
  const casesToSearchResults = (cases: SearchCase[]): SearchResult[] => {
    return cases.map(case_item => ({
      id: case_item.id,
      type: 'case',
      title: case_item.title,
      details: `Статус: ${case_item.status}${case_item.player_name ? ', Игрок: ' + case_item.player_name : ''}`,
      created_at: case_item.created_at,
      updated_at: case_item.updated_at
    }));
  };

  return {
    /**
     * Унифицированный поиск по игрокам и кейсам
     */
    async unifiedSearch(query: string): Promise<UnifiedSearchResult> {
      try {
        // Пытаемся использовать реальный API
        try {
          const response = await api.get(`${baseUrl}/unified`, {
            params: { query }
          });
          
          // Преобразуем данные из API в нужный формат
          const players = mapApiPlayersToSearchPlayers(response.data.players || []);
          
          // Пока у нас нет поиска по кейсам в API, используем моковые данные для кейсов
          const cases = getMockCases(query);
          
          return { players, cases };
        } catch (apiError) {
          console.warn('Ошибка при обращении к API поиска, используем моковые данные:', apiError);
          // Если API недоступен, используем моковые данные
          return {
            players: getMockPlayers(query),
            cases: getMockCases(query)
          };
        }
      } catch (error) {
        console.error('Ошибка при выполнении поиска:', error);
        // Возвращаем пустой результат в случае ошибки
        return { players: [], cases: [] };
      }
    },

    /**
     * Поиск только по игрокам
     */
    async searchPlayers(query: string): Promise<SearchResult[]> {
      try {
        // Пытаемся использовать реальный API
        try {
          const response = await api.get(`${baseUrl}/unified`, {
            params: { query }
          });
          
          // Преобразуем данные из API в нужный формат
          const players = mapApiPlayersToSearchPlayers(response.data.players || []);
          return playersToSearchResults(players);
        } catch (apiError) {
          console.warn('Ошибка при обращении к API поиска игроков, используем моковые данные:', apiError);
          // Если API недоступен, используем моковые данные
          const players = getMockPlayers(query);
          return playersToSearchResults(players);
        }
      } catch (error) {
        console.error('Ошибка при поиске игроков:', error);
        return [];
      }
    },

    /**
     * Поиск только по кейсам
     */
    async searchCases(query: string): Promise<SearchResult[]> {
      try {
        // Пока у нас нет поиска по кейсам в API, используем моковые данные
        const cases = getMockCases(query);
        return casesToSearchResults(cases);
      } catch (error) {
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
        const response = await api.post(`${baseUrl}/index-players`, null, {
          params: { skip, limit }
        });
        return response.data;
      } catch (error) {
        console.error('Ошибка при индексации игроков:', error);
        throw error;
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
    }
  };
} 