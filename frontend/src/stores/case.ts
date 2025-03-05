import { defineStore } from 'pinia';
import { useCasesApi } from '@/api/cases';
import type {
  Case,
  CaseCreate,
  CaseUpdate,
  CaseComment,
  CaseEvidence
} from '@/types/models';

export const useCaseStore = defineStore('case', {
  state: () => ({
    cases: [] as Case[],
    currentCase: null as Case | null,
    caseComments: [] as CaseComment[],
    caseEvidences: [] as CaseEvidence[],
    loading: false,
    error: null as string | null
  }),

  getters: {
    getCaseById: (state) => (id: string) => {
      return state.cases.find(c => c.id === id);
    },
    getCasesByPlayerId: (state) => (playerId: string) => {
      return state.cases.filter(c => c.player_id === playerId);
    },
    getCasesByStatus: (state) => (status: 'open' | 'closed') => {
      return state.cases.filter(c => c.status === status);
    }
  },

  actions: {
    async fetchCases() {
      this.loading = true;
      this.error = null;
      try {
        const api = useCasesApi();
        const cases = await api.getCases();
        this.cases = cases;
      } catch (error) {
        console.error('Ошибка при загрузке дел:', error);
        this.error = 'Не удалось загрузить дела';
      } finally {
        this.loading = false;
      }
    },

    async fetchCase(id: string) {
      this.loading = true;
      this.error = null;
      try {
        const api = useCasesApi();
        const caseItem = await api.getCaseById(id);
        this.currentCase = caseItem;
        
        // Обновляем дело в общем списке, если оно там есть
        const index = this.cases.findIndex(c => c.id === id);
        if (index !== -1) {
          this.cases[index] = caseItem;
        }
        
        return caseItem;
      } catch (error) {
        console.error(`Ошибка при загрузке дела с ID ${id}:`, error);
        this.error = 'Не удалось загрузить дело';
        return null;
      } finally {
        this.loading = false;
      }
    },

    async createCase(caseData: CaseCreate) {
      this.loading = true;
      this.error = null;
      try {
        const api = useCasesApi();
        const caseItem = await api.createCase(caseData);
        this.cases.push(caseItem);
        return caseItem;
      } catch (error) {
        console.error('Ошибка при создании дела:', error);
        this.error = 'Не удалось создать дело';
        return null;
      } finally {
        this.loading = false;
      }
    },

    async updateCase(id: string, caseData: CaseUpdate) {
      this.loading = true;
      this.error = null;
      try {
        const api = useCasesApi();
        const caseItem = await api.updateCase(id, caseData);
        
        // Обновляем дело в общем списке
        const index = this.cases.findIndex(c => c.id === id);
        if (index !== -1) {
          this.cases[index] = caseItem;
        }
        
        // Обновляем currentCase, если это оно
        if (this.currentCase && this.currentCase.id === id) {
          this.currentCase = caseItem;
        }
        
        return caseItem;
      } catch (error) {
        console.error(`Ошибка при обновлении дела с ID ${id}:`, error);
        this.error = 'Не удалось обновить дело';
        return null;
      } finally {
        this.loading = false;
      }
    },

    async deleteCase(id: string) {
      this.loading = true;
      this.error = null;
      try {
        const api = useCasesApi();
        await api.deleteCase(id);
        
        // Удаляем дело из списка
        this.cases = this.cases.filter(caseItem => caseItem.id !== id);
        
        // Сбрасываем currentCase, если это было оно
        if (this.currentCase && this.currentCase.id === id) {
          this.currentCase = null;
        }
        
        return true;
      } catch (error) {
        console.error(`Ошибка при удалении дела с ID ${id}:`, error);
        this.error = 'Не удалось удалить дело';
        return false;
      } finally {
        this.loading = false;
      }
    },

    async fetchCasesByPlayer(playerId: string) {
      this.loading = true;
      this.error = null;
      try {
        const api = useCasesApi();
        const cases = await api.getCasesByPlayer(playerId);

        // Мы добавляем дела игрока в общий список, если их там еще нет
        cases.forEach(caseItem => {
          const index = this.cases.findIndex(c => c.id === caseItem.id);
          if (index === -1) {
            this.cases.push(caseItem);
          } else {
            this.cases[index] = caseItem;
          }
        });
        return cases;
      } catch (error) {
        console.error(`Ошибка при загрузке дел игрока с ID ${playerId}:`, error);
        this.error = 'Не удалось загрузить дела игрока';
        return [];
      } finally {
        this.loading = false;
      }
    },

    async closeCase(id: string) {
      this.loading = true;
      this.error = null;
      try {
        const api = useCasesApi();
        const caseItem = await api.closeCase(id);
        
        // Обновляем дело в общем списке
        const index = this.cases.findIndex(c => c.id === id);
        if (index !== -1) {
          this.cases[index] = caseItem;
        }
        
        // Обновляем currentCase, если это оно
        if (this.currentCase && this.currentCase.id === id) {
          this.currentCase = caseItem;
        }
        
        return caseItem;
      } catch (error) {
        console.error(`Ошибка при закрытии дела с ID ${id}:`, error);
        this.error = 'Не удалось закрыть дело';
        return null;
      } finally {
        this.loading = false;
      }
    },

    // Методы для работы с комментариями
    async fetchCaseComments(caseId: string) {
      this.loading = true;
      try {
        const api = useCasesApi();
        const comments = await api.getCaseComments(caseId);
        this.caseComments = comments;
        return comments;
      } catch (error) {
        console.error(`Ошибка при загрузке комментариев к делу с ID ${caseId}:`, error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async addCaseComment(caseId: string, commentData: { comment: string }) {
      try {
        const api = useCasesApi();
        const comment = await api.addCaseComment(caseId, commentData);
        
        // Добавляем комментарий в список
        this.caseComments.push(comment);
        
        return comment;
      } catch (error) {
        console.error(`Ошибка при добавлении комментария к делу с ID ${caseId}:`, error);
        throw error;
      }
    },

    // Методы для работы с доказательствами
    async fetchCaseEvidences(caseId: string) {
      this.loading = true;
      try {
        const api = useCasesApi();
        const evidences = await api.getCaseEvidences(caseId);
        this.caseEvidences = evidences;
        return evidences;
      } catch (error) {
        console.error(`Ошибка при загрузке доказательств к делу с ID ${caseId}:`, error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async uploadCaseEvidence(caseId: string, file: File, type: string, description?: string) {
      this.loading = true;
      try {
        const api = useCasesApi();
        const evidence = await api.uploadCaseEvidence(caseId, file, type, description);
        
        // Добавляем доказательство в список
        this.caseEvidences.push(evidence);
        
        return evidence;
      } catch (error) {
        console.error(`Ошибка при загрузке доказательства к делу с ID ${caseId}:`, error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async deleteCaseEvidence(caseId: string, evidenceId: string) {
      try {
        const api = useCasesApi();
        await api.deleteCaseEvidence(caseId, evidenceId);
        
        // Удаляем доказательство из списка
        this.caseEvidences = this.caseEvidences.filter(evidence => evidence.id !== evidenceId);
        
        return true;
      } catch (error) {
        console.error(`Ошибка при удалении доказательства с ID ${evidenceId} для дела ${caseId}:`, error);
        throw error;
      }
    }
  }
}); 