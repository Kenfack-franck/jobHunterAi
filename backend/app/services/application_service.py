"""
Application Service - Gestion des candidatures
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime

from app.models.application import Application, ApplicationStatus
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationStats
)


class ApplicationService:
    """Service pour gérer les candidatures"""

    @staticmethod
    async def create_application(
        db: AsyncSession,
        user_id: UUID,
        application_data: ApplicationCreate
    ) -> Application:
        """Créer une nouvelle candidature"""
        application = Application(
            user_id=user_id,
            company_name=application_data.company_name,
            job_title=application_data.job_title,
            email_to=application_data.email_to,
            status="pending",
            notes=application_data.notes,
            job_offer_id=application_data.job_offer_id,
            documents_sent=None
        )
        
        db.add(application)
        await db.commit()
        await db.refresh(application)
        
        return application

    @staticmethod
    async def get_user_applications(
        db: AsyncSession,
        user_id: UUID,
        status: Optional[ApplicationStatus] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Application]:
        """Récupérer les candidatures d'un utilisateur"""
        query = select(Application).where(Application.user_id == user_id)
        
        if status:
            query = query.where(Application.status == status.value)
        
        query = query.order_by(Application.applied_at.desc())
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_application_by_id(
        db: AsyncSession,
        application_id: UUID,
        user_id: UUID
    ) -> Optional[Application]:
        """Récupérer une candidature par ID"""
        query = select(Application).where(
            and_(
                Application.id == application_id,
                Application.user_id == user_id
            )
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def update_application(
        db: AsyncSession,
        application_id: UUID,
        user_id: UUID,
        update_data: ApplicationUpdate
    ) -> Optional[Application]:
        """Mettre à jour une candidature"""
        application = await ApplicationService.get_application_by_id(
            db, application_id, user_id
        )
        
        if not application:
            return None
        
        if update_data.status:
            application.status = update_data.status.value
        if update_data.notes is not None:
            application.notes = update_data.notes
        
        application.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(application)
        
        return application

    @staticmethod
    async def delete_application(
        db: AsyncSession,
        application_id: UUID,
        user_id: UUID
    ) -> bool:
        """Supprimer une candidature"""
        application = await ApplicationService.get_application_by_id(
            db, application_id, user_id
        )
        
        if not application:
            return False
        
        await db.delete(application)
        await db.commit()
        
        return True

    @staticmethod
    async def get_applications_stats(
        db: AsyncSession,
        user_id: UUID
    ) -> ApplicationStats:
        """Calculer les statistiques des candidatures"""
        # Total
        total_query = select(func.count(Application.id)).where(
            Application.user_id == user_id
        )
        total_result = await db.execute(total_query)
        total = total_result.scalar() or 0
        
        # Par statut
        stats = {}
        for status in ApplicationStatus:
            status_query = select(func.count(Application.id)).where(
                and_(
                    Application.user_id == user_id,
                    Application.status == status.value
                )
            )
            status_result = await db.execute(status_query)
            stats[status.value] = status_result.scalar() or 0
        
        # Taux de réponse
        responded = total - stats.get("pending", 0)
        response_rate = (responded / total * 100) if total > 0 else 0.0
        
        return ApplicationStats(
            total=total,
            by_status=stats,
            response_rate=round(response_rate, 1)
        )
