import { apiClient } from './client';
import { UploadResponse } from '../types/api';

export const documentsApi = {
  upload: async (learnerId: number, file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append("file", file);
    
    const response = await apiClient.post<UploadResponse>(
      `/documents/upload?learner_id=${learnerId}`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  }
};
