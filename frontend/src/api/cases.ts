import type { Case, CaseCreate, CaseUpdate, CaseStatus } from '@/types/models';
import { useApiClient } from '@/composables/useApiClient';

export function useCasesApi() {
  const api = useApiClient();
  const baseUrl = '/cases';

  return {
    /**
     * Получить список всех дел
     */
    async getCases() {
      try {
        console.log('Запрос списка дел: ' + baseUrl);
        const response = await api.get<Case[]>(baseUrl);
        return response.data;
      } catch (error) {
        console.error('Ошибка при получении списка дел:', error);
        throw error;
      }
    },

    /**
     * Получить дело по ID
     */
    async getCaseById(id: number) {
      try {
        const response = await api.get<Case>(`${baseUrl}/${id}`);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при получении дела с ID ${id}:`, error);
        throw error;
      }
    },

    /**
     * Создать новое дело
     */
    async createCase(caseData: any) {
      try {
        const response = await api.post<Case>(baseUrl, caseData);
        return response.data;
      } catch (error) {
        console.error('Ошибка при создании дела:', error);
        throw error;
      }
    },

    /**
     * Обновить данные дела
     */
    async updateCase(id: number, caseData: any) {
      try {
        const response = await api.put<Case>(`${baseUrl}/${id}`, caseData);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при обновлении дела с ID ${id}:`, error);
        throw error;
      }
    },

    /**
     * Удалить дело
     */
    async deleteCase(id: number) {
      try {
        const response = await api.delete<{ success: boolean }>(`${baseUrl}/${id}`);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при удалении дела с ID ${id}:`, error);
        throw error;
      }
    },

    /**
     * Изменить статус дела
     */
    async updateCaseStatus(id: number, status: any) {
      try {
        const response = await api.patch<Case>(`${baseUrl}/${id}/status`, { status });
        return response.data;
      } catch (error) {
        console.error(`Ошибка при изменении статуса дела с ID ${id}:`, error);
        throw error;
      }
    },

    /**
     * Закрыть дело
     */
    async closeCase(id: string): Promise<Case> {
      try {
        const response = await api.post(`${baseUrl}/${id}/close`);
        return response.data;
      } catch (error) {
        console.error(`Error closing case with id ${id}:`, error);
        throw error;
      }
    },

    /**
     * Получить дела по статусу
     */
    async getCasesByStatus(status: any): Promise<Case[]> {
      try {
        const response = await api.get(baseUrl, { params: { status } });
        return response.data;
      } catch (error) {
        console.error(`Error fetching cases by status ${status}:`, error);
        throw error;
      }
    },

    /**
     * Получить дела по игроку
     */
    async getCasesByPlayer(playerId: string): Promise<Case[]> {
      try {
        const response = await api.get(baseUrl, { params: { player_id: playerId } });
        return response.data;
      } catch (error) {
        console.error(`Error fetching cases for player ${playerId}:`, error);
        throw error;
      }
    }
  };
} 