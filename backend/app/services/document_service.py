"""
Service pour gérer les documents générés (CRUD + limite génération)
"""
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload

from app.models.generated_document import GeneratedDocument
from app.models.profile import Profile
from app.models.job_offer import JobOffer


class DocumentService:
    """Service pour gérer les documents générés"""
    
    # Limite de génération par jour
    DAILY_GENERATION_LIMIT = 10
    
    @staticmethod
    async def create_document(
        db: AsyncSession,
        user_id: UUID,
        profile_id: UUID,
        job_offer_id: UUID,
        document_type: str,
        content: str,
        generation_params: dict,
        language: str = "fr"
    ) -> GeneratedDocument:
        """
        Crée un nouveau document généré
        
        Args:
            db: Session de base de données
            user_id: ID de l'utilisateur
            profile_id: ID du profil utilisé
            job_offer_id: ID de l'offre ciblée
            document_type: "resume" ou "cover_letter"
            content: Contenu Markdown ou texte brut
            generation_params: Paramètres utilisés (tone, length, etc.)
            language: Langue du document
            
        Returns:
            GeneratedDocument créé
        """
        # Générer un nom de fichier convivial
        job_result = await db.execute(
            select(JobOffer).where(JobOffer.id == job_offer_id)
        )
        job = job_result.scalar_one_or_none()
        
        company_name = (job.company_name or "Entreprise").replace(" ", "_")
        doc_prefix = "CV" if document_type == "resume" else "LM"
        today = datetime.now().strftime("%Y%m%d")
        filename = f"{doc_prefix}_{company_name}_{today}.pdf"
        
        # Créer le document
        document = GeneratedDocument(
            user_id=user_id,
            profile_id=profile_id,
            job_offer_id=job_offer_id,
            document_type=document_type,
            content=content,
            generation_params=generation_params,
            language=language,
            filename=filename
        )
        
        db.add(document)
        await db.commit()
        await db.refresh(document)
        
        return document
    
    @staticmethod
    async def get_document(
        db: AsyncSession,
        document_id: UUID,
        user_id: UUID
    ) -> Optional[GeneratedDocument]:
        """
        Récupère un document par son ID
        
        Args:
            db: Session de base de données
            document_id: ID du document
            user_id: ID de l'utilisateur (sécurité)
            
        Returns:
            GeneratedDocument ou None
        """
        result = await db.execute(
            select(GeneratedDocument)
            .options(
                selectinload(GeneratedDocument.profile),
                selectinload(GeneratedDocument.job_offer)
            )
            .where(
                and_(
                    GeneratedDocument.id == document_id,
                    GeneratedDocument.user_id == user_id
                )
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def list_user_documents(
        db: AsyncSession,
        user_id: UUID,
        document_type: Optional[str] = None,
        limit: int = 50
    ) -> List[GeneratedDocument]:
        """
        Liste les documents d'un utilisateur
        
        Args:
            db: Session de base de données
            user_id: ID de l'utilisateur
            document_type: Filtre par type ("resume" ou "cover_letter")
            limit: Nombre maximum de résultats
            
        Returns:
            Liste de GeneratedDocument
        """
        query = (
            select(GeneratedDocument)
            .options(
                selectinload(GeneratedDocument.job_offer),
                selectinload(GeneratedDocument.profile)
            )
            .where(GeneratedDocument.user_id == user_id)
            .order_by(GeneratedDocument.generated_at.desc())
            .limit(limit)
        )
        
        if document_type:
            query = query.where(GeneratedDocument.document_type == document_type)
        
        result = await db.execute(query)
        return list(result.scalars().all())
    
    @staticmethod
    async def update_document_content(
        db: AsyncSession,
        document_id: UUID,
        user_id: UUID,
        content: str
    ) -> Optional[GeneratedDocument]:
        """
        Met à jour le contenu d'un document
        
        Args:
            db: Session de base de données
            document_id: ID du document
            user_id: ID de l'utilisateur (sécurité)
            content: Nouveau contenu
            
        Returns:
            GeneratedDocument mis à jour ou None
        """
        document = await DocumentService.get_document(db, document_id, user_id)
        if not document:
            return None
        
        document.content = content
        document.updated_at = datetime.now()
        
        await db.commit()
        await db.refresh(document)
        
        return document
    
    @staticmethod
    async def delete_document(
        db: AsyncSession,
        document_id: UUID,
        user_id: UUID
    ) -> bool:
        """
        Supprime un document
        
        Args:
            db: Session de base de données
            document_id: ID du document
            user_id: ID de l'utilisateur (sécurité)
            
        Returns:
            True si supprimé, False sinon
        """
        document = await DocumentService.get_document(db, document_id, user_id)
        if not document:
            return False
        
        await db.delete(document)
        await db.commit()
        
        return True
    
    @staticmethod
    async def check_daily_limit(
        db: AsyncSession,
        user_id: UUID
    ) -> tuple[bool, int]:
        """
        Vérifie si l'utilisateur peut encore générer des documents aujourd'hui
        
        Args:
            db: Session de base de données
            user_id: ID de l'utilisateur
            
        Returns:
            Tuple (can_generate: bool, remaining: int)
        """
        # Compter les documents générés aujourd'hui
        today_start = datetime.combine(date.today(), datetime.min.time())
        
        result = await db.execute(
            select(func.count(GeneratedDocument.id))
            .where(
                and_(
                    GeneratedDocument.user_id == user_id,
                    GeneratedDocument.generated_at >= today_start
                )
            )
        )
        
        count_today = result.scalar() or 0
        remaining = max(0, DocumentService.DAILY_GENERATION_LIMIT - count_today)
        can_generate = remaining > 0
        
        return can_generate, remaining
    
    @staticmethod
    async def get_user_stats(
        db: AsyncSession,
        user_id: UUID
    ) -> dict:
        """
        Obtient les statistiques de génération de l'utilisateur
        
        Args:
            db: Session de base de données
            user_id: ID de l'utilisateur
            
        Returns:
            Dictionnaire avec statistiques
        """
        # Total documents
        total_result = await db.execute(
            select(func.count(GeneratedDocument.id))
            .where(GeneratedDocument.user_id == user_id)
        )
        total = total_result.scalar() or 0
        
        # Documents par type
        type_result = await db.execute(
            select(
                GeneratedDocument.document_type,
                func.count(GeneratedDocument.id)
            )
            .where(GeneratedDocument.user_id == user_id)
            .group_by(GeneratedDocument.document_type)
        )
        by_type = {row[0]: row[1] for row in type_result.all()}
        
        # Limite aujourd'hui
        can_generate, remaining = await DocumentService.check_daily_limit(db, user_id)
        
        return {
            "total_documents": total,
            "resumes": by_type.get("resume", 0),
            "cover_letters": by_type.get("cover_letter", 0),
            "daily_limit": DocumentService.DAILY_GENERATION_LIMIT,
            "remaining_today": remaining,
            "can_generate": can_generate
        }
