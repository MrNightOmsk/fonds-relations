import { useApiClient } from '@/composables/useApiClient';

// Тип для события аудита
export interface AuditEvent {
  id: string;
  action: string;
  description?: string;
  entity_type: string;
  entity_id: string;
  user_id: string;
  user_name?: string;
  created_at: string;
  metadata?: Record<string, any>;
}

export function useAuditApi() {
  const api = useApiClient();
  const baseUrl = '/audit';

  return {
    /**
     * Получить все события аудита с возможностью фильтрации
     */
    async getAuditEvents(params?: {
      limit?: number;
      offset?: number;
      entity_type?: string;
      entity_id?: string;
      user_id?: string;
      action?: string;
      from_date?: string;
      to_date?: string;
    }): Promise<{ results: AuditEvent[], count: number }> {
      try {
        const response = await api.get(baseUrl, { params });
        
        // Обработка разных форматов ответа API
        if (response.data.results && typeof response.data.count === 'number') {
          return response.data;
        } else if (Array.isArray(response.data)) {
          return {
            results: response.data,
            count: response.data.length
          };
        }
        
        return {
          results: [],
          count: 0
        };
      } catch (error) {
        console.error('Ошибка при получении событий аудита:', error);
        return { results: [], count: 0 };
      }
    },

    /**
     * Получить последние события аудита
     * @param limit Количество последних событий
     */
    async getRecentActivity(limit = 5): Promise<AuditEvent[]> {
      try {
        const response = await this.getAuditEvents({ limit });
        return response.results;
      } catch (error) {
        console.error('Ошибка при получении последних активностей:', error);
        return [];
      }
    },

    /**
     * Получить события аудита для конкретной сущности
     */
    async getEntityAudit(entityType: string, entityId: string, limit = 20): Promise<AuditEvent[]> {
      try {
        const response = await this.getAuditEvents({
          entity_type: entityType,
          entity_id: entityId,
          limit
        });
        return response.results;
      } catch (error) {
        console.error(`Ошибка при получении аудита для ${entityType} ${entityId}:`, error);
        return [];
      }
    },

    /**
     * Получить действия конкретного пользователя
     */
    async getUserActivity(userId: string, limit = 20): Promise<AuditEvent[]> {
      try {
        const response = await this.getAuditEvents({
          user_id: userId,
          limit
        });
        return response.results;
      } catch (error) {
        console.error(`Ошибка при получении активности пользователя ${userId}:`, error);
        return [];
      }
    }
  };
} 