from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class SourcePreferencesBase(BaseModel):
    enabled_sources: List[str] = Field(default_factory=list, description="IDs des sources activées")
    priority_sources: List[str] = Field(default_factory=list, description="IDs des sources prioritaires (3-5 max)")
    use_cache: bool = Field(default=True, description="Utiliser le cache")
    cache_ttl_hours: int = Field(default=24, description="Durée du cache en heures")
    max_priority_sources: int = Field(default=3, description="Nombre max de sources prioritaires")
    background_scraping_enabled: bool = Field(default=True, description="Scraping en arrière-plan activé")


class SourcePreferencesCreate(SourcePreferencesBase):
    profile_id: Optional[UUID] = None


class SourcePreferencesUpdate(BaseModel):
    enabled_sources: Optional[List[str]] = None
    priority_sources: Optional[List[str]] = None
    use_cache: Optional[bool] = None
    cache_ttl_hours: Optional[int] = None
    max_priority_sources: Optional[int] = None
    background_scraping_enabled: Optional[bool] = None
    profile_id: Optional[UUID] = None


class SourcePreferencesResponse(SourcePreferencesBase):
    id: UUID
    user_id: UUID
    profile_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PredefinedSourceInfo(BaseModel):
    """Information sur une source prédéfinie"""
    id: str
    name: str
    url: str
    source_type: str
    logo_url: Optional[str] = None
    scraper_type: str
    priority: int
    enabled_by_default: bool


class SourcesListResponse(BaseModel):
    """Liste de toutes les sources prédéfinies"""
    aggregators: List[PredefinedSourceInfo]
    companies: List[PredefinedSourceInfo]
    all_sources: List[PredefinedSourceInfo]
    total_count: int
