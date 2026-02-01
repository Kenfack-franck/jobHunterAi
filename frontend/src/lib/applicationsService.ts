import apiClient from './api';

export interface Application {
  id: string;
  user_id: string;
  job_offer_id: string | null;
  company_name: string;
  job_title: string;
  applied_at: string;
  updated_at: string;
  status: 'pending' | 'replied' | 'interview' | 'rejected' | 'accepted';
  email_to: string;
  documents_sent: Record<string, any> | null;
  notes: string | null;
}

export interface ApplicationCreate {
  company_name: string;
  job_title: string;
  email_to: string;
  job_offer_id?: string;
  notes?: string;
}

export interface ApplicationUpdate {
  status?: Application['status'];
  notes?: string;
}

export interface ApplicationStats {
  total: number;
  by_status: Record<string, number>;
  response_rate: number;
}

class ApplicationsService {
  async getApplications(status?: Application['status']): Promise<Application[]> {
    const params = status ? { status } : {};
    const response = await apiClient.get('/applications/', { params });
    return response.data;
  }

  async getApplication(id: string): Promise<Application> {
    const response = await apiClient.get(`/applications/${id}`);
    return response.data;
  }

  async createApplication(data: ApplicationCreate): Promise<Application> {
    const response = await apiClient.post('/applications/', data);
    return response.data;
  }

  async updateApplication(id: string, data: ApplicationUpdate): Promise<Application> {
    const response = await apiClient.put(`/applications/${id}`, data);
    return response.data;
  }

  async deleteApplication(id: string): Promise<void> {
    await apiClient.delete(`/applications/${id}`);
  }

  async getStats(): Promise<ApplicationStats> {
    const response = await apiClient.get('/applications/stats');
    return response.data;
  }
}

export const applicationsService = new ApplicationsService();
