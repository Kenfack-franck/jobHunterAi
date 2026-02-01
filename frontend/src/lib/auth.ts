/**
 * Service d'authentification
 */
import apiClient from './api';
import { User, RegisterData, LoginData, AuthTokens } from '@/types';

export const authService = {
  /**
   * Inscription d'un nouveau compte
   */
  async register(data: RegisterData): Promise<User> {
    const response = await apiClient.post<User>('/auth/register', data);
    return response.data;
  },

  /**
   * Connexion
   */
  async login(data: LoginData): Promise<AuthTokens> {
    const response = await apiClient.post<AuthTokens>('/auth/login', data);
    return response.data;
  },

  /**
   * Récupérer les informations de l'utilisateur connecté
   */
  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get<User>('/auth/me');
    return response.data;
  },

  /**
   * Rafraîchir le token
   */
  async refreshToken(): Promise<AuthTokens> {
    const response = await apiClient.post<AuthTokens>('/auth/refresh');
    return response.data;
  },

  /**
   * Déconnexion (côté client uniquement)
   */
  logout(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
    }
  },

  /**
   * Sauvegarder le token
   */
  saveToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', token);
    }
  },

  /**
   * Récupérer le token
   */
  getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth_token');
    }
    return null;
  },

  /**
   * Vérifier si l'utilisateur est authentifié
   */
  isAuthenticated(): boolean {
    return !!this.getToken();
  },
};
