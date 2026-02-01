"""
Service pour gérer les offres d'emploi
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, func
from typing import Optional, List
from uuid import UUID

from app.models.job_offer import JobOffer
from app.schemas.job_offer import JobOfferCreate, JobOfferUpdate


class JobOfferService:
    """Service pour les opérations CRUD sur les offres d'emploi"""
    
    @staticmethod
    async def get_user_job_offers(
        db: AsyncSession, 
        user_id: UUID,
        limit: int = 20,
        offset: int = 0
    ) -> List[JobOffer]:
        """Récupérer toutes les offres d'un utilisateur"""
        query = (
            select(JobOffer)
            .where(JobOffer.user_id == user_id)
            .order_by(JobOffer.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    @staticmethod
    async def get_job_offer_by_id(
        db: AsyncSession, 
        job_offer_id: UUID, 
        user_id: UUID
    ) -> Optional[JobOffer]:
        """Récupérer une offre par ID (vérification propriétaire)"""
        query = select(JobOffer).where(
            and_(
                JobOffer.id == job_offer_id,
                JobOffer.user_id == user_id
            )
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create_job_offer(
        db: AsyncSession, 
        user_id: UUID, 
        data: JobOfferCreate
    ) -> JobOffer:
        """Créer une nouvelle offre d'emploi"""
        job_offer = JobOffer(
            user_id=user_id,
            company_name=data.company_name,
            job_title=data.job_title,
            location=data.location,
            job_type=data.job_type,
            description=data.description,
            requirements=data.requirements,
            source_url=data.source_url,
            source_platform=data.source_platform,
            extracted_keywords=data.extracted_keywords or []
        )
        db.add(job_offer)
        await db.commit()
        await db.refresh(job_offer)
        return job_offer
    
    @staticmethod
    async def update_job_offer(
        db: AsyncSession,
        job_offer_id: UUID,
        user_id: UUID,
        data: JobOfferUpdate
    ) -> Optional[JobOffer]:
        """Mettre à jour une offre existante"""
        job_offer = await JobOfferService.get_job_offer_by_id(db, job_offer_id, user_id)
        if not job_offer:
            return None
        
        # Mise à jour des champs fournis
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(job_offer, field, value)
        
        await db.commit()
        await db.refresh(job_offer)
        return job_offer
    
    @staticmethod
    async def delete_job_offer(
        db: AsyncSession,
        job_offer_id: UUID,
        user_id: UUID
    ) -> bool:
        """Supprimer une offre"""
        job_offer = await JobOfferService.get_job_offer_by_id(db, job_offer_id, user_id)
        if not job_offer:
            return False
        
        await db.delete(job_offer)
        await db.commit()
        return True
    
    @staticmethod
    async def search_job_offers(
        db: AsyncSession,
        user_id: UUID,
        keyword: Optional[str] = None,
        location: Optional[str] = None,
        job_type: Optional[str] = None,
        company_name: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[JobOffer]:
        """
        Rechercher des offres avec filtres
        Recherche dans: job_title, description, company_name
        """
        query = select(JobOffer).where(JobOffer.user_id == user_id)
        
        # Filtre par mot-clé (recherche dans titre, description)
        if keyword:
            keyword_filter = or_(
                JobOffer.job_title.ilike(f"%{keyword}%"),
                JobOffer.description.ilike(f"%{keyword}%"),
                JobOffer.requirements.ilike(f"%{keyword}%")
            )
            query = query.where(keyword_filter)
        
        # Filtre par localisation
        if location:
            query = query.where(JobOffer.location.ilike(f"%{location}%"))
        
        # Filtre par type de poste
        if job_type:
            query = query.where(JobOffer.job_type.ilike(f"%{job_type}%"))
        
        # Filtre par entreprise
        if company_name:
            query = query.where(JobOffer.company_name.ilike(f"%{company_name}%"))
        
        # Tri et pagination
        query = query.order_by(JobOffer.created_at.desc()).limit(limit).offset(offset)
        
        result = await db.execute(query)
        return list(result.scalars().all())
    
    @staticmethod
    async def count_user_job_offers(db: AsyncSession, user_id: UUID) -> int:
        """Compter le nombre total d'offres d'un utilisateur"""
        query = select(func.count(JobOffer.id)).where(JobOffer.user_id == user_id)
        result = await db.execute(query)
        return result.scalar() or 0
