"""
Routes API pour l'analyse de compatibilité
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.user import User
from app.models.profile import Profile
from app.models.job_offer import JobOffer
from app.schemas.analysis import CompatibilityAnalysis, JobRecommendation
from app.services.analysis_service import AnalysisService
from app.core.dependencies import get_current_user


router = APIRouter(prefix="/api/v1/analysis", tags=["Analysis"])


@router.post("/jobs/{job_offer_id}/analyze", response_model=CompatibilityAnalysis)
async def analyze_job_compatibility(
    job_offer_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Analyse la compatibilité entre le profil de l'utilisateur et une offre d'emploi
    
    Calcule un score basé sur:
    - Similarité sémantique des embeddings (50%)
    - Correspondance des compétences (35%)
    - Pertinence des expériences (15%)
    
    Retourne également:
    - Liste des compétences qui correspondent
    - Liste des compétences manquantes
    - Expériences pertinentes
    - Suggestions d'amélioration
    """
    
    # Récupérer l'offre
    result = await db.execute(
        select(JobOffer).where(
            JobOffer.id == job_offer_id,
            JobOffer.user_id == current_user.id
        )
    )
    job_offer = result.scalar_one_or_none()
    
    if not job_offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offre d'emploi non trouvée"
        )
    
    # Récupérer le profil avec les relations
    result = await db.execute(
        select(Profile)
        .options(
            selectinload(Profile.experiences),
            selectinload(Profile.skills)
        )
        .where(Profile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil non trouvé. Créez d'abord votre profil."
        )
    
    # Analyser la compatibilité
    analysis_result = await AnalysisService.analyze_compatibility(
        db=db,
        profile=profile,
        job_offer=job_offer
    )
    
    return analysis_result


@router.get("/recommendations", response_model=List[JobRecommendation])
async def get_job_recommendations(
    limit: int = Query(10, ge=1, le=50, description="Nombre de recommandations"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Recommande les offres d'emploi les plus compatibles avec le profil de l'utilisateur
    
    Utilise la recherche vectorielle pgvector pour trouver les offres
    dont l'embedding est le plus proche de celui du profil.
    
    Les offres sont triées par score de compatibilité décroissant.
    """
    
    # Récupérer le profil
    result = await db.execute(
        select(Profile).where(Profile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil non trouvé. Créez d'abord votre profil."
        )
    
    if profile.embedding is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'embedding du profil n'a pas été généré. Mettez à jour votre profil."
        )
    
    # Obtenir les recommandations
    recommendations = await AnalysisService.get_recommendations(
        db=db,
        profile_id=profile.id,
        limit=limit
    )
    
    return recommendations


@router.get("/stats", response_model=dict)
async def get_analysis_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Statistiques sur l'analyse et les recommandations
    
    Retourne:
    - Nombre total d'offres
    - Nombre d'offres avec embedding
    - État du profil
    """
    from sqlalchemy import func
    
    # Compter les offres
    result = await db.execute(
        select(func.count(JobOffer.id)).where(JobOffer.user_id == current_user.id)
    )
    total_offers = result.scalar() or 0
    
    # Compter les offres avec embedding
    result = await db.execute(
        select(func.count(JobOffer.id)).where(
            JobOffer.user_id == current_user.id,
            JobOffer.embedding.is_not(None)
        )
    )
    offers_with_embedding = result.scalar() or 0
    
    # Vérifier le profil
    result = await db.execute(
        select(Profile).where(Profile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    has_profile = profile is not None
    profile_has_embedding = has_profile and profile.embedding is not None
    
    return {
        "total_job_offers": total_offers,
        "job_offers_with_embedding": offers_with_embedding,
        "has_profile": has_profile,
        "profile_has_embedding": profile_has_embedding,
        "can_analyze": has_profile and profile_has_embedding and offers_with_embedding > 0
    }
