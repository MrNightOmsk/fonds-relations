import type { Fund } from '@/types/models';
import { useApiClient } from '@/composables/useApiClient';

// Моковые данные для демонстрации
const mockFunds: Fund[] = [
  {
    id: '1',
    name: 'Альфа Фонд',
    description: 'Фонд поддержки игроков',
    created_at: '2022-12-01T00:00:00Z',
    updated_at: '2022-12-01T00:00:00Z'
  },
  {
    id: '2',
    name: 'Бета Фонд',
    description: 'Инвестиционный фонд игроков',
    created_at: '2022-12-10T00:00:00Z',
    updated_at: '2022-12-10T00:00:00Z'
  },
  {
    id: '3',
    name: 'Гамма Фонд',
    description: 'Международный гарантийный фонд',
    created_at: '2023-01-05T00:00:00Z',
    updated_at: '2023-01-05T00:00:00Z'
  }
];

export function useFundsApi() {
  const api = useApiClient();
  const baseUrl = '/funds';

  return {
    /**
     * Получить список всех фондов
     */
    async getFunds(): Promise<Fund[]> {
      try {
        // В моковом режиме возвращаем локальные данные
        if (window.location.hostname === 'localhost') {
          console.log('Using mock data for getFunds');
          return [...mockFunds];
        }
        
        // В реальном режиме используем API
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
    async getFundById(id: string): Promise<Fund> {
      try {
        // В моковом режиме возвращаем локальные данные
        if (window.location.hostname === 'localhost') {
          console.log('Using mock data for getFundById', id);
          const fund = mockFunds.find(f => f.id === id);
          if (!fund) {
            throw new Error(`Фонд с ID ${id} не найден`);
          }
          return { ...fund };
        }
        
        // В реальном режиме используем API
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
    async createFund(fundData: Pick<Fund, 'name' | 'description'>): Promise<Fund> {
      try {
        // В моковом режиме симулируем создание
        if (window.location.hostname === 'localhost') {
          console.log('Using mock data for createFund', fundData);
          const newFund: Fund = {
            id: Date.now().toString(),
            name: fundData.name,
            description: fundData.description || '',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
          };
          
          mockFunds.push(newFund);
          return { ...newFund };
        }
        
        // В реальном режиме используем API
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
    async updateFund(id: string, fundData: Partial<Pick<Fund, 'name' | 'description'>>): Promise<Fund> {
      try {
        // В моковом режиме симулируем обновление
        if (window.location.hostname === 'localhost') {
          console.log('Using mock data for updateFund', id, fundData);
          const index = mockFunds.findIndex(f => f.id === id);
          
          if (index === -1) {
            throw new Error(`Фонд с ID ${id} не найден`);
          }
          
          const updatedFund = {
            ...mockFunds[index],
            ...fundData,
            updated_at: new Date().toISOString()
          };
          
          mockFunds[index] = updatedFund;
          return { ...updatedFund };
        }
        
        // В реальном режиме используем API
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
    async deleteFund(id: string): Promise<void> {
      try {
        // В моковом режиме симулируем удаление
        if (window.location.hostname === 'localhost') {
          console.log('Using mock data for deleteFund', id);
          const index = mockFunds.findIndex(f => f.id === id);
          
          if (index === -1) {
            throw new Error(`Фонд с ID ${id} не найден`);
          }
          
          mockFunds.splice(index, 1);
          return;
        }
        
        // В реальном режиме используем API
        await api.delete(`${baseUrl}/${id}`);
      } catch (error) {
        console.error(`Ошибка при удалении фонда с ID ${id}:`, error);
        throw error;
      }
    }
  };
} 