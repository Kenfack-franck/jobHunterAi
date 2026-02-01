"""
Schémas Pydantic pour JobOffer
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class JobOfferBase(BaseModel):
    """Champs de base pour une offre d'emploi"""
    company_name: Optional[str] = Field(None, max_length=255)
    job_title: str = Field(..., min_length=1, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    job_type: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    requirements: Optional[str] = None
    source_url: Optional[str] = Field(None, max_length=1000)
    source_platform: Optional[str] = Field(None, max_length=100)
    extracted_keywords: Optional[List[str]] = Field(default_factory=list)


class JobOfferCreate(JobOfferBase):
    """Création d'une offre d'emploi"""
    pass


class JobOfferUpdate(BaseModel):
    """Mise à jour d'une offre d'emploi"""
    company_name: Optional[str] = Field(None, max_length=255)
    job_title: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    job_type: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    requirements: Optional[str] = None
    source_url: Optional[str] = Field(None, max_length=1000)
    source_platform: Optional[str] = Field(None, max_length=100)
    extracted_keywords: Optional[List[str]] = None


class JobOfferResponse(JobOfferBase):
    """Réponse avec une offre d'emploi"""
    id: UUID
    user_id: UUID
    analyzed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class JobOfferSearchParams(BaseModel):
    """Paramètres de recherche d'offres"""
    keyword: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    company_name: Optional[str] = None
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)
