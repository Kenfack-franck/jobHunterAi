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

  // Analyze URL to extract job offer information
  async analyzeUrl(url: string): Promise<{
    success: boolean;
    job_offer: JobOfferCreate;
    message: string;
  }> {
    try {
      const response = await axios.post(
        `${API_URL}/sources/custom/test`,
        { url },
        { headers: this.getHeaders() }
      );
      
      // Transform API response to JobOfferCreate format
      const analysis = response.data.analysis || {};
      
      return {
        success: response.data.success || false,
        job_offer: {
          job_title: analysis.job_title || analysis.title || "Titre à compléter",
          company_name: analysis.company_name || analysis.company || "",
          location: analysis.location || "",
          job_type: analysis.job_type || analysis.type || "",
          description: analysis.description || "",
          requirements: analysis.requirements || analysis.skills || "",
          source_url: url,
          source_platform: analysis.source_platform || "Custom",
          extracted_keywords: analysis.keywords || [],
        },
        message: response.data.message || "Analyse réussie"
      };
    } catch (error: any) {
      console.error('Error analyzing URL:', error);
      throw new Error(
        error.response?.data?.detail || 
        "Erreur lors de l'analyse de l'URL. Vérifiez que l'URL est accessible."
      );
    }
  }

  // Parse job text to extract job offer information using AI
  async parseJobText(text: string): Promise<{
    success: boolean;
    job_offer: JobOfferCreate;
    message: string;
  }> {
    try {
      const response = await axios.post(
        `${API_URL}/jobs/parse-text`,
        { text },
        { headers: this.getHeaders() }
      );
      
      // Transform API response to JobOfferCreate format
      const data = response.data;
      
      return {
        success: true,
        job_offer: {
          job_title: data.job_title || "Titre à compléter",
          company_name: data.company_name || "",
          location: data.location || "",
          job_type: data.job_type || "",
          description: data.description || text,
          requirements: data.requirements || "",
          source_url: data.source_url || "",
          source_platform: "Text Import",
          extracted_keywords: data.extracted_keywords || [],
        },
        message: response.data.message || "Texte analysé avec succès"
      };
    } catch (error: any) {
      console.error('Error parsing text:', error);
      throw new Error(
        error.response?.data?.detail || 
        "Erreur lors de l'analyse du texte. Réessayez avec un texte plus complet."
      );
    }
  }

  // Search job offers with filters
  async searchJobOffers(params: JobOfferSearchParams): Promise<JobOffer[]> {
    const response = await axios.get(`${API_URL}/jobs/search`, {
      params,
      headers: this.getHeaders(),
    });
    return response.data;
  }

  // ============================================
  // MULTI-SOURCE SEARCH (with cache and priority sources)
  // ============================================
  
  /**
   * Recherche avec scraping multi-sources + cache intelligent
   * Retourne les offres + métadonnées (sources utilisées, cache, durée)
   */
  async searchJobOffersWithScraping(params: JobOfferSearchParams): Promise<{
    success: boolean;
    offers: JobOffer[];
    count: number;
    sources_used?: string[];
    cached?: boolean;
    duration_seconds?: number;
    scraped_count?: number;
    deduplicated_count?: number;
    saved_count?: number;
    message?: string;
  }> {
    // Validation des paramètres
    const keywords = params.keyword?.trim() || '';
    if (!keywords || keywords.length < 2) {
      throw new Error('Veuillez entrer au moins 2 caractères pour la recherche');
    }

    const payload = {
      keywords: keywords,
      location: params.location,
      job_type: params.job_type,
      work_mode: params.work_mode,
      company: params.company_name,
      limit_per_platform: 100
    };

    const response = await axios.post(`${API_URL}/search/scrape`, payload, {
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
