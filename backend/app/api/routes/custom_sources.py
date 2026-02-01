"""
Routes API pour la gestion des sources personnalisées (career pages, job boards custom).
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.custom_source_service import CustomSourceService
from app.schemas.custom_source import (
    AddCustomSourceRequest,
    CustomSourceResponse,
    CustomSourceListResponse,
    TestSourceResponse,
    UpdateCustomSourceRequest,
    DeleteSourceResponse,
    SourceAnalysis
)

router = APIRouter(prefix="/sources/custom", tags=["Custom Sources"])


@router.post("", response_model=CustomSourceResponse, status_code=status.HTTP_201_CREATED)
async def add_custom_source(
    request: AddCustomSourceRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Ajoute une source personnalisée après analyse automatique.
    
    L'URL est automatiquement analysée pour :
    - Déterminer le type (career page, job board, etc.)
    - Vérifier la présence d'offres d'emploi
    - Détecter d'éventuels systèmes anti-bot
    - Fournir une recommandation de scrapabilité
    
    Args:
        request: Détails de la source à ajouter
        current_user: Utilisateur authentifié
        db: Session de base de données
        
    Returns:
        CustomSourceResponse: Source créée avec son analyse
        
    Raises:
        HTTPException 400: URL déjà ajoutée ou non scrapable
        HTTPException 500: Erreur lors de l'ajout
    """
    service = CustomSourceService(db)
    
    try:
        # Ajouter la source (analyse automatique incluse)
        source = await service.add_custom_source(
            user_id=current_user.id,
            source_name=request.source_name,
            source_url=str(request.source_url),
            scraping_frequency=request.scraping_frequency
        )
        
        # Construire la réponse avec l'analyse
        analysis = None
        if source.get('analysis'):
            analysis = SourceAnalysis(**source['analysis'])
        
        return CustomSourceResponse(
            id=source['id'],
            user_id=str(source['user_id']),
            source_name=source['source_name'],
            source_url=source['source_url'],
            source_type=source['source_type'],
            is_active=source['is_active'],
            scraping_frequency=source['scraping_frequency'],
            created_at=source['created_at'],
            last_scraped_at=source.get('last_scraped_at'),
            total_offers_found=source.get('total_offers_found', 0),
            analysis=analysis
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'ajout de la source: {str(e)}"
        )


@router.get("", response_model=CustomSourceListResponse)
async def get_user_custom_sources(
    page: int = 1,
    per_page: int = 20,
    active_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Liste toutes les sources personnalisées de l'utilisateur.
    
    Args:
        page: Numéro de page (défaut: 1)
        per_page: Résultats par page (défaut: 20, max: 100)
        active_only: Filtrer uniquement les sources actives
        current_user: Utilisateur authentifié
        db: Session de base de données
        
    Returns:
        CustomSourceListResponse: Liste paginée des sources
    """
    if per_page > 100:
        per_page = 100
    
    service = CustomSourceService(db)
    
    try:
        result = await service.get_user_sources(
            user_id=current_user.id,
            page=page,
            per_page=per_page,
            active_only=active_only
        )
        
        sources = [
            CustomSourceResponse(
                id=s['id'],
                user_id=str(s['user_id']),
                source_name=s['source_name'],
                source_url=s['source_url'],
                source_type=s['source_type'],
                is_active=s['is_active'],
                scraping_frequency=s['scraping_frequency'],
                created_at=s['created_at'],
                last_scraped_at=s.get('last_scraped_at'),
                total_offers_found=s.get('total_offers_found', 0)
            )
            for s in result['sources']
        ]
        
        return CustomSourceListResponse(
            sources=sources,
            total=result['total'],
            page=page,
            per_page=per_page
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des sources: {str(e)}"
        )


@router.post("/test", response_model=TestSourceResponse)
async def test_url_scrapability(
    url: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Teste une URL pour vérifier sa scrapabilité SANS l'ajouter.
    
    Utile pour prévisualiser si une URL est valide avant de l'enregistrer.
    
    Args:
        url: URL à tester
        current_user: Utilisateur authentifié
        db: Session de base de données
        
    Returns:
        TestSourceResponse: Résultat de l'analyse avec recommandation
    """
    service = CustomSourceService(db)
    
    try:
        analysis = await service.analyze_url(url)
        
        message = "✅ URL scrapable" if analysis['is_scrapable'] else "⚠️ Scraping difficile ou impossible"
        
        return TestSourceResponse(
            success=True,
            analysis=SourceAnalysis(**analysis),
            message=message
        )
        
    except Exception as e:
        return TestSourceResponse(
            success=False,
            analysis=SourceAnalysis(
                is_accessible=False,
                content_type="unknown",
                has_jobs=False,
                job_keywords_found=[],
                estimated_job_count=None,
                has_anti_bot=False,
                anti_bot_indicators=[],
                recommendation="❌ Erreur lors de l'analyse",
                is_scrapable=False
            ),
            message=f"Erreur: {str(e)}"
        )


@router.patch("/{source_id}", response_model=CustomSourceResponse)
async def update_custom_source(
    source_id: int,
    request: UpdateCustomSourceRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Met à jour une source personnalisée (nom, statut actif, fréquence).
    
    Args:
        source_id: ID de la source à modifier
        request: Champs à mettre à jour
        current_user: Utilisateur authentifié
        db: Session de base de données
        
    Returns:
        CustomSourceResponse: Source mise à jour
        
    Raises:
        HTTPException 404: Source non trouvée
        HTTPException 403: Source appartient à un autre utilisateur
    """
    service = CustomSourceService(db)
    
    try:
        # Récupérer la source pour vérifier l'ownership
        result = await service.get_user_sources(
            user_id=current_user.id,
            page=1,
            per_page=1
        )
        
        source_exists = any(s['id'] == source_id for s in result['sources'])
        if not source_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Source non trouvée"
            )
        
        # Mettre à jour
        from app.models.custom_source import CustomSource
        from sqlalchemy import select, update
        
        update_data = {}
        if request.source_name is not None:
            update_data['source_name'] = request.source_name
        if request.is_active is not None:
            update_data['is_active'] = request.is_active
        if request.scraping_frequency is not None:
            update_data['scraping_frequency'] = request.scraping_frequency
        
        if update_data:
            stmt = (
                update(CustomSource)
                .where(CustomSource.id == source_id)
                .values(**update_data)
            )
            await db.execute(stmt)
            await db.commit()
        
        # Récupérer la source mise à jour
        stmt = select(CustomSource).where(CustomSource.id == source_id)
        result = await db.execute(stmt)
        updated_source = result.scalar_one()
        
        return CustomSourceResponse(
            id=updated_source.id,
            user_id=str(updated_source.user_id),
            source_name=updated_source.source_name,
            source_url=updated_source.source_url,
            source_type=updated_source.source_type,
            is_active=updated_source.is_active,
            scraping_frequency=updated_source.scraping_frequency,
            created_at=updated_source.created_at,
            last_scraped_at=updated_source.last_scraped_at,
            total_offers_found=updated_source.total_offers_found or 0
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour: {str(e)}"
        )


@router.delete("/{source_id}", response_model=DeleteSourceResponse)
async def delete_custom_source(
    source_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Supprime une source personnalisée.
    
    Args:
        source_id: ID de la source à supprimer
        current_user: Utilisateur authentifié
        db: Session de base de données
        
    Returns:
        DeleteSourceResponse: Confirmation de suppression
        
    Raises:
        HTTPException 404: Source non trouvée
    """
    service = CustomSourceService(db)
    
    try:
        success = await service.delete_source(
            user_id=current_user.id,
            source_id=source_id
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Source non trouvée ou déjà supprimée"
            )
        
        return DeleteSourceResponse(
            success=True,
            message=f"Source {source_id} supprimée avec succès"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression: {str(e)}"
        )
