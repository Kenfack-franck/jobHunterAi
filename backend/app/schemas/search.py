"""
Schémas Pydantic pour l'API de recherche
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SearchRequest(BaseModel):
    """Requête de recherche avec scraping"""
    keywords: str = Field(..., min_length=2, max_length=200, description="Mots-clés de recherche")
    location: Optional[str] = Field(None, max_length=100, description="Localisation")
    job_type: Optional[str] = Field(None, description="Type de contrat (fulltime, contract, internship, etc.)")
    work_mode: Optional[str] = Field(None, description="Mode de travail (remote, hybrid, onsite)")
    company: Optional[str] = Field(None, max_length=200, description="Nom d'entreprise")
    limit_per_platform: int = Field(100, ge=1, le=200, description="Limite d'offres par plateforme")
    
    class Config:
        json_schema_extra = {
            "example": {
                "keywords": "Python Developer",
                "location": "Remote",
                "job_type": "fulltime",
                "work_mode": "remote",
                "limit_per_platform": 50
            }
        }


class OfferResponse(BaseModel):
    """Offre d'emploi dans la réponse"""
    id: Optional[str] = None
    job_title: str
    company_name: str
    location: str
    description: str
    source_url: str
    source_platform: str
    job_type: Optional[str] = None
    work_mode: Optional[str] = None
    scraped_at: Optional[str] = None
    compatibility_score: Optional[float] = None


class SearchResponse(BaseModel):
    """Réponse de recherche"""
    success: bool
    offers: List[OfferResponse]
    count: int
    scraped_count: Optional[int] = None
    deduplicated_count: Optional[int] = None
    saved_count: Optional[int] = None
    platforms_scraped: Optional[List[str]] = None  # Deprecated, use sources_used
    sources_used: Optional[List[str]] = None  # New multi-source field
    cached: Optional[bool] = False  # Cache hit indicator
    search_params: Optional[dict] = None
    scraped_at: Optional[str] = None
    duration_seconds: Optional[float] = None
    message: Optional[str] = None


class FeedRequest(BaseModel):
    """Requête pour récupérer le feed personnalisé"""
    profile_id: str = Field(..., description="ID du profil candidat")
    limit: int = Field(50, ge=1, le=100, description="Nombre max d'offres")
    min_score: float = Field(60.0, ge=0, le=100, description="Score minimum de compatibilité")
    max_age_days: int = Field(7, ge=1, le=30, description="Âge maximum des offres en jours")
    
    class Config:
        json_schema_extra = {
            "example": {
                "profile_id": "123e4567-e89b-12d3-a456-426614174000",
                "limit": 50,
                "min_score": 70.0,
                "max_age_days": 7
            }
        }


class FeedResponse(BaseModel):
    """Réponse feed personnalisé"""
    success: bool
    offers: List[OfferResponse]
    count: int
    total_analyzed: Optional[int] = None
    min_score_applied: Optional[float] = None
    max_age_days: Optional[int] = None
    message: Optional[str] = None
    error: Optional[str] = None
