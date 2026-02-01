import apiClient from './api';

export interface Document {
  id: string;
  user_id: string;
  job_offer_id?: string;
  profile_id?: string;
  document_type: 'resume' | 'cover_letter';
  content: string;
  filename: string;
  metadata?: any;
  generated_at: string;  // Backend utilise "generated_at" et non "created_at"
  updated_at: string;
}

export interface DocumentWithDetails extends Document {
  job_title?: string;
  company_name?: string;
}

class DocumentsService {
  async getDocuments(): Promise<DocumentWithDetails[]> {
    const response = await apiClient.get('/documents/');
    return response.data;
  }

  async getDocument(documentId: string): Promise<Document> {
    const response = await apiClient.get(`/documents/${documentId}`);
    return response.data;
  }

  async generateDocuments(jobOfferId: string, profileId: string, options?: {
    include_cv?: boolean;
    include_cover_letter?: boolean;
    tone?: 'professional' | 'enthusiastic' | 'creative';
    length?: 'short' | 'medium' | 'long';
  }) {
    const documents: Document[] = [];
    const tone = options?.tone || 'professional';
    const length = options?.length || 'medium';
    
    // Générer le CV si demandé
    if (options?.include_cv !== false) {
      const cvResponse = await apiClient.post('/documents/generate', {
        job_offer_id: jobOfferId,
        document_type: 'resume',
        tone: tone,
        language: 'fr'
      });
      documents.push(cvResponse.data);
    }
    
    // Générer la lettre de motivation si demandée
    if (options?.include_cover_letter !== false) {
      const clResponse = await apiClient.post('/documents/generate', {
        job_offer_id: jobOfferId,
        document_type: 'cover_letter',
        tone: tone,
        length: length,
        language: 'fr'
      });
      documents.push(clResponse.data);
    }
    
    return { documents };
  }

  async downloadDocument(documentId: string): Promise<Blob> {
    const response = await apiClient.get(`/documents/${documentId}/download`, {
      responseType: 'blob'
    });
    return response.data;
  }

  async deleteDocument(documentId: string): Promise<void> {
    await apiClient.delete(`/documents/${documentId}`);
  }

  async getStats() {
    const response = await apiClient.get('/documents/stats');
    return response.data;
  }
}

export const documentsService = new DocumentsService();
