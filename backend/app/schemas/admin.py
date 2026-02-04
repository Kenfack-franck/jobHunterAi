"""
Schémas Pydantic pour les routes Admin
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime
import uuid


# Usage stats schema
class UsageStats(BaseModel):
    """Statistiques d'utilisation pour une limite"""
    current: int
    limit: int
    percentage: int


# User response schemas
class UserListItem(BaseModel):
    """Utilisateur dans la liste"""
    id: str
    email: str
    full_name: Optional[str]
    role: str
    is_active: bool
    created_at: datetime
    usage: Dict[str, UsageStats]
    
    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Réponse pour la liste des utilisateurs"""
    users: List[UserListItem]
    total: int
    page: int
    per_page: int
    total_pages: int


class UserDetailResponse(BaseModel):
    """Détails complets d'un utilisateur"""
    id: str
    email: str
    full_name: Optional[str]
    role: str
    is_active: bool
    language: str
    created_at: datetime
    updated_at: Optional[datetime]
    usage: Dict[str, UsageStats]
    custom_limits: Optional[Dict[str, int]]
    
    class Config:
        from_attributes = True


# Update limits request
class UpdateUserLimitsRequest(BaseModel):
    """Requête pour mettre à jour les limites d'un utilisateur"""
    max_saved_offers: Optional[int] = Field(None, ge=1, le=10000)
    max_searches_per_day: Optional[int] = Field(None, ge=1, le=10000)
    max_profiles: Optional[int] = Field(None, ge=1, le=100)
    max_applications: Optional[int] = Field(None, ge=1, le=10000)
    max_cv_parses: Optional[int] = Field(None, ge=1, le=1000)
    max_watched_companies: Optional[int] = Field(None, ge=1, le=1000)
    max_generated_cv_per_day: Optional[int] = Field(None, ge=1, le=100)
    reason: Optional[str] = Field(None, max_length=500, description="Raison de la modification")


# Dashboard stats schemas
class UserNearLimit(BaseModel):
    """Utilisateur approchant d'une limite"""
    email: str
    usage: str


class AdminDashboardStats(BaseModel):
    """Statistiques pour le dashboard admin"""
    total_users: int
    active_users: int
    blocked_users: int
    new_users_this_week: int
    new_users_today: int
    users_near_limit: List[UserNearLimit]
    registrations_last_7_days: Dict[str, int]


# User stats response (for regular users to see their own stats)
class UserStatsResponse(BaseModel):
    """Statistiques d'utilisation pour un utilisateur normal"""
    usage: Dict[str, UsageStats]
    
    class Config:
        from_attributes = True
