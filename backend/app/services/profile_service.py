"""
Service métier pour la gestion des profils candidats.
"""
from uuid import UUID
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models.profile import Profile, Experience, Education, Skill
from app.schemas.profile import (
    ProfileCreate, ProfileUpdate,
    ExperienceCreate, ExperienceUpdate,
    EducationCreate, EducationUpdate,
    SkillCreate, SkillUpdate
)


class ProfileService:
    """Service pour gérer les profils candidats"""
    
    @staticmethod
    async def get_user_profile(user_id: UUID, db: AsyncSession) -> Optional[Profile]:
        """
        Récupère le profil complet d'un utilisateur avec toutes ses relations.
        
        Args:
            user_id: ID de l'utilisateur
            db: Session de base de données
            
        Returns:
            Profile ou None si pas de profil
        """
        query = (
            select(Profile)
            .options(
                selectinload(Profile.experiences),
                selectinload(Profile.educations),
                selectinload(Profile.skills)
            )
            .where(Profile.user_id == user_id)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create_profile(user_id: UUID, data: ProfileCreate, db: AsyncSession) -> Profile:
        """
        Crée un nouveau profil pour un utilisateur.
        
        Args:
            user_id: ID de l'utilisateur
            data: Données du profil
            db: Session de base de données
            
        Returns:
            Profile créé
            
        Raises:
            HTTPException: Si un profil existe déjà
        """
        # Vérifier qu'un profil n'existe pas déjà
        existing = await ProfileService.get_user_profile(user_id, db)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Profile already exists for this user"
            )
        
        # Créer le profil
        profile = Profile(
            user_id=user_id,
            **data.model_dump()
        )
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
        
        # Recharger avec les relations
        return await ProfileService.get_user_profile(user_id, db)
    
    @staticmethod
    async def update_profile(
        user_id: UUID,
        data: ProfileUpdate,
        db: AsyncSession
    ) -> Profile:
        """
        Met à jour le profil d'un utilisateur.
        
        Args:
            user_id: ID de l'utilisateur
            data: Données à mettre à jour
            db: Session de base de données
            
        Returns:
            Profile mis à jour
            
        Raises:
            HTTPException: Si le profil n'existe pas
        """
        profile = await ProfileService.get_user_profile(user_id, db)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        
        # Mettre à jour les champs non-None
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(profile, field, value)
        
        await db.commit()
        await db.refresh(profile)
        
        # Recharger avec les relations
        return await ProfileService.get_user_profile(user_id, db)
    
    # ==================== EXPERIENCES ====================
    
    @staticmethod
    async def add_experience(
        user_id: UUID,
        data: ExperienceCreate,
        db: AsyncSession
    ) -> Experience:
        """
        Ajoute une expérience au profil de l'utilisateur.
        
        Args:
            user_id: ID de l'utilisateur
            data: Données de l'expérience
            db: Session de base de données
            
        Returns:
            Experience créée
            
        Raises:
            HTTPException: Si le profil n'existe pas
        """
        profile = await ProfileService.get_user_profile(user_id, db)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found. Create a profile first."
            )
        
        # Convertir date -> datetime pour la base de données
        from datetime import datetime, time
        exp_data = data.model_dump()
        if exp_data.get('start_date'):
            exp_data['start_date'] = datetime.combine(exp_data['start_date'], time.min)
        if exp_data.get('end_date'):
            exp_data['end_date'] = datetime.combine(exp_data['end_date'], time.min)
        
        experience = Experience(
            profile_id=profile.id,
            **exp_data
        )
        db.add(experience)
        await db.commit()
        await db.refresh(experience)
        
        return experience
    
    @staticmethod
    async def update_experience(
        experience_id: UUID,
        user_id: UUID,
        data: ExperienceUpdate,
        db: AsyncSession
    ) -> Experience:
        """
        Met à jour une expérience.
        
        Args:
            experience_id: ID de l'expérience
            user_id: ID de l'utilisateur (pour vérifier la propriété)
            data: Données à mettre à jour
            db: Session de base de données
            
        Returns:
            Experience mise à jour
            
        Raises:
            HTTPException: Si l'expérience n'existe pas ou n'appartient pas à l'utilisateur
        """
        # Récupérer l'expérience avec son profil
        query = (
            select(Experience)
            .join(Profile)
            .where(Experience.id == experience_id)
            .where(Profile.user_id == user_id)
        )
        result = await db.execute(query)
        experience = result.scalar_one_or_none()
        
        if not experience:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Experience not found"
            )
        
        # Mettre à jour les champs non-None
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(experience, field, value)
        
        await db.commit()
        await db.refresh(experience)
        
        return experience
    
    @staticmethod
    async def delete_experience(
        experience_id: UUID,
        user_id: UUID,
        db: AsyncSession
    ) -> None:
        """
        Supprime une expérience.
        
        Args:
            experience_id: ID de l'expérience
            user_id: ID de l'utilisateur (pour vérifier la propriété)
            db: Session de base de données
            
        Raises:
            HTTPException: Si l'expérience n'existe pas ou n'appartient pas à l'utilisateur
        """
        # Vérifier que l'expérience appartient à l'utilisateur
        query = (
            select(Experience)
            .join(Profile)
            .where(Experience.id == experience_id)
            .where(Profile.user_id == user_id)
        )
        result = await db.execute(query)
        experience = result.scalar_one_or_none()
        
        if not experience:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Experience not found"
            )
        
        await db.delete(experience)
        await db.commit()
    
    # ==================== EDUCATIONS ====================
    
    @staticmethod
    async def add_education(
        user_id: UUID,
        data: EducationCreate,
        db: AsyncSession
    ) -> Education:
        """
        Ajoute une formation au profil de l'utilisateur.
        """
        profile = await ProfileService.get_user_profile(user_id, db)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found. Create a profile first."
            )
        
        # Convertir date -> datetime pour la base de données
        from datetime import datetime, time
        edu_data = data.model_dump()
        if edu_data.get('start_date'):
            edu_data['start_date'] = datetime.combine(edu_data['start_date'], time.min)
        if edu_data.get('end_date'):
            edu_data['end_date'] = datetime.combine(edu_data['end_date'], time.min)
        
        education = Education(
            profile_id=profile.id,
            **edu_data
        )
        db.add(education)
        await db.commit()
        await db.refresh(education)
        
        return education
    
    @staticmethod
    async def update_education(
        education_id: UUID,
        user_id: UUID,
        data: EducationUpdate,
        db: AsyncSession
    ) -> Education:
        """
        Met à jour une formation.
        """
        query = (
            select(Education)
            .join(Profile)
            .where(Education.id == education_id)
            .where(Profile.user_id == user_id)
        )
        result = await db.execute(query)
        education = result.scalar_one_or_none()
        
        if not education:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Education not found"
            )
        
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(education, field, value)
        
        await db.commit()
        await db.refresh(education)
        
        return education
    
    @staticmethod
    async def delete_education(
        education_id: UUID,
        user_id: UUID,
        db: AsyncSession
    ) -> None:
        """
        Supprime une formation.
        """
        query = (
            select(Education)
            .join(Profile)
            .where(Education.id == education_id)
            .where(Profile.user_id == user_id)
        )
        result = await db.execute(query)
        education = result.scalar_one_or_none()
        
        if not education:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Education not found"
            )
        
        await db.delete(education)
        await db.commit()
    
    # ==================== SKILLS ====================
    
    @staticmethod
    async def add_skill(
        user_id: UUID,
        data: SkillCreate,
        db: AsyncSession
    ) -> Skill:
        """
        Ajoute une compétence au profil de l'utilisateur.
        """
        profile = await ProfileService.get_user_profile(user_id, db)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found. Create a profile first."
            )
        
        skill = Skill(
            profile_id=profile.id,
            **data.model_dump()
        )
        db.add(skill)
        await db.commit()
        await db.refresh(skill)
        
        return skill
    
    @staticmethod
    async def update_skill(
        skill_id: UUID,
        user_id: UUID,
        data: SkillUpdate,
        db: AsyncSession
    ) -> Skill:
        """
        Met à jour une compétence.
        """
        query = (
            select(Skill)
            .join(Profile)
            .where(Skill.id == skill_id)
            .where(Profile.user_id == user_id)
        )
        result = await db.execute(query)
        skill = result.scalar_one_or_none()
        
        if not skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill not found"
            )
        
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(skill, field, value)
        
        await db.commit()
        await db.refresh(skill)
        
        return skill
    
    @staticmethod
    async def delete_skill(
        skill_id: UUID,
        user_id: UUID,
        db: AsyncSession
    ) -> None:
        """
        Supprime une compétence.
        """
        query = (
            select(Skill)
            .join(Profile)
            .where(Skill.id == skill_id)
            .where(Profile.user_id == user_id)
        )
        result = await db.execute(query)
        skill = result.scalar_one_or_none()
        
        if not skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill not found"
            )
        
        await db.delete(skill)
        await db.commit()
