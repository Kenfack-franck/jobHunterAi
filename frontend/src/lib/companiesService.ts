import apiClient from './api';

export interface WatchedCompany {
  id: number;
  user_id: number;
  company_name: string;
  careers_url: string;
  last_scraped_at?: string;
  offers_count: number;
  created_at: string;
}

export interface CreateCompanyWatchRequest {
  company_name: string;
  careers_url: string;
}

class CompaniesService {
  async getWatchedCompanies(): Promise<WatchedCompany[]> {
    const response = await apiClient.get('/watch/companies');
    // L'API retourne {watches: [...], total: X, ...}
    return response.data.watches || [];
  }

  async addCompanyWatch(data: CreateCompanyWatchRequest): Promise<WatchedCompany> {
    const response = await apiClient.post('/watch/company', data);
    return response.data;
  }

  async deleteCompanyWatch(watchId: number): Promise<void> {
    await apiClient.delete(`/watch/${watchId}`);
  }

  async triggerManualScrape(watchId: number): Promise<void> {
    await apiClient.post('/watch/scrape-all');
  }

  async getCompanyOffers(companyId: number) {
    const response = await apiClient.get(`/watch/${companyId}/offers`);
    return response.data;
  }
}

export const companiesService = new CompaniesService();
