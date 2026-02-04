/**
 * Service Admin - Gestion des utilisateurs et statistiques
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface UsageStats {
  current: number;
  limit: number;
  percentage: number;
}

export interface UserListItem {
  id: string;
  email: string;
  full_name: string | null;
  role: string;
  is_active: boolean;
  created_at: string;
  usage: Record<string, UsageStats>;
}

export interface UserListResponse {
  users: UserListItem[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export interface UserDetailResponse {
  id: string;
  email: string;
  full_name: string | null;
  role: string;
  is_active: boolean;
  language: string;
  created_at: string;
  updated_at: string | null;
  usage: Record<string, UsageStats>;
  custom_limits: Record<string, number> | null;
}

export interface UpdateLimitsRequest {
  max_saved_offers?: number;
  max_searches_per_day?: number;
  max_profiles?: number;
  max_applications?: number;
  max_cv_parses?: number;
  max_watched_companies?: number;
  max_generated_cv_per_day?: number;
  reason?: string;
}

export interface UserNearLimit {
  email: string;
  usage: string;
}

export interface AdminDashboardStats {
  total_users: number;
  active_users: number;
  blocked_users: number;
  new_users_this_week: number;
  new_users_today: number;
  users_near_limit: UserNearLimit[];
  registrations_last_7_days: Record<string, number>;
}

export interface AdminFilters {
  search?: string;
  role?: 'user' | 'admin';
  is_active?: boolean;
  page?: number;
  per_page?: number;
}

class AdminService {
  /**
   * Récupère la liste des utilisateurs avec filtres
   */
  async getUsers(filters: AdminFilters = {}): Promise<UserListResponse> {
    const token = localStorage.getItem('token');
    
    const params = new URLSearchParams();
    if (filters.search) params.append('search', filters.search);
    if (filters.role) params.append('role', filters.role);
    if (filters.is_active !== undefined) params.append('is_active', String(filters.is_active));
    if (filters.page) params.append('page', String(filters.page));
    if (filters.per_page) params.append('per_page', String(filters.per_page));
    
    const response = await fetch(`${API_URL}/api/v1/admin/users?${params}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Erreur lors de la récupération des utilisateurs');
    }
    
    return response.json();
  }

  /**
   * Récupère les détails d'un utilisateur
   */
  async getUserDetail(userId: string): Promise<UserDetailResponse> {
    const token = localStorage.getItem('token');
    
    const response = await fetch(`${API_URL}/api/v1/admin/users/${userId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Erreur lors de la récupération de l\'utilisateur');
    }
    
    return response.json();
  }

  /**
   * Bloquer/Débloquer un utilisateur
   */
  async toggleUserActive(userId: string): Promise<UserDetailResponse> {
    const token = localStorage.getItem('token');
    
    const response = await fetch(`${API_URL}/api/v1/admin/users/${userId}/toggle-active`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Erreur lors de la modification de l\'utilisateur');
    }
    
    return response.json();
  }

  /**
   * Supprimer un utilisateur
   */
  async deleteUser(userId: string): Promise<void> {
    const token = localStorage.getItem('token');
    
    const response = await fetch(`${API_URL}/api/v1/admin/users/${userId}?confirm=yes`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Erreur lors de la suppression de l\'utilisateur');
    }
  }

  /**
   * Modifier les limites d'un utilisateur
   */
  async updateUserLimits(userId: string, limits: UpdateLimitsRequest): Promise<UserDetailResponse> {
    const token = localStorage.getItem('token');
    
    const response = await fetch(`${API_URL}/api/v1/admin/users/${userId}/limits`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(limits),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Erreur lors de la modification des limites');
    }
    
    return response.json();
  }

  /**
   * Récupère les statistiques du dashboard admin
   */
  async getDashboardStats(): Promise<AdminDashboardStats> {
    const token = localStorage.getItem('token');
    
    const response = await fetch(`${API_URL}/api/v1/admin/stats`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Erreur lors de la récupération des statistiques');
    }
    
    return response.json();
  }
}

export const adminService = new AdminService();
