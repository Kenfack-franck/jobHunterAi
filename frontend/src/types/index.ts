/**
 * Types TypeScript pour l'application Job Hunter AI
 */

// ============================================
// USER & AUTH TYPES
// ============================================

export interface User {
  id: string;
  email: string;
  full_name?: string | null;
  language: string;
  is_active: boolean;
  created_at: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name?: string;
  language?: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface AuthTokens {
  access_token: string;
  token_type: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

// ============================================
// API RESPONSE TYPES
// ============================================

export interface ApiError {
  detail: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: ApiError;
}

// ============================================
// PROFILE TYPES
// ============================================

export enum SkillLevel {
  BEGINNER = "beginner",
  INTERMEDIATE = "intermediate",
  ADVANCED = "advanced",
  EXPERT = "expert"
}

export enum SkillCategory {
  LANGUAGE = "language",
  FRAMEWORK = "framework",
  TOOL = "tool",
  SOFT_SKILL = "soft_skill",
  OTHER = "other"
}

export interface Skill {
  id: string;
  name: string;
  category: SkillCategory;
  level: SkillLevel;
  created_at: string;
}

export interface SkillCreate {
  name: string;
  category: SkillCategory;
  level: SkillLevel;
}

export interface SkillUpdate {
  name?: string;
  category?: SkillCategory;
  level?: SkillLevel;
}

export interface Education {
  id: string;
  degree: string;
  institution: string;
  field_of_study?: string;
  location?: string;
  start_date: string; // ISO date string
  end_date?: string;
  description?: string;
  created_at: string;
}

export interface EducationCreate {
  degree: string;
  institution: string;
  field_of_study?: string;
  location?: string;
  start_date: string;
  end_date?: string;
  description?: string;
}

export interface EducationUpdate {
  degree?: string;
  institution?: string;
  field_of_study?: string;
  location?: string;
  start_date?: string;
  end_date?: string;
  description?: string;
}

export interface Experience {
  id: string;
  title: string;
  company: string;
  location?: string;
  start_date: string;
  end_date?: string;
  current: boolean;
  description?: string;
  technologies?: string[];
  created_at: string;
}

export interface ExperienceCreate {
  title: string;
  company: string;
  location?: string;
  start_date: string;
  end_date?: string;
  current: boolean;
  description?: string;
  technologies?: string[];
}

export interface ExperienceUpdate {
  title?: string;
  company?: string;
  location?: string;
  start_date?: string;
  end_date?: string;
  current?: boolean;
  description?: string;
  technologies?: string[];
}

export interface Profile {
  id: string;
  user_id: string;
  title: string;
  summary?: string;
  location?: string;
  phone?: string;
  linkedin_url?: string;
  github_url?: string;
  portfolio_url?: string;
  created_at: string;
  updated_at?: string;
  experiences: Experience[];
  educations: Education[];
  skills: Skill[];
}

export interface ProfileCreate {
  title: string;
  summary?: string;
  location?: string;
  phone?: string;
  linkedin_url?: string;
  github_url?: string;
  portfolio_url?: string;
}

export interface ProfileUpdate {
  title?: string;
  summary?: string;
  location?: string;
  phone?: string;
  linkedin_url?: string;
  github_url?: string;
  portfolio_url?: string;
}

// ==================== Job Offers ====================

export interface JobOffer {
  id: string;
  user_id?: string;  // Optionnel : présent seulement si l'offre est sauvegardée
  company_name?: string;
  job_title: string;
  location?: string;
  job_type?: string;
  work_mode?: string;  // "remote", "hybrid", "onsite"
  description?: string;
  requirements?: string;
  source_url?: string;
  source_platform?: string;
  source?: "database" | "scraping";  // Distingue offres DB vs offres scrapées temporaires
  extracted_keywords?: string[];
  analyzed_at?: string;
  created_at?: string;  // Pour offres sauvegardées
  posted_date?: string;  // Pour offres scrapées
  scraped_at?: string;  // Pour offres scrapées
}

export interface JobOfferCreate {
  job_title: string;
  company_name?: string;
  location?: string;
  job_type?: string;
  work_mode?: string;
  description?: string;
  requirements?: string;
  source_url?: string;
  source_platform?: string;
  extracted_keywords?: string[];
}

export interface JobOfferUpdate {
  job_title?: string;
  company_name?: string;
  location?: string;
  job_type?: string;
  work_mode?: string;
  description?: string;
  requirements?: string;
  source_url?: string;
  source_platform?: string;
  extracted_keywords?: string[];
}

export interface JobOfferSearchParams {
  keyword?: string;
  location?: string;
  job_type?: string;
  company_name?: string;
  limit?: number;
  offset?: number;
}

// ==================== Analysis ====================

export interface CompatibilityAnalysis {
  score: number;
  semantic_score: number;
  skill_match_score: number;
  experience_score: number;
  matching_skills: string[];
  missing_skills: string[];
  matching_experiences: string[];
  suggestions: string[];
}

export interface JobRecommendation {
  job_offer_id: string;
  job_title: string;
  company_name?: string;
  location?: string;
  score: number;
}

export interface AnalysisStats {
  total_job_offers: number;
  job_offers_with_embedding: number;
  has_profile: boolean;
  profile_has_embedding: boolean;
  can_analyze: boolean;
}

// ==================== Generated Documents ====================

export interface GeneratedDocument {
  id: string;
  user_id: string;
  profile_id: string;
  job_offer_id: string;
  document_type: "resume" | "cover_letter";
  content: string;
  pdf_path?: string;
  generation_params?: {
    tone?: string;
    language?: string;
    length?: string;
  };
  language: string;
  filename?: string;
  file_size?: number;
  generated_at: string;
  updated_at?: string;
}

export interface DocumentGenerateRequest {
  job_offer_id: string;
  document_type: "resume" | "cover_letter";
  tone?: "professional" | "creative" | "dynamic" | "enthusiastic" | "confident";
  language?: "fr" | "en";
  length?: "short" | "medium" | "long";
}

export interface DocumentStatsResponse {
  total_documents: number;
  resumes: number;
  cover_letters: number;
  daily_limit: number;
  remaining_today: number;
  can_generate: boolean;
}
