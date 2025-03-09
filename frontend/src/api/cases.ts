import type { 
  Case, 
  CaseCreate, 
  CaseUpdate, 
  CaseComment,
  CaseCommentCreate,
  CaseEvidence,
  CaseExtended
} from '@/types/models';
import { useApiClient } from '@/composables/useApiClient';
import * as jwtDecode from 'jwt-decode';

// Моковые данные для демонстрации
const mockCases: CaseExtended[] = [
  {
    id: '1',
    case_number: 'CASE-001',
    title: 'Скам игрока на форуме',
    description: 'Игрок обманул нескольких участников форума, пообещав услуги, но не выполнив их после получения оплаты.',
    status: 'open',
    case_type: 'scam',
    player_id: '1',
    created_at: '2023-03-01T10:30:00Z',
    updated_at: '2023-03-01T10:30:00Z',
    created_by: 'admin',
    created_by_fund_id: '1',
    amount: 1500,
    currency: 'USD',
    arbitrage_type: 'pending',
    arbitrage_amount: 1500,
    arbitrage_currency: 'USD',
    player: {
      id: '1',
      full_name: 'Иванов Иван',
      first_name: 'Иван',
      last_name: 'Иванов',
      email: 'ivanov@example.com',
      phone: '+71234567890',
      created_at: '2023-01-15T12:00:00Z',
      updated_at: '2023-01-15T12:00:00Z'
    },
    fund: {
      id: '1',
      name: 'Альфа Фонд',
      description: 'Фонд поддержки игроков',
      created_at: '2022-12-01T00:00:00Z',
      updated_at: '2022-12-01T00:00:00Z'
    }
  },
  {
    id: '2',
    case_number: 'CASE-002',
    title: 'Долг по игре в покер',
    description: 'Игрок задолжал сумму после игры в покер и отказывается выплачивать долг.',
    status: 'in_progress',
    case_type: 'debt',
    player_id: '2',
    created_at: '2023-02-15T14:45:00Z',
    updated_at: '2023-02-16T09:30:00Z',
    created_by: 'manager1',
    created_by_fund_id: '1',
    amount: 3000,
    currency: 'EUR',
    arbitrage_type: 'in_progress',
    arbitrage_amount: 3000,
    arbitrage_currency: 'EUR',
    player: {
      id: '2',
      full_name: 'Петров Петр',
      first_name: 'Петр',
      last_name: 'Петров',
      email: 'petrov@example.com',
      created_at: '2023-01-20T15:30:00Z',
      updated_at: '2023-01-20T15:30:00Z'
    },
    fund: {
      id: '1',
      name: 'Альфа Фонд',
      description: 'Фонд поддержки игроков',
      created_at: '2022-12-01T00:00:00Z',
      updated_at: '2022-12-01T00:00:00Z'
    }
  },
  {
    id: '3',
    case_number: 'CASE-003',
    title: 'Мультиаккаунтинг на GGPoker',
    description: 'Подозрение в использовании нескольких аккаунтов на платформе GGPoker.',
    status: 'resolved',
    case_type: 'multi_accounting',
    player_id: '3',
    created_at: '2023-02-20T11:15:00Z',
    updated_at: '2023-02-25T16:40:00Z',
    created_by: 'manager2',
    created_by_fund_id: '2',
    amount: 0,
    currency: 'USD',
    player: {
      id: '3',
      full_name: 'Сидоров Сидор',
      first_name: 'Сидор',
      last_name: 'Сидоров',
      email: 'sidorov@example.com',
      created_at: '2023-01-25T10:00:00Z',
      updated_at: '2023-01-25T10:00:00Z'
    },
    fund: {
      id: '2',
      name: 'Бета Фонд',
      description: 'Инвестиционный фонд игроков',
      created_at: '2022-12-10T00:00:00Z',
      updated_at: '2022-12-10T00:00:00Z'
    }
  }
];

export function useCasesApi() {
  const api = useApiClient();
  const baseUrl = '/cases';

  return {
    /**
     * Получить список всех дел
     */
    async getCases(): Promise<Case[]> {
      try {
        // Всегда используем реальное API
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
    async getCaseById(id: string): Promise<CaseExtended> {
      try {
        // Всегда используем реальное API
        const response = await api.get<CaseExtended>(`${baseUrl}/${id}`);
        
        // Дополнительное логирование для отладки
        console.log(`API response for case ${id}:`, response.data);
        
        // Проверяем наличие основных полей
        if (!response.data) {
          console.error(`Empty response for case ${id}`);
        } else {
          console.log(`Case fields: ${Object.keys(response.data).join(', ')}`);
        }
        
        return response.data;
      } catch (error) {
        console.error(`Ошибка при получении дела с ID ${id}:`, error);
        throw error;
      }
    },

    /**
     * Создать новое дело
     */
    async createCase(caseData: CaseCreate): Promise<CaseExtended> {
      try {
        const response = await api.post<CaseExtended>(baseUrl, caseData);
        return response.data;
      } catch (error) {
        console.error('Ошибка при создании дела:', error);
        throw error;
      }
    },

    /**
     * Обновить существующее дело
     */
    async updateCase(id: string, caseData: CaseUpdate): Promise<CaseExtended> {
      try {
        const response = await api.put<CaseExtended>(`${baseUrl}/${id}`, caseData);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при обновлении дела ${id}:`, error);
        throw error;
      }
    },

    /**
     * Удалить дело
     */
    async deleteCase(id: string): Promise<void> {
      try {
        // Всегда используем реальное API
        await api.delete(`${baseUrl}/${id}`);
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
     * Получить дела по игроку (расширенные данные, включая информацию об игроке и фонде)
     */
    async getCasesByPlayer(playerId: string): Promise<CaseExtended[]> {
      try {
        const response = await api.get<CaseExtended[]>(`${baseUrl}/by-player/${playerId}`);
        return response.data;
      } catch (error) {
        console.error(`Error fetching cases for player ${playerId}:`, error);
        throw error;
      }
    },

    /**
     * Получить дела по фонду (расширенные данные, включая информацию об игроке и фонде)
     */
    async getCasesByFund(fundId: string): Promise<CaseExtended[]> {
      try {
        const response = await api.get<CaseExtended[]>(`${baseUrl}/by-fund/${fundId}`);
        return response.data;
      } catch (error) {
        console.error(`Error fetching cases for fund ${fundId}:`, error);
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
    },

    /**
     * Получить доступные для просмотра кейсы (с учетом изоляции фондов)
     * Этот метод проверяет, какие кейсы действительно доступны пользователю
     */
    async getAccessibleCases(params?: any): Promise<{ results: Case[], count: number }> {
      try {
        // Получаем данные о текущем пользователе из токена
        let userData = null;
        try {
          const token = localStorage.getItem('token');
          if (token) {
            // Если токен есть, декодируем его
            userData = jwtDecode.jwtDecode(token);
            console.log('Данные пользователя из токена JWT:', userData);
          }
        } catch (e) {
          console.error('Ошибка декодирования токена:', e);
        }

        // Настраиваем параметры запроса
        const requestParams = { ...params };
        
        // Если не указан лимит, устанавливаем значение по умолчанию
        if (!requestParams.limit && requestParams.limit !== 0) {
          requestParams.limit = 20; // Значение по умолчанию
        }
        
        // Для запросов со статусом проверяем, если передан список статусов через запятую
        if (requestParams.status && typeof requestParams.status === 'string' && requestParams.status.includes(',')) {
          // Преобразовываем "open,in_progress" в ["open", "in_progress"]
          const statusList = requestParams.status.split(',').map((s: string) => s.trim());
          // Используем параметр API для множественных значений
          requestParams.status = statusList;
        }
        
        console.log('Запрос на получение кейсов с параметрами:', requestParams, 'пользователь:', userData);
        
        // Получаем кейсы с учетом параметров
        // Добавляем обработку потенциальных ошибок сети
        let response;
        try {
          response = await api.get(baseUrl, { params: requestParams });
          console.log('Получен ответ от API:', response.data);
        } catch (networkError) {
          console.error('Ошибка сети при получении кейсов:', networkError);
          // В случае ошибки сети возвращаем пустые данные
          return { results: [], count: 0 };
        }
        
        // Возвращаем результаты и общее количество
        // Предполагаем, что API возвращает { results: Case[], count: number }
        if (response.data.results && response.data.count !== undefined) {
          return response.data;
        }
        
        // Если API возвращает массив, преобразуем в нужный формат
        if (Array.isArray(response.data)) {
          return {
            results: response.data,
            count: response.data.length
          };
        }
        
        // Для других форматов ответа - логируем и возвращаем безопасное значение
        console.warn('API вернул неожиданный формат данных:', response.data);
        return {
          results: Array.isArray(response.data) ? response.data : [],
          count: Array.isArray(response.data) ? response.data.length : 0
        };
      } catch (error) {
        console.error('Ошибка при получении кейсов:', error);
        return { results: [], count: 0 };
      }
    },
    
    /**
     * Проверяет, может ли текущий пользователь редактировать кейс
     * @param caseItem Кейс для проверки
     * @returns true, если пользователь может редактировать кейс
     */
    canEditCase(caseItem: Case): boolean {
      // Получаем текущего пользователя из хранилища
      const authStore = JSON.parse(localStorage.getItem('auth') || '{}');
      const currentUser = authStore.user;
      
      if (!currentUser) return false;
      
      // Админы могут редактировать любые кейсы
      if (currentUser.role === 'admin') return true;
      
      // Менеджеры могут редактировать только кейсы своего фонда
      return caseItem.created_by_fund_id === currentUser.fund_id;
    },
    
    /**
     * Сохраняет ID недоступного кейса в локальное хранилище,
     * чтобы не запрашивать его повторно
     */
    cacheInaccessibleCase(caseId: string): void {
      const cache = JSON.parse(localStorage.getItem('inaccessibleCases') || '[]');
      if (!cache.includes(caseId)) {
        cache.push(caseId);
        localStorage.setItem('inaccessibleCases', JSON.stringify(cache));
      }
    }
  };
} 