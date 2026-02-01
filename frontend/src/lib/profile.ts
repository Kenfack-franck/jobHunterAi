/**
 * Service API pour la gestion des profils
 */
import api from './api';
import {
  Profile,
  ProfileCreate,
  ProfileUpdate,
  Experience,
  ExperienceCreate,
  ExperienceUpdate,
  Education,
  EducationCreate,
  EducationUpdate,
  Skill,
  SkillCreate,
  SkillUpdate
} from '@/types';

class ProfileService {
  // ==================== PROFILE ====================
  
  /**
   * Récupère le profil complet de l'utilisateur connecté
   */
  async getProfile(): Promise<Profile> {
    const response = await api.get<Profile>('/profile');
    return response.data;
  }

  /**
   * Crée le profil de l'utilisateur
   */
  async createProfile(data: ProfileCreate): Promise<Profile> {
    const response = await api.post<Profile>('/profile', data);
    return response.data;
  }

  /**
   * Met à jour le profil de l'utilisateur
   */
  async updateProfile(data: ProfileUpdate): Promise<Profile> {
    const response = await api.put<Profile>('/profile', data);
    return response.data;
  }

  // ==================== EXPERIENCES ====================

  /**
   * Ajoute une expérience professionnelle
   */
  async addExperience(data: ExperienceCreate): Promise<Experience> {
    const response = await api.post<Experience>('/profile/experiences', data);
    return response.data;
  }

  /**
   * Met à jour une expérience
   */
  async updateExperience(id: string, data: ExperienceUpdate): Promise<Experience> {
    const response = await api.put<Experience>(`/profile/experiences/${id}`, data);
    return response.data;
  }

  /**
   * Supprime une expérience
   */
  async deleteExperience(id: string): Promise<void> {
    await api.delete(`/profile/experiences/${id}`);
  }

  // ==================== EDUCATIONS ====================

  /**
   * Ajoute une formation
   */
  async addEducation(data: EducationCreate): Promise<Education> {
    const response = await api.post<Education>('/profile/educations', data);
    return response.data;
  }

  /**
   * Met à jour une formation
   */
  async updateEducation(id: string, data: EducationUpdate): Promise<Education> {
    const response = await api.put<Education>(`/profile/educations/${id}`, data);
    return response.data;
  }

  /**
   * Supprime une formation
   */
  async deleteEducation(id: string): Promise<void> {
    await api.delete(`/profile/educations/${id}`);
  }

  // ==================== SKILLS ====================

  /**
   * Ajoute une compétence
   */
  async addSkill(data: SkillCreate): Promise<Skill> {
    const response = await api.post<Skill>('/profile/skills', data);
    return response.data;
  }

  /**
   * Met à jour une compétence
   */
  async updateSkill(id: string, data: SkillUpdate): Promise<Skill> {
    const response = await api.put<Skill>(`/profile/skills/${id}`, data);
    return response.data;
  }

  /**
   * Supprime une compétence
   */
  async deleteSkill(id: string): Promise<void> {
    await api.delete(`/profile/skills/${id}`);
  }

  // ==================== HELPERS ====================

  /**
   * Vérifie si l'utilisateur a un profil
   */
  async hasProfile(): Promise<boolean> {
    try {
      await this.getProfile();
      return true;
    } catch (error) {
      return false;
    }
  }

  /**
   * Calcule le pourcentage de complétion du profil
   */
  calculateCompletion(profile: Profile): number {
    let completed = 0;
    let total = 7;

    // Champs de base (5 points)
    if (profile.title) completed++;
    if (profile.summary) completed++;
    if (profile.location) completed++;
    if (profile.linkedin_url || profile.github_url || profile.portfolio_url) completed++;
    if (profile.phone) completed++;

    // Relations (2 points)
    if (profile.experiences && profile.experiences.length > 0) completed++;
    if (profile.skills && profile.skills.length > 0) completed++;

    return Math.round((completed / total) * 100);
  }
}

// Export singleton instance
export const profileService = new ProfileService();
export default profileService;
