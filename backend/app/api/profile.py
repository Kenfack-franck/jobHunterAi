"""
Routes API pour la gestion des profils candidats.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.profile_service import ProfileService
from app.services.cv_parser_service import CVParserService
from app.services.ai_service import AIService
from app.schemas.profile import (
    ProfileCreate, ProfileUpdate, ProfileResponse,
    ExperienceCreate, ExperienceUpdate, ExperienceResponse,
    EducationCreate, EducationUpdate, EducationResponse,
    SkillCreate, SkillUpdate, SkillResponse,
    CVParseResponse
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


# ==================== CV PARSING ROUTE ====================

@router.post("/parse-cv", response_model=CVParseResponse, status_code=status.HTTP_200_OK)
async def parse_cv(
    file: UploadFile = File(..., description="CV au format PDF"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Parse un CV PDF et extrait automatiquement les informations du profil.
    
    Cette route utilise l'IA pour analyser le CV et extraire :
    - Informations personnelles (nom, titre, résumé, contacts)
    - Expériences professionnelles
    - Formations académiques
    - Compétences techniques et soft skills
    
    Le résultat est retourné au format JSON structuré, prêt à être utilisé
    pour pré-remplir le formulaire de profil.
    
    Args:
        file: Fichier PDF du CV (max 10MB)
        
    Returns:
        CVParseResponse avec les données extraites
        
    Raises:
        400: Si le fichier n'est pas un PDF ou est invalide
        413: Si le fichier dépasse 10MB
        500: Si l'analyse échoue
    """
    # Valider le type de fichier
    if not file.content_type == "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seuls les fichiers PDF sont acceptés"
        )
    
    # Valider la taille (10MB max)
    file_size = 0
    chunk_size = 1024 * 1024  # 1MB chunks
    while chunk := await file.read(chunk_size):
        file_size += len(chunk)
        if file_size > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Le fichier ne doit pas dépasser 10MB"
            )
    
    # Remettre le curseur au début
    await file.seek(0)
    
    try:
        # Initialiser les services
        ai_service = AIService()
        cv_parser = CVParserService(ai_service)
        
        # Parser le CV
        profile_data = await cv_parser.parse_cv_pdf(file)
        
        return CVParseResponse(
            success=True,
            message="CV analysé avec succès ! Vérifiez les informations avant de sauvegarder.",
            profile_data=profile_data
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        import logging
        logging.error(f"Erreur parsing CV: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'analyse du CV: {str(e)}"
        )
