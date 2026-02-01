"""
Tâches Celery pour le scraping périodique

Ces tâches sont exécutées automatiquement par Celery Beat :
- scrape_all_watched_companies : Toutes les 4h
- scrape_all_custom_sources : Toutes les 4h (décalé)
- cleanup_old_job_offers : Tous les jours à 3h
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from uuid import UUID
from celery.utils.log import get_task_logger
from sqlalchemy import select, delete, and_

from app.celery_config import celery_app
from app.database import AsyncSessionLocal
from app.models.watched_company import WatchedCompany
from app.models.custom_source import CustomSource
from app.models.job_offer import JobOffer
from app.services.company_watch_service import CompanyWatchService

logger = get_task_logger(__name__)


@celery_app.task(
    bind=True,
    name='app.tasks.scraping_tasks.scrape_all_watched_companies',
    max_retries=3,
    default_retry_delay=300  # 5 minutes
)
def scrape_all_watched_companies(self) -> Dict[str, Any]:
    """
    Scrappe toutes les entreprises surveillées.
    
    Processus :
    1. Récupère toutes les entreprises avec last_scraped_at > 4h
    2. Pour chaque entreprise, lance le scraping
    3. Sauvegarde les nouvelles offres en DB
    4. Met à jour last_scraped_at
    
    Returns:
        Dict avec statistiques (companies_scraped, offers_found, errors)
    """
    async def _run():
        logger.info("🚀 Démarrage scraping entreprises surveillées...")
        
        stats = {
            "companies_scraped": 0,
            "offers_found": 0,
            "errors": [],
            "started_at": datetime.now().isoformat()
        }
        
        try:
            async with AsyncSessionLocal() as db:
                # Récupérer entreprises à scraper (pas scrapées depuis 4h ou jamais)
                four_hours_ago = datetime.now() - timedelta(hours=4)
                
                query = select(WatchedCompany).where(
                    (WatchedCompany.last_scraped_at == None) |
                    (WatchedCompany.last_scraped_at < four_hours_ago)
                )
                result = await db.execute(query)
                companies = result.scalars().all()
                
                logger.info(f"📊 {len(companies)} entreprise(s) à scraper")
                
                if not companies:
                    logger.info("✅ Aucune entreprise à scraper")
                    return stats
                
                # Service de scraping
                service = CompanyWatchService(db)
                
                # Scraper chaque entreprise
                for company in companies:
                    try:
                        logger.info(f"🔍 Scraping {company.company_name}...")
                        
                        # Lancer le scraping (utilise la méthode existante)
                        offers_count = await service._scrape_and_save_company_offers(
                            company_name=company.company_name,
                            company_id=company.id,
                            user_id=None  # Scraping global, pas pour un user spécifique
                        )
                        
                        stats["companies_scraped"] += 1
                        stats["offers_found"] += offers_count
                        
                        logger.info(f"✅ {company.company_name}: {offers_count} offre(s) trouvée(s)")
                        
                    except Exception as e:
                        error_msg = f"Erreur scraping {company.company_name}: {str(e)}"
                        logger.error(error_msg)
                        stats["errors"].append(error_msg)
                
                await db.commit()
                
        except Exception as e:
            error_msg = f"Erreur globale scraping: {str(e)}"
            logger.error(error_msg)
            stats["errors"].append(error_msg)
            raise
        
        stats["completed_at"] = datetime.now().isoformat()
        logger.info(f"✅ Scraping terminé: {stats['companies_scraped']} entreprises, "
                    f"{stats['offers_found']} offres")
        
        return stats
    
    try:
        return asyncio.run(_run())
    except Exception as e:
        logger.error(f"❌ Erreur task: {str(e)}")
        raise self.retry(exc=e)


@celery_app.task(
    bind=True,
    name='app.tasks.scraping_tasks.scrape_all_custom_sources',
    max_retries=3,
    default_retry_delay=300
)
def scrape_all_custom_sources(self) -> Dict[str, Any]:
    """
    Scrappe toutes les sources custom actives.
    
    Returns:
        Dict avec statistiques
    """
    async def _run():
        logger.info("🚀 Démarrage scraping sources custom...")
        
        stats = {
            "sources_scraped": 0,
            "offers_found": 0,
            "errors": [],
            "started_at": datetime.now().isoformat()
        }
        
        try:
            async with AsyncSessionLocal() as db:
                # Récupérer sources actives à scraper
                four_hours_ago = datetime.now() - timedelta(hours=4)
                
                query = select(CustomSource).where(
                    and_(
                        CustomSource.is_active == True,
                        (
                            (CustomSource.last_scraped_at == None) |
                            (CustomSource.last_scraped_at < four_hours_ago)
                        )
                    )
                )
                result = await db.execute(query)
                sources = result.scalars().all()
                
                logger.info(f"📊 {len(sources)} source(s) custom à scraper")
                
                if not sources:
                    logger.info("✅ Aucune source custom à scraper")
                    return stats
                
                # TODO: Implémenter scraping sources custom
                # Pour l'instant, on log juste
                for source in sources:
                    logger.info(f"🔍 À scraper: {source.source_name} ({source.source_url})")
                    stats["sources_scraped"] += 1
                    
                    # Mettre à jour last_scraped_at
                    source.last_scraped_at = datetime.now()
                
                await db.commit()
                
        except Exception as e:
            error_msg = f"Erreur scraping sources custom: {str(e)}"
            logger.error(error_msg)
            stats["errors"].append(error_msg)
            raise
        
        stats["completed_at"] = datetime.now().isoformat()
        logger.info(f"✅ Scraping sources custom terminé: {stats['sources_scraped']} sources")
        
        return stats
    
    try:
        return asyncio.run(_run())
    except Exception as e:
        logger.error(f"❌ Erreur task: {str(e)}")
        raise self.retry(exc=e)


@celery_app.task(
    bind=True,
    name='app.tasks.scraping_tasks.cleanup_old_job_offers',
    max_retries=2
)
def cleanup_old_job_offers(self) -> Dict[str, Any]:
    """
    Nettoie les offres d'emploi de plus de 30 jours.
    
    Garde en DB uniquement les offres récentes pour éviter la surcharge.
    
    Returns:
        Dict avec nombre d'offres supprimées
    """
    async def _run():
        logger.info("🧹 Démarrage nettoyage anciennes offres...")
        
        stats = {
            "offers_deleted": 0,
            "started_at": datetime.now().isoformat()
        }
        
        try:
            async with AsyncSessionLocal() as db:
                # Supprimer offres > 30 jours
                thirty_days_ago = datetime.now() - timedelta(days=30)
                
                delete_stmt = delete(JobOffer).where(
                    JobOffer.scraped_at < thirty_days_ago
                )
                
                result = await db.execute(delete_stmt)
                await db.commit()
                
                stats["offers_deleted"] = result.rowcount
                
        except Exception as e:
            error_msg = f"Erreur nettoyage offres: {str(e)}"
            logger.error(error_msg)
            stats["error"] = error_msg
            raise
        
        stats["completed_at"] = datetime.now().isoformat()
        logger.info(f"✅ Nettoyage terminé: {stats['offers_deleted']} offre(s) supprimée(s)")
        
        return stats
    
    try:
        return asyncio.run(_run())
    except Exception as e:
        logger.error(f"❌ Erreur task: {str(e)}")
        raise self.retry(exc=e)


@celery_app.task(
    bind=True,
    name='app.tasks.scraping_tasks.scrape_single_company',
    max_retries=3
)
def scrape_single_company(self, company_name: str, user_id: str = None) -> Dict[str, Any]:
    """
    Scrappe une entreprise spécifique (utilisé pour scraping à la demande).
    
    Args:
        company_name: Nom de l'entreprise
        user_id: ID utilisateur (optionnel)
        
    Returns:
        Dict avec résultats
    """
    async def _run():
        async with AsyncSessionLocal() as db:
            service = CompanyWatchService(db)
            
            # Récupérer la company
            query = select(WatchedCompany).where(
                WatchedCompany.company_name == company_name
            )
            result = await db.execute(query)
            company = result.scalar_one_or_none()
            
            if not company:
                return {"error": "Entreprise non trouvée", "offers_found": 0}
            
            # Scraper
            offers_count = await service._scrape_and_save_company_offers(
                company_name=company_name,
                company_id=company.id,
                user_id=user_id
            )
            
            await db.commit()
            
            return {
                "company_name": company_name,
                "offers_found": offers_count,
                "scraped_at": datetime.now().isoformat()
            }
    
    try:
        return asyncio.run(_run())
    except Exception as e:
        logger.error(f"Erreur scraping {company_name}: {str(e)}")
        raise self.retry(exc=e)


@celery_app.task(
    bind=True,
    name='app.tasks.scraping_tasks.search_jobs_async',
    max_retries=2
)
def search_jobs_async(
    self, 
    user_id: str, 
    keywords: Optional[str] = None,
    location: Optional[str] = None,
    job_type: Optional[str] = None,
    work_mode: Optional[str] = None,
    company: Optional[str] = None
) -> Dict[str, Any]:
    """
    Recherche asynchrone d'offres d'emploi avec scraping.
    
    Cette task:
    1. Met à jour son état à 'STARTED'
    2. Lance le scraping des plateformes
    3. Sauvegarde les offres en DB
    4. Retourne les résultats
    
    Args:
        user_id: ID de l'utilisateur
        keywords: Mots-clés de recherche
        location: Localisation
        job_type: Type de contrat (CDI, CDD, etc.)
        work_mode: Mode de travail (remote, hybrid, onsite)
        company: Nom d'entreprise spécifique
        
    Returns:
        Dict avec offers, count, et metadata
    """
    async def _run():
        from app.services.search_service import search_service
        
        logger.info(f"🔍 Recherche async démarrée pour user {user_id}")
        logger.info(f"   Params: keywords={keywords}, location={location}, job_type={job_type}")
        
        # Mettre à jour l'état de la task
        self.update_state(
            state='STARTED',
            meta={
                'status': 'processing',
                'message': 'Scraping des plateformes en cours...',
                'current': 0,
                'total': 100
            }
        )
        
        try:
            async with AsyncSessionLocal() as db:
                # Lancer la recherche avec scraping
                result = await search_service.search_with_scraping(
                    db=db,
                    keywords=keywords,
                    location=location,
                    job_type=job_type,
                    work_mode=work_mode,
                    company=company,
                    limit_per_platform=20,
                    user_id=user_id
                )
                
                # Extraire les résultats
                offers = result.get("offers", [])
                count = result.get("count", 0)
                
                logger.info(f"✅ Recherche terminée: {count} offres trouvées")
                
                # Mettre à jour l'état avec progression
                self.update_state(
                    state='STARTED',
                    meta={
                        'status': 'processing',
                        'message': f'{count} offres trouvées, traitement en cours...',
                        'current': 50,
                        'total': 100,
                        'count': count
                    }
                )
                
                # Formatter les offres pour le frontend
                formatted_offers = []
                for offer in offers:
                    formatted_offers.append({
                        "id": str(offer.get("id", "")),
                        "title": offer.get("title", ""),
                        "company": offer.get("company", ""),
                        "location": offer.get("location", ""),
                        "description": offer.get("description", "")[:300],
                        "url": offer.get("url", ""),
                        "source_platform": offer.get("source_platform", ""),
                        "job_type": offer.get("job_type"),
                        "work_mode": offer.get("work_mode"),
                        "scraped_at": offer.get("scraped_at", datetime.now().isoformat())
                    })
                
                logger.info(f"📦 {len(formatted_offers)} offres formatées")
                
                return {
                    "success": True,
                    "offers": formatted_offers,
                    "count": count,
                    "scraped_count": result.get("scraped_count", 0),
                    "platforms_scraped": result.get("platforms_scraped", []),
                    "search_params": {
                        "keywords": keywords,
                        "location": location,
                        "job_type": job_type,
                        "work_mode": work_mode,
                        "company": company
                    },
                    "completed_at": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"❌ Erreur recherche: {str(e)}")
            # Mettre à jour l'état en échec
            self.update_state(
                state='FAILURE',
                meta={
                    'status': 'failed',
                    'error': str(e),
                    'message': f'Erreur lors de la recherche: {str(e)}'
                }
            )
            raise
    
    try:
        return asyncio.run(_run())
    except Exception as e:
        logger.error(f"❌ Erreur task search_jobs_async: {str(e)}")
        raise self.retry(exc=e)
