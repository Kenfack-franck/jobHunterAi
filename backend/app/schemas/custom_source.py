"""
Schémas Pydantic pour la gestion des sources personnalisées.
"""
from pydantic import BaseModel, HttpUrl, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class SourceType(str, Enum):
    """Types de sources custom."""
    CAREER_PAGE = "career_page"
    JOB_BOARD = "job_board"
    ATS_PLATFORM = "ats_platform"
    UNKNOWN = "unknown"


class ScrapingFrequency(str, Enum):
    """Fréquences de scraping."""
    HOURLY = "hourly"
    EVERY_4_HOURS = "every_4_hours"
    DAILY = "daily"
    WEEKLY = "weekly"


class SourceAnalysis(BaseModel):
    """Résultat de l'analyse d'une URL."""
    is_accessible: bool
    content_type: str
    has_jobs: bool
    job_keywords_found: List[str]
    estimated_job_count: Optional[int] = None
    has_anti_bot: bool
    anti_bot_indicators: List[str]
    recommendation: str
    is_scrapable: bool


class AddCustomSourceRequest(BaseModel):
    """Requête pour ajouter une source personnalisée."""
    source_name: str = Field(..., min_length=1, max_length=100, description="Nom de la source (ex: 'Google Careers')")
    source_url: HttpUrl = Field(..., description="URL de la source (ex: 'https://careers.google.com')")
    scraping_frequency: ScrapingFrequency = Field(
        default=ScrapingFrequency.EVERY_4_HOURS,
        description="Fréquence de scraping souhaitée"
    )
    
    @field_validator('source_url')
    @classmethod
    def validate_url(cls, v):
        """Valide que l'URL est bien formée."""
        url_str = str(v)
        if not (url_str.startswith('http://') or url_str.startswith('https://')):
            raise ValueError("L'URL doit commencer par http:// ou https://")
        return v


class CustomSourceResponse(BaseModel):
    """Réponse avec les détails d'une source."""
    id: int
    user_id: str  # UUID as string
    source_name: str
    source_url: str
    source_type: str
    is_active: bool
    scraping_frequency: str
    created_at: datetime
    last_scraped_at: Optional[datetime] = None
    total_offers_found: int = 0
    
    # Analyse de l'URL (si disponible)
    analysis: Optional[SourceAnalysis] = None
    
    class Config:
        from_attributes = True


class CustomSourceListResponse(BaseModel):
    """Liste des sources avec pagination."""
    sources: List[CustomSourceResponse]
    total: int
    page: int
    per_page: int


class TestSourceResponse(BaseModel):
    """Résultat du test d'une source."""
    success: bool
    analysis: SourceAnalysis
    message: str


class UpdateCustomSourceRequest(BaseModel):
    """Requête pour mettre à jour une source."""
    source_name: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None
    scraping_frequency: Optional[ScrapingFrequency] = None


class DeleteSourceResponse(BaseModel):
    """Réponse après suppression d'une source."""
    success: bool
    message: str
