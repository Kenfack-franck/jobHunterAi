"""
Routes API pour la génération de documents (CV, Lettres)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
from uuid import UUID
import os

from app.database import get_db
from app.models.user import User
from app.models.profile import Profile
from app.models.job_offer import JobOffer
from app.schemas.document import (
    DocumentGenerateRequest,
    DocumentUpdateRequest,
    DocumentResponse,
    DocumentStatsResponse
)
from app.services.ai_service import ai_service
from app.services.document_service import DocumentService
from app.api.auth import get_current_user


router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


@router.post("/generate", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def generate_document(
    request: DocumentGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Génère un CV ou une lettre de motivation avec l'IA
    
    Limite: 10 générations par jour par utilisateur
    """
    # 1. Vérifier la limite quotidienne
    can_generate, remaining = await DocumentService.check_daily_limit(db, current_user.id)
    if not can_generate:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Limite quotidienne atteinte ({DocumentService.DAILY_GENERATION_LIMIT} générations/jour). Réessayez demain."
        )
    
    # 2. Charger le profil utilisateur
    profile_result = await db.execute(
        select(Profile)
        .options(
            selectinload(Profile.experiences),
            selectinload(Profile.skills),
            selectinload(Profile.educations)
        )
        .where(Profile.user_id == current_user.id)
    )
    profile = profile_result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil non trouvé. Créez d'abord votre profil."
        )
    
    # 3. Charger l'offre d'emploi
    # 3. Charger l'offre d'emploi (sans filtrer par user_id)
    job_result = await db.execute(
        select(JobOffer).where(JobOffer.id == request.job_offer_id)
    )
    job_offer = job_result.scalar_one_or_none()
    
    if not job_offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offre non trouvée. Veuillez sauvegarder l'offre avant de générer des documents."
        )
    
    # 4. Générer le contenu avec l'IA
    try:
        if request.document_type == "resume":
            content = await ai_service.generate_resume(
                profile=profile,
                job_offer=job_offer,
                tone=request.tone,
                language=request.language
            )
        elif request.document_type == "cover_letter":
            content = await ai_service.generate_cover_letter(
                profile=profile,
                job_offer=job_offer,
                tone=request.tone,
                length=request.length,
                language=request.language
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Type de document invalide"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la génération: {str(e)}"
        )
    
    # 5. Sauvegarder le document en base
    generation_params = {
        "tone": request.tone,
        "language": request.language,
        "document_type": request.document_type
    }
    if request.document_type == "cover_letter":
        generation_params["length"] = request.length
    
    document = await DocumentService.create_document(
        db=db,
        user_id=current_user.id,
        profile_id=profile.id,
        job_offer_id=job_offer.id,
        document_type=request.document_type,
        content=content,
        generation_params=generation_params,
        language=request.language
    )
    
    return document


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    document_type: str = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Liste les documents générés par l'utilisateur
    
    Query params:
    - document_type: Filtre par type ("resume" ou "cover_letter")
    - limit: Nombre maximum de résultats
    """
    documents = await DocumentService.list_user_documents(
        db=db,
        user_id=current_user.id,
        document_type=document_type,
        limit=limit
    )
    return documents


@router.get("/stats", response_model=DocumentStatsResponse)
async def get_document_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtient les statistiques de génération de l'utilisateur
    
    Retourne:
    - Nombre total de documents
    - Décompte par type
    - Limite quotidienne et nombre restant
    """
    stats = await DocumentService.get_user_stats(db, current_user.id)
    return stats


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Récupère un document par son ID
    """
    document = await DocumentService.get_document(db, document_id, current_user.id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document non trouvé"
        )
    
    return document


@router.patch("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: UUID,
    request: DocumentUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Met à jour le contenu d'un document (après édition manuelle)
    """
    document = await DocumentService.update_document_content(
        db=db,
        document_id=document_id,
        user_id=current_user.id,
        content=request.content
    )
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document non trouvé"
        )
    
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Supprime un document
    """
    success = await DocumentService.delete_document(db, document_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document non trouvé"
        )
    
    return None


@router.get("/{document_id}/download")
async def download_document_pdf(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Télécharge le PDF d'un document généré
    """
    from fastapi.responses import Response
    from app.services.pdf_generator import PDFGenerator
    
    # Récupérer le document
    document = await DocumentService.get_document(db, document_id, current_user.id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document non trouvé"
        )
    
    # Récupérer les infos pour le titre
    job_result = await db.execute(
        select(JobOffer).where(JobOffer.id == document.job_offer_id)
    )
    job_offer = job_result.scalar_one_or_none()
    
    profile_result = await db.execute(
        select(Profile).where(Profile.id == document.profile_id)
    )
    profile = profile_result.scalar_one_or_none()
    
    # Préparer les informations pour le PDF
    candidate_name = current_user.full_name if current_user.full_name else "Candidat"
    contact_info = f"{current_user.email}"
    if profile and profile.phone:
        contact_info += f" | {profile.phone}"
    if profile and profile.location:
        contact_info += f" | {profile.location}"
    
    company_name = job_offer.company_name if job_offer else "Entreprise"
    company_address = job_offer.location if job_offer else ""
    
    from datetime import datetime
    today = datetime.now().strftime("%d/%m/%Y")
    
    # Générer le PDF selon le type
    if document.document_type == "cover_letter":
        pdf_bytes = PDFGenerator.generate_cover_letter_pdf(
            candidate_name=candidate_name,
            contact_info=contact_info,
            company_name=company_name,
            company_address=company_address,
            content_markdown=document.content,
            date=today
        )
    else:  # resume
        pdf_bytes = PDFGenerator.generate_cv_pdf(
            candidate_name=candidate_name,
            contact_info=contact_info,
            content_markdown=document.content,
            date=today
        )
    
    # Retourner le PDF
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=\"{document.filename}\""
        }
    )
