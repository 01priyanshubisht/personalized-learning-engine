import { apiClient } from './client';
import { HistoryResponse } from '../types/api';

export const historyApi = {
  getHistory: async (learnerId: number, limit: number = 50): Promise<HistoryResponse> => {
    const response = await apiClient.get<HistoryResponse>(`/history/${learnerId}?limit=${limit}`);
    return response.data;
  }
};
