import { useApiClient } from '@/composables/useApiClient';
import type { Fund } from '@/types/models';

export function useFundsApi() {
  const api = useApiClient();
  const baseUrl = '/funds';

  return {
    /**
     * Получить список всех фондов
     */
    async getFunds() {
      try {
        console.log('Запрос списка фондов: ' + baseUrl);
        const response = await api.get<Fund[]>(baseUrl);
        return response.data;
      } catch (error) {
        console.error('Ошибка при получении списка фондов:', error);
        throw error;
      }
    },

    /**
     * Получить фонд по ID
     */
    async getFundById(id: number) {
      try {
        const response = await api.get<Fund>(`${baseUrl}/${id}`);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при получении фонда с ID ${id}:`, error);
        throw error;
      }
    },

    /**
     * Создать новый фонд
     */
    async createFund(fundData: any) {
      try {
        const response = await api.post<Fund>(baseUrl, fundData);
        return response.data;
      } catch (error) {
        console.error('Ошибка при создании фонда:', error);
        throw error;
      }
    },

    /**
     * Обновить данные фонда
     */
    async updateFund(id: number, fundData: any) {
      try {
        const response = await api.put<Fund>(`${baseUrl}/${id}`, fundData);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при обновлении фонда с ID ${id}:`, error);
        throw error;
      }
    },

    /**
     * Удалить фонд
     */
    async deleteFund(id: number) {
      try {
        const response = await api.delete<{ success: boolean }>(`${baseUrl}/${id}`);
        return response.data;
      } catch (error) {
        console.error(`Ошибка при удалении фонда с ID ${id}:`, error);
        throw error;
      }
    }
  };
} 