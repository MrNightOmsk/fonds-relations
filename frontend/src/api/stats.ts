import { useApiClient } from '@/composables/useApiClient';

// Интерфейс для статистики Dashboard
export interface DashboardStats {
  players: {
    total: number;
    active?: number;
    inactive?: number;
  };
  cases: {
    total: number;
    open?: number;
    in_progress?: number;
    resolved?: number;
    closed?: number;
  };
  funds?: {
    total: number;
    active?: number;
  };
}

// Значения по умолчанию
const defaultDashboardStats: DashboardStats = {
  players: {
    total: 0,
    active: 0,
    inactive: 0
  },
  cases: {
    total: 0,
    open: 0,
    in_progress: 0,
    resolved: 0,
    closed: 0
  },
  funds: {
    total: 0,
    active: 0
  }
};

export function useStatsApi() {
  const api = useApiClient();
  const baseUrl = '/stats';

  return {
    /**
     * Получить статистику для Dashboard
     * @param scope - Область статистики: 'default', 'all', 'global', 'fund'
     */
    async getDashboardStats(scope: string = 'global'): Promise<DashboardStats> {
      try {
        // Сначала пробуем получить отладочные данные
        try {
          const debugResponse = await api.get(`${baseUrl}/dashboard-debug`);
          if (debugResponse.data) {
            console.log('Получены отладочные данные статистики:', debugResponse.data);
            return debugResponse.data;
          }
        } catch (debugError) {
          console.warn('Отладочная статистика недоступна, использую обычный API');
        }
        
        // Затем пробуем получить данные с обычного эндпоинта статистики
        const response = await api.get(`${baseUrl}/dashboard`, {
          params: { scope }
        });
        return response.data || defaultDashboardStats;
      } catch (error) {
        console.error('Ошибка при получении статистики Dashboard:', error);
        
        // Если эндпоинт недоступен, переходим к запасным вариантам
        return await this.getFallbackDashboardStats();
      }
    },
    
    /**
     * Запасной метод получения статистики, использующий несколько API
     */
    async getFallbackDashboardStats(): Promise<DashboardStats> {
      try {
        // Создаем базовую структуру статистики
        const stats: DashboardStats = {
          players: { total: 0 },
          cases: { total: 0 }
        };
        
        // Загружаем статистику из разных источников
        try {
          // Получаем статистику по игрокам
          const playersApi = await import('@/api/players').then(m => m.usePlayersApi());
          const playerStats = await playersApi.getPlayersCount();
          stats.players.total = playerStats.count || 0;
        } catch (e) {
          console.warn('Не удалось получить статистику игроков:', e);
        }
        
        try {
          // Получаем статистику по кейсам с разбивкой по статусам
          const casesApi = await import('@/api/cases').then(m => m.useCasesApi());
          
          // Запрашиваем общую статистику
          const allCases = await casesApi.getAccessibleCases({ limit: 0 });
          stats.cases.total = allCases.count || 0;
          
          // Запрашиваем открытые кейсы
          const openCases = await casesApi.getAccessibleCases({ status: 'open', limit: 0 });
          stats.cases.open = openCases.count || 0;
          
          // Запрашиваем кейсы в работе
          const inProgressCases = await casesApi.getAccessibleCases({ status: 'in_progress', limit: 0 });
          stats.cases.in_progress = inProgressCases.count || 0;
          
          // Запрашиваем закрытые кейсы
          const closedCases = await casesApi.getAccessibleCases({ status: 'closed', limit: 0 });
          stats.cases.closed = closedCases.count || 0;
          
          // Запрашиваем решенные кейсы
          const resolvedCases = await casesApi.getAccessibleCases({ status: 'resolved', limit: 0 });
          stats.cases.resolved = resolvedCases.count || 0;
          
          // Проверка корректности
          if (stats.cases.total === 0 && 
              (stats.cases.open || stats.cases.in_progress || stats.cases.closed || stats.cases.resolved)) {
            stats.cases.total = (stats.cases.open || 0) + 
                              (stats.cases.in_progress || 0) + 
                              (stats.cases.closed || 0) + 
                              (stats.cases.resolved || 0);
          }
        } catch (e) {
          console.warn('Не удалось получить статистику кейсов:', e);
        }
        
        // Другие источники статистики можно добавить здесь
        
        return stats;
      } catch (error) {
        console.error('Ошибка при получении запасной статистики:', error);
        return defaultDashboardStats;
      }
    }
  };
} 