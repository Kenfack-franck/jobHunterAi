"""
Service de gestion du cache des résultats de recherche
"""
import hashlib
import json
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete

from app.models.search_cache import SearchResultsCache


class SearchCacheService:
    """Service pour gérer le cache des recherches d'offres"""
    
    def _serialize_for_json(self, obj: Any) -> Any:
        """
        Convertit récursivement les objets datetime en chaînes ISO
        pour permettre la sérialisation JSON
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {k: self._serialize_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_for_json(item) for item in obj]
        else:
            return obj
    
    def generate_cache_key(
        self,
        user_id: str,
        keywords: str,
        location: Optional[str] = None,
        job_type: Optional[str] = None,
        work_mode: Optional[str] = None,
        company: Optional[str] = None,
        sources: Optional[List[str]] = None
    ) -> str:
        """
        Génère une clé de cache unique basée sur les paramètres de recherche
        
        Args:
            user_id: ID utilisateur
            keywords: Mots-clés recherche
            location: Localisation
            job_type: Type de contrat
            work_mode: Mode de travail
            company: Entreprise
            sources: Liste des sources utilisées
        
        Returns:
            Hash MD5 (32 caractères)
        """
        # Normaliser les paramètres
        keywords_norm = keywords.lower().strip() if keywords else ""
        location_norm = location.lower().strip() if location else ""
        job_type_norm = job_type.lower().strip() if job_type else ""
        work_mode_norm = work_mode.lower().strip() if work_mode else ""
        company_norm = company.lower().strip() if company else ""
        sources_norm = "|".join(sorted(sources)) if sources else ""
        
        # Créer la chaîne à hasher
        cache_string = f"{user_id}|{keywords_norm}|{location_norm}|{job_type_norm}|{work_mode_norm}|{company_norm}|{sources_norm}"
        
        # Générer MD5
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    async def get_cached_results(
        self,
        db: AsyncSession,
        cache_key: str
    ) -> Optional[Dict]:
        """
        Récupère les résultats depuis le cache s'ils sont valides
        
        Args:
            db: Session DB
            cache_key: Clé de cache
        
        Returns:
            Dict avec résultats ou None si cache invalide/expiré
        """
        # Chercher dans le cache
        stmt = select(SearchResultsCache).where(
            and_(
                SearchResultsCache.cache_key == cache_key,
                SearchResultsCache.is_valid == True,
                SearchResultsCache.expires_at > datetime.utcnow()
            )
        )
        result = await db.execute(stmt)
        cache_entry = result.scalar_one_or_none()
        
        if not cache_entry:
            return None
        
        # Incrémenter le compteur de hits
        cache_entry.hit_count += 1
        await db.commit()
        
        print(f"[SearchCache] ✅ CACHE HIT - Key: {cache_key[:8]}... (hits: {cache_entry.hit_count})")
        
        return {
            "success": True,
            "offers": cache_entry.results,
            "count": cache_entry.results_count,
            "scraped_count": cache_entry.scraped_count,
            "deduplicated_count": cache_entry.deduplicated_count,
            "execution_time_seconds": cache_entry.execution_time_seconds,
            "sources_used": cache_entry.sources_used,
            "cached": True,
            "cached_at": cache_entry.created_at.isoformat(),
            "cache_hits": cache_entry.hit_count,
            "search_params": {
                "keywords": cache_entry.keywords,
                "location": cache_entry.location,
                "job_type": cache_entry.job_type,
                "work_mode": cache_entry.work_mode,
                "company": cache_entry.company
            }
        }
    
    async def save_to_cache(
        self,
        db: AsyncSession,
        cache_key: str,
        user_id: str,
        keywords: str,
        location: Optional[str],
        job_type: Optional[str],
        work_mode: Optional[str],
        company: Optional[str],
        sources_used: List[str],
        results: List[Dict],
        scraped_count: int,
        deduplicated_count: int,
        execution_time_seconds: int,
        ttl_hours: int = 24
    ):
        """
        Sauvegarde les résultats dans le cache
        
        Args:
            db: Session DB
            cache_key: Clé de cache
            user_id: ID utilisateur
            keywords: Mots-clés
            location: Localisation
            job_type: Type de contrat
            work_mode: Mode de travail
            company: Entreprise
            sources_used: Sources utilisées
            results: Liste des offres
            scraped_count: Nombre d'offres scrapées
            deduplicated_count: Nombre après déduplication
            execution_time_seconds: Temps d'exécution
            ttl_hours: Durée de vie du cache en heures
        """
        expires_at = datetime.utcnow() + timedelta(hours=ttl_hours)
        
        # Nettoyer les résultats pour JSON (convertir datetime en ISO)
        cleaned_results = self._serialize_for_json(results)
        
        # Vérifier si entrée existe déjà
        stmt = select(SearchResultsCache).where(SearchResultsCache.cache_key == cache_key)
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()
        
        if existing:
            # Mettre à jour
            existing.results = cleaned_results
            existing.results_count = len(results)
            existing.scraped_count = scraped_count
            existing.deduplicated_count = deduplicated_count
            existing.execution_time_seconds = execution_time_seconds
            existing.sources_used = sources_used
            existing.expires_at = expires_at
            existing.is_valid = True
            existing.hit_count = 0  # Reset hits
            print(f"[SearchCache] 🔄 CACHE UPDATED - Key: {cache_key[:8]}...")
        else:
            # Créer nouvelle entrée
            cache_entry = SearchResultsCache(
                user_id=user_id,
                cache_key=cache_key,
                keywords=keywords,
                location=location,
                job_type=job_type,
                work_mode=work_mode,
                company=company,
                sources_used=sources_used,
                results=cleaned_results,
                results_count=len(results),
                scraped_count=scraped_count,
                deduplicated_count=deduplicated_count,
                execution_time_seconds=execution_time_seconds,
                expires_at=expires_at,
                hit_count=0,
                is_valid=True
            )
            db.add(cache_entry)
            print(f"[SearchCache] 💾 CACHE SAVED - Key: {cache_key[:8]}... (TTL: {ttl_hours}h)")
        
        await db.commit()
    
    async def invalidate_cache(
        self,
        db: AsyncSession,
        user_id: Optional[str] = None,
        cache_key: Optional[str] = None
    ):
        """
        Invalide le cache (par user ou par clé spécifique)
        
        Args:
            db: Session DB
            user_id: ID utilisateur (invalide tout son cache)
            cache_key: Clé spécifique (invalide juste cette recherche)
        """
        if cache_key:
            stmt = delete(SearchResultsCache).where(SearchResultsCache.cache_key == cache_key)
            await db.execute(stmt)
            print(f"[SearchCache] 🗑️ Cache invalidé - Key: {cache_key[:8]}...")
        elif user_id:
            stmt = delete(SearchResultsCache).where(SearchResultsCache.user_id == user_id)
            await db.execute(stmt)
            print(f"[SearchCache] 🗑️ Cache invalidé - User: {user_id}")
        
        await db.commit()
    
    async def cleanup_expired(self, db: AsyncSession):
        """
        Nettoie les entrées expirées du cache
        """
        stmt = delete(SearchResultsCache).where(
            SearchResultsCache.expires_at < datetime.utcnow()
        )
        result = await db.execute(stmt)
        await db.commit()
        
        deleted_count = result.rowcount
        if deleted_count > 0:
            print(f"[SearchCache] 🧹 {deleted_count} entrées expirées supprimées")


# Instance globale
search_cache_service = SearchCacheService()
