"""
Routes API pour la gestion des profils candidats.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.profile_service import ProfileService
from app.schemas.profile import (
    ProfileCreate, ProfileUpdate, ProfileResponse,
    ExperienceCreate, ExperienceUpdate, ExperienceResponse,
    EducationCreate, EducationUpdate, EducationResponse,
    SkillCreate, SkillUpdate, SkillResponse
)


router = APIRouter(prefix="/profile", tags=["Profile"])


# ==================== PROFILE ROUTES ====================

@router.get("", response_model=ProfileResponse, status_code=status.HTTP_200_OK)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Récupère le profil complet de l'utilisateur connecté.
    
    Returns:
        ProfileResponse avec toutes les relations (experiences, educations, skills)
    """
    profile = await ProfileService.get_user_profile(current_user.id, db)
    
    if not profile:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Create your profile first."
        )
    
    return profile


@router.post("", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Crée le profil de l'utilisateur connecté.
    
    Args:
        data: Données du profil (title, summary, location, etc.)
        
    Returns:
        ProfileResponse créé
        
    Raises:
        400: Si un profil existe déjà
    """
    profile = await ProfileService.create_profile(current_user.id, data, db)
    return profile


@router.put("", response_model=ProfileResponse, status_code=status.HTTP_200_OK)
async def update_profile(
    data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Met à jour le profil de l'utilisateur connecté.
    
    Args:
        data: Données à mettre à jour (seuls les champs fournis sont modifiés)
        
    Returns:
        ProfileResponse mis à jour
        
    Raises:
        404: Si le profil n'existe pas
    """
    profile = await ProfileService.update_profile(current_user.id, data, db)
    return profile


# ==================== EXPERIENCE ROUTES ====================

@router.post("/experiences", response_model=ExperienceResponse, status_code=status.HTTP_201_CREATED)
async def add_experience(
    data: ExperienceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Ajoute une expérience professionnelle au profil.
    
    Args:
        data: Données de l'expérience (title, company, dates, description, technologies)
        
    Returns:
        ExperienceResponse créée
        
    Raises:
        404: Si le profil n'existe pas
    """
    experience = await ProfileService.add_experience(current_user.id, data, db)
    return experience


@router.put("/experiences/{experience_id}", response_model=ExperienceResponse, status_code=status.HTTP_200_OK)
async def update_experience(
    experience_id: UUID,
    data: ExperienceUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Met à jour une expérience professionnelle.
    
    Args:
        experience_id: ID de l'expérience à modifier
        data: Données à mettre à jour
        
    Returns:
        ExperienceResponse mise à jour
        
    Raises:
        404: Si l'expérience n'existe pas ou n'appartient pas à l'utilisateur
    """
    experience = await ProfileService.update_experience(experience_id, current_user.id, data, db)
    return experience


@router.delete("/experiences/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experience(
    experience_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Supprime une expérience professionnelle.
    
    Args:
        experience_id: ID de l'expérience à supprimer
        
    Raises:
        404: Si l'expérience n'existe pas ou n'appartient pas à l'utilisateur
    """
    await ProfileService.delete_experience(experience_id, current_user.id, db)
    return None


# ==================== EDUCATION ROUTES ====================

@router.post("/educations", response_model=EducationResponse, status_code=status.HTTP_201_CREATED)
async def add_education(
    data: EducationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Ajoute une formation au profil.
    
    Args:
        data: Données de la formation (degree, institution, dates, description)
        
    Returns:
        EducationResponse créée
        
    Raises:
        404: Si le profil n'existe pas
    """
    education = await ProfileService.add_education(current_user.id, data, db)
    return education


@router.put("/educations/{education_id}", response_model=EducationResponse, status_code=status.HTTP_200_OK)
async def update_education(
    education_id: UUID,
    data: EducationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Met à jour une formation.
    
    Args:
        education_id: ID de la formation à modifier
        data: Données à mettre à jour
        
    Returns:
        EducationResponse mise à jour
        
    Raises:
        404: Si la formation n'existe pas ou n'appartient pas à l'utilisateur
    """
    education = await ProfileService.update_education(education_id, current_user.id, data, db)
    return education


@router.delete("/educations/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_education(
    education_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Supprime une formation.
    
    Args:
        education_id: ID de la formation à supprimer
        
    Raises:
        404: Si la formation n'existe pas ou n'appartient pas à l'utilisateur
    """
    await ProfileService.delete_education(education_id, current_user.id, db)
    return None


# ==================== SKILL ROUTES ====================

@router.post("/skills", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
async def add_skill(
    data: SkillCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Ajoute une compétence au profil.
    
    Args:
        data: Données de la compétence (name, category, level)
        
    Returns:
        SkillResponse créée
        
    Raises:
        404: Si le profil n'existe pas
    """
    skill = await ProfileService.add_skill(current_user.id, data, db)
    return skill


@router.put("/skills/{skill_id}", response_model=SkillResponse, status_code=status.HTTP_200_OK)
async def update_skill(
    skill_id: UUID,
    data: SkillUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Met à jour une compétence.
    
    Args:
        skill_id: ID de la compétence à modifier
        data: Données à mettre à jour
        
    Returns:
        SkillResponse mise à jour
        
    Raises:
        404: Si la compétence n'existe pas ou n'appartient pas à l'utilisateur
    """
    skill = await ProfileService.update_skill(skill_id, current_user.id, data, db)
    return skill


@router.delete("/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(
    skill_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Supprime une compétence.
    
    Args:
        skill_id: ID de la compétence à supprimer
        
    Raises:
        404: Si la compétence n'existe pas ou n'appartient pas à l'utilisateur
    """
    await ProfileService.delete_skill(skill_id, current_user.id, db)
    return None
