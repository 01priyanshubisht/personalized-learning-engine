import { apiClient } from './client';
import { LearningRequest, LearningResponse } from '../types/api';

export const learningApi = {
  teach: async (request: LearningRequest): Promise<LearningResponse> => {
    const response = await apiClient.post<LearningResponse>('/learning/teach', request);
    return response.data;
  }
};
