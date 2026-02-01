"""
Schémas Pydantic pour l'analyse de compatibilité
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID


class CompatibilityAnalysis(BaseModel):
    """Résultat de l'analyse de compatibilité"""
    score: float = Field(..., ge=0, le=100, description="Score global de compatibilité (0-100)")
    semantic_score: float = Field(..., ge=0, le=100, description="Score de similarité sémantique")
    skill_match_score: float = Field(..., ge=0, le=100, description="Score de correspondance des compétences")
    experience_score: float = Field(..., ge=0, le=100, description="Score de pertinence des expériences")
    
    matching_skills: List[str] = Field(default_factory=list, description="Compétences qui correspondent")
    missing_skills: List[str] = Field(default_factory=list, description="Compétences manquantes")
    matching_experiences: List[str] = Field(default_factory=list, description="Expériences pertinentes")
    
    suggestions: List[str] = Field(default_factory=list, description="Suggestions d'amélioration")


class JobRecommendation(BaseModel):
    """Recommandation d'offre d'emploi"""
    job_offer_id: UUID
    job_title: str
    company_name: Optional[str] = None
    location: Optional[str] = None
    score: float = Field(..., ge=0, le=100, description="Score de compatibilité")
