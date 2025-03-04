import { useApiClient } from '@/composables/useApiClient';
import type { Fund, CreateFundRequest, UpdateFundRequest } from '@/types/models';

export function useFundsApi() {
  const api = useApiClient();
  const baseUrl = '/api/v1/funds';

  const getFunds = async (): Promise<Fund[]> => {
    try {
      const response = await api.get(baseUrl);
      return response.data;
    } catch (error) {
      console.error('Ошибка при получении фондов:', error);
      throw error;
    }
  };

  const getFundById = async (id: string): Promise<Fund> => {
    try {
      const response = await api.get(`${baseUrl}/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Ошибка при получении фонда ${id}:`, error);
      throw error;
    }
  };

  const createFund = async (fundData: CreateFundRequest): Promise<Fund> => {
    try {
      const response = await api.post(baseUrl, fundData);
      return response.data;
    } catch (error) {
      console.error('Ошибка при создании фонда:', error);
      throw error;
    }
  };

  const updateFund = async (id: string, fundData: UpdateFundRequest): Promise<Fund> => {
    try {
      const response = await api.put(`${baseUrl}/${id}`, fundData);
      return response.data;
    } catch (error) {
      console.error(`Ошибка при обновлении фонда ${id}:`, error);
      throw error;
    }
  };

  const deleteFund = async (id: string): Promise<void> => {
    try {
      await api.delete(`${baseUrl}/${id}`);
    } catch (error) {
      console.error(`Ошибка при удалении фонда ${id}:`, error);
      throw error;
    }
  };

  return {
    getFunds,
    getFundById,
    createFund,
    updateFund,
    deleteFund
  };
} 