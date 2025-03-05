import type { 
  Case, 
  CaseCreate, 
  CaseUpdate, 
  CaseComment,
  CaseCommentCreate,
  CaseEvidence 
} from '@/types/models';
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
    async getCaseById(id: string) {
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
    async createCase(caseData: CaseCreate) {
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
    async updateCase(id: string, caseData: CaseUpdate) {
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
    async deleteCase(id: string) {
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
    async updateCaseStatus(id: string, status: 'open' | 'closed') {
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
    async getCasesByStatus(status: 'open' | 'closed'): Promise<Case[]> {
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
    },

    /**
     * Получить комментарии к делу
     */
    async getCaseComments(caseId: string): Promise<CaseComment[]> {
      try {
        const response = await api.get(`${baseUrl}/${caseId}/comments`);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при получении комментариев к делу с ID ${caseId}:`, error);
        throw error;
      }
    },

    /**
     * Добавить комментарий к делу
     */
    async addCaseComment(caseId: string, commentData: { comment: string }): Promise<CaseComment> {
      try {
        const response = await api.post(`${baseUrl}/${caseId}/comments`, {
          ...commentData,
          case_id: caseId
        });
        return response.data;
      } catch (error) {
        console.error(`Ошибка при добавлении комментария к делу с ID ${caseId}:`, error);
        throw error;
      }
    },

    /**
     * Получить доказательства к делу
     */
    async getCaseEvidences(caseId: string): Promise<CaseEvidence[]> {
      try {
        const response = await api.get(`${baseUrl}/${caseId}/evidences`);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при получении доказательств к делу с ID ${caseId}:`, error);
        throw error;
      }
    },

    /**
     * Загрузить доказательство к делу
     */
    async uploadCaseEvidence(
      caseId: string, 
      file: File, 
      type: string, 
      description?: string
    ): Promise<CaseEvidence> {
      try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('type', type);
        if (description) {
          formData.append('description', description);
        }
        
        const response = await api.post(`${baseUrl}/${caseId}/evidences`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data;
      } catch (error) {
        console.error(`Ошибка при загрузке доказательства к делу с ID ${caseId}:`, error);
        throw error;
      }
    },

    /**
     * Удалить доказательство
     */
    async deleteCaseEvidence(caseId: string, evidenceId: string): Promise<{ success: boolean }> {
      try {
        const response = await api.delete(`${baseUrl}/${caseId}/evidences/${evidenceId}`);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при удалении доказательства:`, error);
        throw error;
      }
    }
  };
} 