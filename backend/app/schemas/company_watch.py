"""
Schémas Pydantic pour la veille entreprise
"""
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class AddWatchRequest(BaseModel):
    """Requête pour ajouter une veille entreprise"""
    company_name: str = Field(..., min_length=2, max_length=200, description="Nom de l'entreprise")
    profile_id: Optional[UUID] = Field(None, description="ID du profil pour scoring")
    alert_threshold: int = Field(70, ge=0, le=100, description="Score minimum pour alerte")
    linkedin_url: Optional[str] = Field(None, max_length=500, description="URL LinkedIn entreprise")
    careers_url: Optional[str] = Field(None, max_length=500, description="URL page carrières")


class WatchResponse(BaseModel):
    """Réponse après ajout/modification d'une veille"""
    success: bool
    message: str
    watch_id: Optional[str] = None
    company_id: Optional[str] = None
    company_slug: Optional[str] = None
    total_watchers: Optional[int] = None


class WatchItem(BaseModel):
    """Une veille entreprise"""
    watch_id: str
    company_id: str
    company_name: str
    company_slug: str
    alert_threshold: int
    profile_id: Optional[str] = None
    total_watchers: int
    total_offers_found: int
    last_scraped_at: Optional[str] = None
    linkedin_url: Optional[str] = None
    careers_url: Optional[str] = None
    created_at: str


class WatchListResponse(BaseModel):
    """Liste des veilles d'un utilisateur"""
    success: bool
    watches: List[WatchItem]
    count: int
    total: int
    page: int
    per_page: int


class CompanyOffer(BaseModel):
    """Une offre d'emploi d'une entreprise"""
    id: str
    title: str
    company: str
    location: Optional[str] = None
    job_type: Optional[str] = None
    work_mode: Optional[str] = None
    url: Optional[str] = None
    scraped_at: Optional[str] = None
    compatibility_score: Optional[float] = None


class CompanyOffersResponse(BaseModel):
    """Liste des offres d'une entreprise surveillée"""
    success: bool
    company_name: str
    company_slug: str
    offers: List[CompanyOffer]
    count: int
    total_offers_found: int
    last_scraped_at: Optional[str] = None
