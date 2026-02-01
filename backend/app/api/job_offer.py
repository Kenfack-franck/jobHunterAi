"""
Routes API pour les offres d'emploi
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.schemas.job_offer import (
    JobOfferCreate,
    JobOfferUpdate,
    JobOfferResponse,
    JobOfferSearchParams
)
from app.services.job_offer_service import JobOfferService
from app.core.dependencies import get_current_user


router = APIRouter(prefix="/api/v1/jobs", tags=["Job Offers"])


@router.get("", response_model=List[JobOfferResponse])
async def get_user_job_offers(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Récupérer toutes les offres d'emploi de l'utilisateur connecté"""
    offers = await JobOfferService.get_user_job_offers(
        db, 
        user_id=current_user.id,
        limit=limit,
        offset=offset
    )
    return offers


@router.post("", response_model=JobOfferResponse, status_code=status.HTTP_201_CREATED)
async def create_job_offer(
    data: JobOfferCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Créer une nouvelle offre d'emploi"""
    offer = await JobOfferService.create_job_offer(
        db,
        user_id=current_user.id,
        data=data
    )
    return offer


@router.get("/search", response_model=List[JobOfferResponse])
async def search_job_offers(
    keyword: Optional[str] = Query(None, description="Mot-clé pour rechercher dans titre, description"),
    location: Optional[str] = Query(None, description="Localisation"),
    job_type: Optional[str] = Query(None, description="Type de poste (CDI, CDD, Stage, etc.)"),
    company_name: Optional[str] = Query(None, description="Nom de l'entreprise"),
    enable_scraping: bool = Query(True, description="Activer le scraping Internet"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Recherche HYBRIDE: DB locale + Scraping Internet
    
    Cette endpoint fait deux choses:
    1. Cherche dans la base de données locale de l'utilisateur
    2. Si enable_scraping=True ET keyword fourni, lance le scraping sur Internet
    3. Combine les résultats et déduplique
    
    Paramètres:
    - keyword: Mots-clés de recherche (ex: "data-science", "Python Developer")
    - location: Localisation (ex: "Paris", "Remote")
    - job_type: Type de contrat (Stage, CDI, CDD, Alternance, etc.)
    - company_name: Nom d'entreprise spécifique
    - enable_scraping: True pour activer le scraping, False pour DB uniquement
    - limit: Nombre max de résultats (défaut: 50)
    
    Returns:
        Liste d'offres d'emploi (DB + Internet, dédupliquées)
    """
    from app.services.search_service import search_service
    
    print(f"\n[API] Recherche hybride lancée par {current_user.email}")
    print(f"[API] Params: keyword={keyword}, location={location}, job_type={job_type}, scraping={enable_scraping}")
    
    try:
        # Utiliser la recherche hybride
        result = await search_service.search_hybrid(
            db=db,
            user_id=str(current_user.id),
            keywords=keyword,
            location=location,
            job_type=job_type,
            company=company_name,
            enable_scraping=enable_scraping,
            limit=limit
        )
        
        print(f"[API] Résultats: {result['total_count']} offres ({result['db_count']} DB + {result['scraped_count']} scraping)")
        
        # Normaliser les offres au format JobOfferResponse
        normalized_offers = []
        for offer in result["offers"]:
            try:
                # Générer un UUID temporaire pour les offres scrapées (non sauvegardées en DB)
                offer_id = offer.get("id")
                if not offer_id or offer_id == "":
                    import uuid
                    offer_id = str(uuid.uuid4())
                
                # Normaliser les champs
                normalized = JobOfferResponse(
                    id=offer_id,
                    user_id=current_user.id,  # Associé à l'utilisateur actuel
                    job_title=offer.get("title", "Poste non spécifié"),
                    company_name=offer.get("company"),
                    location=offer.get("location"),
                    job_type=offer.get("job_type"),
                    description=offer.get("description"),
                    source_url=offer.get("url"),
                    source_platform=offer.get("source_platform", "unknown"),
                    created_at=datetime.fromisoformat(offer["created_at"]) if offer.get("created_at") and isinstance(offer["created_at"], str) else datetime.utcnow(),
                    analyzed_at=None
                )
                normalized_offers.append(normalized)
            except Exception as e:
                print(f"[API] Erreur normalisation offre: {e}")
                continue
        
        print(f"[API] {len(normalized_offers)} offres normalisées retournées")
        return normalized_offers
        
    except Exception as e:
        print(f"[API] Erreur recherche hybride: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la recherche: {str(e)}"
        )


@router.get("/{job_offer_id}", response_model=JobOfferResponse)
async def get_job_offer(
    job_offer_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Récupérer une offre d'emploi par ID"""
    offer = await JobOfferService.get_job_offer_by_id(
        db,
        job_offer_id=job_offer_id,
        user_id=current_user.id
    )
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offre d'emploi non trouvée"
        )
    return offer


@router.put("/{job_offer_id}", response_model=JobOfferResponse)
async def update_job_offer(
    job_offer_id: UUID,
    data: JobOfferUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mettre à jour une offre d'emploi"""
    offer = await JobOfferService.update_job_offer(
        db,
        job_offer_id=job_offer_id,
        user_id=current_user.id,
        data=data
    )
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offre d'emploi non trouvée"
        )
    return offer


@router.delete("/{job_offer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_offer(
    job_offer_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Supprimer une offre d'emploi"""
    success = await JobOfferService.delete_job_offer(
        db,
        job_offer_id=job_offer_id,
        user_id=current_user.id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offre d'emploi non trouvée"
        )
    return None


@router.get("/stats/count", response_model=dict)
async def get_job_offers_count(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Obtenir le nombre total d'offres de l'utilisateur"""
    count = await JobOfferService.count_user_job_offers(db, current_user.id)
    return {"count": count}


@router.get("/{job_id}/compatibility/{profile_id}", response_model=dict)
async def get_compatibility_score(
    job_id: str,
    profile_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Calcule le score de compatibilité entre un profil et une offre.
    
    Returns:
        Score et détails de l'analyse
    """
    from app.services.analysis_service import AnalysisService
    
    try:
        analysis = await AnalysisService.calculate_compatibility_score(
            profile_id, job_id, db
        )
        return {
            "success": True,
            "analysis": analysis
        }
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(e))


# ============================================
# ASYNC SEARCH ENDPOINTS
# ============================================

@router.post("/search/async", response_model=dict)
async def search_jobs_async_endpoint(
    keywords: Optional[str] = Query(None, description="Mots-clés de recherche"),
    location: Optional[str] = Query(None, description="Localisation"),
    job_type: Optional[str] = Query(None, description="Type de contrat"),
    work_mode: Optional[str] = Query(None, description="Mode de travail"),
    company: Optional[str] = Query(None, description="Entreprise spécifique"),
    current_user: User = Depends(get_current_user),
):
    """
    Lance une recherche d'offres asynchrone avec scraping.
    
    Retourne immédiatement un task_id pour suivre la progression.
    Utilisez GET /search/status/{task_id} pour obtenir les résultats.
    """
    from app.tasks.scraping_tasks import search_jobs_async
    
    # Lancer la task Celery
    task = search_jobs_async.delay(
        user_id=str(current_user.id),
        keywords=keywords,
        location=location,
        job_type=job_type,
        work_mode=work_mode,
        company=company
    )
    
    return {
        "task_id": task.id,
        "status": "pending",
        "message": "Recherche lancée. Utilisez /search/status/{task_id} pour suivre la progression.",
        "search_params": {
            "keywords": keywords,
            "location": location,
            "job_type": job_type,
            "work_mode": work_mode,
            "company": company
        }
    }


@router.get("/search/status/{task_id}", response_model=dict)
async def get_search_status(
    task_id: str,
    current_user: User = Depends(get_current_user),
):
    """
    Récupère le statut d'une recherche asynchrone.
    
    États possibles:
    - pending: En attente dans la queue
    - processing: Scraping en cours
    - completed: Terminé avec succès
    - failed: Échec
    
    Returns:
        Status et résultats si disponibles
    """
    from celery.result import AsyncResult
    
    task = AsyncResult(task_id)
    
    # Task en attente
    if task.state == 'PENDING':
        return {
            "task_id": task_id,
            "status": "pending",
            "message": "Recherche en file d'attente...",
            "progress": 0
        }
    
    # Task en cours
    elif task.state == 'STARTED':
        info = task.info or {}
        return {
            "task_id": task_id,
            "status": info.get('status', 'processing'),
            "message": info.get('message', 'Scraping en cours...'),
            "progress": info.get('current', 0),
            "total": info.get('total', 100),
            "count": info.get('count', 0)
        }
    
    # Task réussie
    elif task.state == 'SUCCESS':
        result = task.result or {}
        return {
            "task_id": task_id,
            "status": "completed",
            "message": f"{result.get('count', 0)} offres trouvées",
            "progress": 100,
            "offers": result.get('offers', []),
            "count": result.get('count', 0),
            "scraped_count": result.get('scraped_count', 0),
            "platforms_scraped": result.get('platforms_scraped', []),
            "search_params": result.get('search_params', {}),
            "completed_at": result.get('completed_at')
        }
    
    # Task échouée
    elif task.state == 'FAILURE':
        info = task.info or {}
        error_message = str(info) if not isinstance(info, dict) else info.get('error', 'Erreur inconnue')
        
        return {
            "task_id": task_id,
            "status": "failed",
            "message": f"Erreur: {error_message}",
            "error": error_message,
            "progress": 0
        }
    
    # État inconnu
    else:
        return {
            "task_id": task_id,
            "status": "unknown",
            "message": f"État inconnu: {task.state}",
            "state": task.state
        }
