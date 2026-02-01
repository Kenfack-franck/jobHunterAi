/**
 * Service de gestion des documents générés
 */
import type { GeneratedDocument, DocumentGenerateRequest, DocumentStatsResponse } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

/**
 * Génère un document (CV ou Lettre de Motivation)
 */
export async function generateDocument(
  request: DocumentGenerateRequest,
  token: string
): Promise<GeneratedDocument> {
  const response = await fetch(
    `${API_URL}/documents/generate`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Erreur lors de la génération');
  }

  return response.json();
}

/**
 * Liste les documents de l'utilisateur
 */
export async function listDocuments(
  token: string,
  documentType?: 'resume' | 'cover_letter'
): Promise<GeneratedDocument[]> {
  const params = new URLSearchParams();
  if (documentType) params.append('document_type', documentType);
  
  const url = `${API_URL}/documents/?${params.toString()}`;
  
  const response = await fetch(url, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error('Erreur lors de la récupération des documents');
  }

  return response.json();
}

/**
 * Récupère un document par son ID
 */
export async function getDocument(
  documentId: string,
  token: string
): Promise<GeneratedDocument> {
  const response = await fetch(
    `${API_URL}/documents/${documentId}`,
    {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error('Document non trouvé');
  }

  return response.json();
}

/**
 * Met à jour le contenu d'un document
 */
export async function updateDocument(
  documentId: string,
  content: string,
  token: string
): Promise<GeneratedDocument> {
  const response = await fetch(
    `${API_URL}/documents/${documentId}`,
    {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content }),
    }
  );

  if (!response.ok) {
    throw new Error('Erreur lors de la mise à jour');
  }

  return response.json();
}

/**
 * Supprime un document
 */
export async function deleteDocument(
  documentId: string,
  token: string
): Promise<void> {
  const response = await fetch(
    `${API_URL}/documents/${documentId}`,
    {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error('Erreur lors de la suppression');
  }
}

/**
 * Obtient les statistiques de génération
 */
export async function getDocumentStats(
  token: string
): Promise<DocumentStatsResponse> {
  const response = await fetch(
    `${API_URL}/documents/stats`,
    {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error('Erreur lors de la récupération des statistiques');
  }

  return response.json();
}

/**
 * Télécharge le contenu d'un document
 */
export async function downloadDocument(
  documentId: string,
  token: string
): Promise<{ content: string; filename: string }> {
  const response = await fetch(
    `${API_URL}/documents/${documentId}/download`,
    {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error('Erreur lors du téléchargement');
  }

  return response.json();
}
