"""
Applications API endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.application import ApplicationStatus
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    ApplicationStats
)
from app.services.application_service import ApplicationService
from app.services.limit_service import LimitService

router = APIRouter()


@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(
    application_data: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer une nouvelle candidature"""
    # Vérifier la limite de candidatures
    limit_service = LimitService(db)
    can_proceed, current_count, max_val = await limit_service.check_limit(
        user_id=current_user.id,
        limit_type="applications"
    )
    
    if not can_proceed:
        raise HTTPException(
            status_code=429,
            detail=f"Limite de candidatures atteinte ({current_count}/{max_val}). Plan gratuit limité à {max_val} candidatures."
        )
    
    application = await ApplicationService.create_application(
        db=db,
        user_id=current_user.id,
        application_data=application_data
    )
    
    # Incrémenter le compteur
    await limit_service.increment(
        user_id=current_user.id,
        limit_type="applications"
    )
    
    return application


@router.get("/", response_model=List[ApplicationResponse])
async def get_applications(
    status: Optional[ApplicationStatus] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer toutes les candidatures"""
    applications = await ApplicationService.get_user_applications(
        db=db,
        user_id=current_user.id,
        status=status,
        skip=skip,
        limit=limit
    )
    return applications


@router.get("/stats", response_model=ApplicationStats)
async def get_applications_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Statistiques candidatures"""
    stats = await ApplicationService.get_applications_stats(
        db=db,
        user_id=current_user.id
    )
    return stats


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer une candidature"""
    application = await ApplicationService.get_application_by_id(
        db=db,
        application_id=application_id,
        user_id=current_user.id
    )
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidature non trouvée"
        )
    
    return application


@router.put("/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: UUID,
    update_data: ApplicationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mettre à jour candidature"""
    application = await ApplicationService.update_application(
        db=db,
        application_id=application_id,
        user_id=current_user.id,
        update_data=update_data
    )
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidature non trouvée"
        )
    
    return application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(
    application_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprimer candidature"""
    success = await ApplicationService.delete_application(
        db=db,
        application_id=application_id,
        user_id=current_user.id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidature non trouvée"
        )
    
    return None
