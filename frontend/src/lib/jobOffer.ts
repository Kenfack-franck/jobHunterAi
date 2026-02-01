import axios from "axios";
import { JobOffer, JobOfferCreate, JobOfferUpdate, JobOfferSearchParams } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

class JobOfferService {
  private getHeaders() {
    const token = localStorage.getItem("auth_token");
    return {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    };
  }

  // Get all user's job offers
  async getJobOffers(limit: number = 20, offset: number = 0): Promise<JobOffer[]> {
    const response = await axios.get(`${API_URL}/jobs`, {
      params: { limit, offset },
      headers: this.getHeaders(),
    });
    return response.data;
  }

  // Get a single job offer by ID
  async getJobOfferById(id: string): Promise<JobOffer> {
    const response = await axios.get(`${API_URL}/jobs/${id}`, {
      headers: this.getHeaders(),
    });
    return response.data;
  }

  // Create a new job offer
  async createJobOffer(data: JobOfferCreate): Promise<JobOffer> {
    const response = await axios.post(`${API_URL}/jobs`, data, {
      headers: this.getHeaders(),
    });
    return response.data;
  }

  // Update an existing job offer
  async updateJobOffer(id: string, data: JobOfferUpdate): Promise<JobOffer> {
    const response = await axios.put(`${API_URL}/jobs/${id}`, data, {
      headers: this.getHeaders(),
    });
    return response.data;
  }

  // Delete a job offer
  async deleteJobOffer(id: string): Promise<void> {
    await axios.delete(`${API_URL}/jobs/${id}`, {
      headers: this.getHeaders(),
    });
  }

  // Search job offers with filters
  async searchJobOffers(params: JobOfferSearchParams): Promise<JobOffer[]> {
    const response = await axios.get(`${API_URL}/jobs/search`, {
      params,
      headers: this.getHeaders(),
    });
    return response.data;
  }

  // Get count of job offers
  async getJobOffersCount(): Promise<number> {
    const response = await axios.get(`${API_URL}/jobs/stats/count`, {
      headers: this.getHeaders(),
    });
    return response.data.count;
  }

  // ============================================
  // ASYNC SEARCH (with Celery)
  // ============================================
  
  /**
   * Lance une recherche asynchrone avec scraping
   * Retourne immédiatement un task_id pour suivre la progression
   */
  async searchJobsAsync(params: JobOfferSearchParams): Promise<{ task_id: string; status: string }> {
    const queryParams = new URLSearchParams();
    if (params.keyword) queryParams.append("keywords", params.keyword);
    if (params.location) queryParams.append("location", params.location);
    if (params.job_type) queryParams.append("job_type", params.job_type);
    if (params.company_name) queryParams.append("company", params.company_name);
    
    const response = await axios.post(
      `${API_URL}/jobs/search/async?${queryParams.toString()}`,
      {},
      { headers: this.getHeaders() }
    );
    
    return response.data;
  }
  
  /**
   * Récupère le statut d'une recherche asynchrone
   * À appeler en boucle (polling) jusqu'à obtenir status="completed" ou "failed"
   */
  async getSearchStatus(taskId: string): Promise<{
    task_id: string;
    status: "pending" | "processing" | "completed" | "failed";
    message: string;
    progress?: number;
    offers?: JobOffer[];
    count?: number;
    error?: string;
  }> {
    const response = await axios.get(
      `${API_URL}/jobs/search/status/${taskId}`,
      { headers: this.getHeaders() }
    );
    
    return response.data;
  }
  
  /**
   * Helper: Lance une recherche et poll le statut jusqu'à complétion
   * Appelle onProgress à chaque mise à jour du statut
   */
  async searchJobsWithProgress(
    params: JobOfferSearchParams,
    onProgress: (status: string, message: string, progress?: number) => void
  ): Promise<JobOffer[]> {
    // Lancer la recherche
    const { task_id } = await this.searchJobsAsync(params);
    
    // Polling du statut
    return new Promise((resolve, reject) => {
      const pollInterval = setInterval(async () => {
        try {
          const status = await this.getSearchStatus(task_id);
          
          // Notifier de la progression
          onProgress(status.status, status.message, status.progress);
          
          // Si terminé avec succès
          if (status.status === "completed") {
            clearInterval(pollInterval);
            resolve(status.offers || []);
          }
          
          // Si échec
          else if (status.status === "failed") {
            clearInterval(pollInterval);
            reject(new Error(status.error || "Recherche échouée"));
          }
          
          // Sinon continuer à poller
        } catch (error) {
          clearInterval(pollInterval);
          reject(error);
        }
      }, 2000); // Poll toutes les 2 secondes
      
      // Timeout après 2 minutes
      setTimeout(() => {
        clearInterval(pollInterval);
        reject(new Error("Timeout: La recherche a pris trop de temps"));
      }, 120000);
    });
  }
}

const jobOfferService = new JobOfferService();
export default jobOfferService;
