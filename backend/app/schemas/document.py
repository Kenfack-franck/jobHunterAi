"""
Schémas Pydantic pour les documents générés
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from uuid import UUID


class DocumentGenerateRequest(BaseModel):
    """Requête de génération de document"""
    job_offer_id: UUID
    document_type: Literal["resume", "cover_letter"]
    tone: Optional[Literal["professional", "creative", "dynamic", "enthusiastic", "confident"]] = "professional"
    language: Optional[Literal["fr", "en"]] = "fr"
    length: Optional[Literal["short", "medium", "long"]] = "medium"  # Pour les lettres


class DocumentUpdateRequest(BaseModel):
    """Requête de mise à jour de contenu"""
    content: str = Field(..., min_length=10)


class DocumentResponse(BaseModel):
    """Réponse avec un document"""
    id: UUID
    user_id: UUID
    profile_id: UUID
    job_offer_id: UUID
    document_type: str
    content: str
    pdf_path: Optional[str] = None
    generation_params: Optional[dict] = None
    language: str
    filename: Optional[str] = None
    file_size: Optional[int] = None
    generated_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class DocumentStatsResponse(BaseModel):
    """Statistiques de génération de l'utilisateur"""
    total_documents: int
    resumes: int
    cover_letters: int
    daily_limit: int
    remaining_today: int
    can_generate: bool
