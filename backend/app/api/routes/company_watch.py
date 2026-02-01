"""
Routes API pour la veille entreprise
"""
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.company_watch_service import CompanyWatchService
from app.schemas.company_watch import (
    AddWatchRequest,
    WatchResponse,
    WatchListResponse,
    CompanyOffersResponse
)


router = APIRouter(prefix="/watch", tags=["Company Watch"])


@router.post("/company", response_model=WatchResponse)
async def add_company_watch(
    request: AddWatchRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Ajouter une entreprise à surveiller
    
    **Paramètres**:
    - company_name: Nom de l'entreprise (obligatoire)
    - profile_id: ID du profil pour scoring (optionnel)
    - alert_threshold: Score minimum pour alerte (défaut: 70)
    - linkedin_url: URL LinkedIn entreprise (optionnel)
    - careers_url: URL page carrières (optionnel)
    
    **Mutualisation**: Si l'entreprise est déjà surveillée par d'autres users,
    elle sera partagée (1 scraping pour N users).
    """
    try:
        service = CompanyWatchService(db)
        result = await service.add_company_watch(
            user_id=current_user.id,
            company_name=request.company_name,
            profile_id=request.profile_id,
            alert_threshold=request.alert_threshold,
            linkedin_url=request.linkedin_url,
            careers_url=request.careers_url
        )
        return WatchResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur ajout veille: {str(e)}")


@router.get("/companies", response_model=WatchListResponse)
async def get_my_watches(
    page: int = Query(1, ge=1, description="Numéro de page"),
    per_page: int = Query(20, ge=1, le=100, description="Résultats par page"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Récupérer toutes mes veilles entreprises
    
    **Pagination**: Utiliser `page` et `per_page`
    
    **Réponse**: Liste des entreprises surveillées avec:
    - Nom entreprise
    - Nombre total de watchers (mutualisation)
    - Nombre d'offres trouvées
    - Date dernier scraping
    """
    try:
        service = CompanyWatchService(db)
        result = await service.get_user_watches(
            user_id=current_user.id,
            page=page,
            per_page=per_page
        )
        return WatchListResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur récupération veilles: {str(e)}")


@router.delete("/{watch_id}")
async def remove_watch(
    watch_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Supprimer une veille entreprise
    
    **Paramètres**:
    - watch_id: ID de la veille à supprimer
    
    **Mutualisation**: Si c'est le dernier user à surveiller l'entreprise,
    celle-ci sera supprimée de la table `watched_companies`.
    """
    try:
        service = CompanyWatchService(db)
        result = await service.remove_company_watch(
            user_id=current_user.id,
            watch_id=watch_id
        )
        
        if not result["success"]:
            raise HTTPException(status_code=404, detail=result["message"])
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur suppression veille: {str(e)}")


@router.get("/{company_id}/offers", response_model=CompanyOffersResponse)
async def get_company_offers(
    company_id: UUID,
    profile_id: Optional[UUID] = Query(None, description="ID profil pour scoring"),
    limit: int = Query(50, ge=1, le=200, description="Nombre max d'offres"),
    min_score: int = Query(0, ge=0, le=100, description="Score minimum (si profile_id fourni)"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Récupérer les offres d'une entreprise surveillée
    
    **Paramètres**:
    - company_id: ID de l'entreprise
    - profile_id: ID profil pour calculer scores (optionnel)
    - limit: Nombre max d'offres (défaut: 50, max: 200)
    - min_score: Score minimum si profil fourni (défaut: 0)
    
    **Réponse**: Liste des offres des 30 derniers jours avec:
    - Détails offre (titre, localisation, type...)
    - Score de compatibilité (si profile_id fourni)
    - Date de scraping
    
    **Tri**: Par score décroissant (si profile_id fourni), sinon par date
    """
    try:
        service = CompanyWatchService(db)
        result = await service.get_company_offers(
            company_id=company_id,
            user_id=current_user.id,
            profile_id=profile_id,
            limit=limit,
            min_score=min_score
        )
        
        if not result["success"]:
            raise HTTPException(status_code=404, detail=result["message"])
        
        return CompanyOffersResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur récupération offres: {str(e)}")


@router.post("/scrape-all")
async def scrape_all_watched_companies(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    **[ADMIN ONLY]** Lancer le scraping de toutes les entreprises surveillées
    
    ⚠️ Cette route devrait être protégée par un middleware admin.
    
    **Fonctionnement**:
    - Scrape toutes les entreprises avec watchers > 0
    - Mutualisation: 1 scraping pour N users
    - Met à jour last_scraped_at et total_offers_found
    
    **Note**: En production, cette fonction sera appelée par Celery Beat (tâche périodique).
    """
    try:
        # TODO: Ajouter vérification is_admin
        # if not current_user.is_admin:
        #     raise HTTPException(status_code=403, detail="Accès réservé aux admins")
        
        service = CompanyWatchService(db)
        result = await service.scrape_watched_companies()
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur scraping: {str(e)}")
