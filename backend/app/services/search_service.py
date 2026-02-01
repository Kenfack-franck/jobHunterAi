"""
SearchService - Service de recherche et agrégation d'offres d'emploi
Gère le scraping, la déduplication, la sauvegarde en DB et le feed personnalisé
"""
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc
from sqlalchemy.dialects.postgresql import insert
import hashlib
from difflib import SequenceMatcher

from app.models.job_offer import JobOffer
from app.models.profile import Profile
from app.models.user_feed_cache import UserFeedCache
from app.services.scraping_service import scraping_service
from app.services.ai_service import ai_service
class SearchService:
    """Service de recherche d'offres avec scraping et feed personnalisé"""
    
    def __init__(self):
        self.scraping_service = scraping_service
        self.ai_service = ai_service
        self.deduplication_threshold = 0.9  # 90% similarité pour considérer comme doublon
    
    async def search_with_scraping(
        self,
        db: AsyncSession,
        keywords: str,
        location: Optional[str] = None,
        job_type: Optional[str] = None,
        work_mode: Optional[str] = None,
        company: Optional[str] = None,
        limit_per_platform: int = 100,
        user_id: Optional[str] = None
    ) -> Dict:
        """
        Recherche d'offres avec scraping des plateformes activées
        
        Args:
            db: Session DB
            keywords: Mots-clés de recherche (ex: "Python Developer")
            location: Localisation (ex: "Paris", "Remote")
            job_type: Type de contrat (fulltime, contract, internship, etc.)
            work_mode: Mode de travail (remote, hybrid, onsite)
            company: Nom d'entreprise spécifique
            limit_per_platform: Limite d'offres par plateforme
            user_id: ID utilisateur (pour audit)
        
        Returns:
            Dict avec offres, statistiques et métadonnées
        """
        start_time = datetime.utcnow()
        
        # 1. Scraping depuis toutes les plateformes activées
        print(f"[SearchService] Début scraping: keywords={keywords}, location={location}")
        
        raw_results = await self.scraping_service.scrape_all_platforms(
            keywords=keywords,
            location=location or "",
            limit_per_platform=limit_per_platform
        )
        
        # Aplatir les résultats (dict[platform] -> list)
        all_offers = []
        for platform, offers in raw_results.items():
            all_offers.extend(offers)
        
        print(f"[SearchService] {len(all_offers)} offres brutes récupérées")
        
        # 2. Déduplication
        deduplicated_offers = await self.deduplicate_offers(all_offers)
        print(f"[SearchService] {len(deduplicated_offers)} offres après déduplication")
        
        # 3. Filtrage par critères (si spécifiés)
        filtered_offers = self._filter_offers(
            deduplicated_offers,
            job_type=job_type,
            work_mode=work_mode,
            company=company
        )
        print(f"[SearchService] {len(filtered_offers)} offres après filtrage")
        
        # 4. Sauvegarde en DB + génération embeddings
        saved_count = await self._save_offers_to_db(db, filtered_offers)
        print(f"[SearchService] {saved_count} offres sauvegardées en DB")
        
        # 5. Préparer la réponse
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        return {
            "success": True,
            "offers": filtered_offers,
            "count": len(filtered_offers),
            "scraped_count": len(all_offers),
            "deduplicated_count": len(deduplicated_offers),
            "saved_count": saved_count,
            "platforms_scraped": list(raw_results.keys()),
            "search_params": {
                "keywords": keywords,
                "location": location,
                "job_type": job_type,
                "work_mode": work_mode,
                "company": company
            },
            "scraped_at": start_time.isoformat(),
            "duration_seconds": round(duration, 2)
        }
    
    async def get_feed(
        self,
        db: AsyncSession,
        user_id: str,
        profile_id: str,
        limit: int = 50,
        min_score: float = 60.0,
        max_age_days: int = 7
    ) -> Dict:
        """
        Récupère le feed personnalisé pour un utilisateur
        
        Args:
            db: Session DB
            user_id: ID utilisateur
            profile_id: ID profil candidat
            limit: Nombre max d'offres
            min_score: Score minimum de compatibilité (0-100)
            max_age_days: Âge maximum des offres en jours
        
        Returns:
            Dict avec offres triées par score + métadonnées
        """
        print(f"[SearchService] get_feed: user={user_id}, profile={profile_id}, limit={limit}")
        
        # 1. Récupérer le profil
        profile_query = select(Profile).where(Profile.id == profile_id)
        result = await db.execute(profile_query)
        profile = result.scalar_one_or_none()
        
        if not profile:
            return {
                "success": False,
                "error": "Profile not found",
                "offers": [],
                "count": 0
            }
        
        # 2. Récupérer les offres récentes (< max_age_days)
        cutoff_date = datetime.utcnow() - timedelta(days=max_age_days)
        
        offers_query = select(JobOffer).where(
            and_(
                JobOffer.scraped_at >= cutoff_date,
                JobOffer.scraped_at.isnot(None)
            )
        ).order_by(desc(JobOffer.scraped_at)).limit(200)  # Limite pour performance
        
        result = await db.execute(offers_query)
        recent_offers = result.scalars().all()
        
        print(f"[SearchService] {len(recent_offers)} offres récentes trouvées")
        
        if not recent_offers:
            return {
                "success": True,
                "offers": [],
                "count": 0,
                "message": "Aucune offre récente disponible"
            }
        
        # 3. Vérifier cache existant
        cache_query = select(UserFeedCache).where(
            and_(
                UserFeedCache.user_id == user_id,
                UserFeedCache.profile_id == profile_id,
                UserFeedCache.expires_at > datetime.utcnow()
            )
        )
        result = await db.execute(cache_query)
        cached_scores = {cache.job_offer_id: cache.compatibility_score 
                        for cache in result.scalars().all()}
        
        print(f"[SearchService] {len(cached_scores)} scores en cache")
        
        # 4. Calculer scores pour offres non cachées
        offers_with_scores = []
        
        for offer in recent_offers:
            # Utiliser cache si disponible
            if offer.id in cached_scores:
                score = cached_scores[offer.id]
            else:
                # Calculer nouveau score
                try:
                    score_result = await self.ai_service.calculate_compatibility(
                        profile_data=self._profile_to_dict(profile),
                        job_data=self._offer_to_dict(offer)
                    )
                    score = score_result.get("overall_score", 0)
                    
                    # Mettre en cache (expire dans 24h)
                    await self._cache_score(
                        db, user_id, profile_id, offer.id, score
                    )
                except Exception as e:
                    print(f"[SearchService] Erreur calcul score pour offre {offer.id}: {e}")
                    score = 0
            
            # Filtrer par score minimum
            if score >= min_score:
                offers_with_scores.append({
                    "offer": offer,
                    "compatibility_score": score
                })
        
        # 5. Trier par score décroissant
        offers_with_scores.sort(key=lambda x: x["compatibility_score"], reverse=True)
        
        # 6. Limiter résultats
        top_offers = offers_with_scores[:limit]
        
        print(f"[SearchService] {len(top_offers)} offres après filtrage score >= {min_score}")
        
        # 7. Formater réponse
        formatted_offers = []
        for item in top_offers:
            offer = item["offer"]
            formatted_offers.append({
                "id": str(offer.id),
                "title": offer.title,
                "company": offer.company,
                "location": offer.location,
                "description": offer.description[:500] if offer.description else "",
                "url": offer.source_url,
                "source_platform": offer.source_platform,
                "job_type": offer.job_type,
                "work_mode": offer.work_mode,
                "scraped_at": offer.scraped_at.isoformat() if offer.scraped_at else None,
                "compatibility_score": round(item["compatibility_score"], 1)
            })
        
        return {
            "success": True,
            "offers": formatted_offers,
            "count": len(formatted_offers),
            "total_analyzed": len(recent_offers),
            "min_score_applied": min_score,
            "max_age_days": max_age_days
        }
    
    async def deduplicate_offers(self, offers: List[Dict]) -> List[Dict]:
        """
        Déduplique les offres par URL et similarité titre+entreprise
        
        Args:
            offers: Liste d'offres brutes
        
        Returns:
            Liste d'offres dédupliquées
        """
        if not offers:
            return []
        
        seen_urls = set()
        seen_signatures = set()
        deduplicated = []
        
        for offer in offers:
            # Déduplication par URL (exact)
            url = offer.get("url", "")
            if url and url in seen_urls:
                continue
            
            # Déduplication par signature (titre + entreprise)
            title = offer.get("title", "").lower().strip()
            company = offer.get("company", "").lower().strip()
            signature = f"{title}|{company}"
            
            # Vérifier similarité avec signatures existantes
            is_duplicate = False
            for existing_sig in seen_signatures:
                similarity = SequenceMatcher(None, signature, existing_sig).ratio()
                if similarity >= self.deduplication_threshold:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                deduplicated.append(offer)
                if url:
                    seen_urls.add(url)
                seen_signatures.add(signature)
        
        return deduplicated
    
    def _filter_offers(
        self,
        offers: List[Dict],
        job_type: Optional[str] = None,
        work_mode: Optional[str] = None,
        company: Optional[str] = None
    ) -> List[Dict]:
        """Filtre les offres selon critères"""
        filtered = offers
        
        if job_type:
            filtered = [o for o in filtered if o.get("job_type", "").lower() == job_type.lower()]
        
        if work_mode:
            filtered = [o for o in filtered if o.get("work_mode", "").lower() == work_mode.lower()]
        
        if company:
            filtered = [o for o in filtered 
                       if company.lower() in o.get("company", "").lower()]
        
        return filtered
    
    async def _save_offers_to_db(
        self,
        db: AsyncSession,
        offers: List[Dict]
    ) -> int:
        """
        Sauvegarde les offres en DB avec génération d'embeddings
        Utilise UPSERT pour éviter les doublons
        
        Returns:
            Nombre d'offres sauvegardées
        """
        if not offers:
            return 0
        
        saved_count = 0
        
        for offer_data in offers:
            try:
                # Générer hash unique pour déduplication DB
                offer_hash = self._generate_offer_hash(offer_data)
                
                # Vérifier si offre existe déjà
                existing_query = select(JobOffer).where(
                    or_(
                        JobOffer.source_url == offer_data.get("url"),
                        JobOffer.title == offer_data.get("title")
                    )
                ).limit(1)
                result = await db.execute(existing_query)
                existing = result.scalar_one_or_none()
                
                if existing:
                    # Offre existe déjà, skip
                    continue
                
                # Générer embedding pour description
                embedding = None
                description = offer_data.get("description", "")
                if description:
                    try:
                        embedding = await self.ai_service.generate_embedding(description)
                    except Exception as e:
                        print(f"[SearchService] Erreur génération embedding: {e}")
                
                # Créer nouvelle offre
                new_offer = JobOffer(
                    title=offer_data.get("title", ""),
                    company=offer_data.get("company", "Non spécifié"),
                    location=offer_data.get("location", "Non spécifié"),
                    description=description,
                    requirements=offer_data.get("requirements", ""),
                    source_url=offer_data.get("url", ""),
                    source_platform=offer_data.get("source_platform", "unknown"),
                    job_type=offer_data.get("job_type"),
                    work_mode=offer_data.get("work_mode"),
                    scraped_at=offer_data.get("scraped_at") or datetime.utcnow(),
                    embedding=embedding
                )
                
                db.add(new_offer)
                saved_count += 1
                
            except Exception as e:
                print(f"[SearchService] Erreur sauvegarde offre: {e}")
                continue
        
        # Commit batch
        try:
            await db.commit()
        except Exception as e:
            print(f"[SearchService] Erreur commit DB: {e}")
            await db.rollback()
            saved_count = 0
        
        return saved_count
    
    def _generate_offer_hash(self, offer_data: Dict) -> str:
        """Génère un hash unique pour une offre"""
        signature = f"{offer_data.get('title', '')}|{offer_data.get('company', '')}|{offer_data.get('url', '')}"
        return hashlib.md5(signature.encode()).hexdigest()
    
    async def _cache_score(
        self,
        db: AsyncSession,
        user_id: str,
        profile_id: str,
        job_offer_id: str,
        score: float
    ):
        """Met en cache un score de compatibilité"""
        try:
            cache_entry = UserFeedCache(
                user_id=user_id,
                profile_id=profile_id,
                job_offer_id=job_offer_id,
                compatibility_score=score,
                calculated_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
            db.add(cache_entry)
            await db.commit()
        except Exception as e:
            print(f"[SearchService] Erreur cache score: {e}")
            await db.rollback()
    
    def _profile_to_dict(self, profile: Profile) -> Dict:
        """Convertit un profil en dict pour AI"""
        return {
            "title": profile.current_title or "",
            "summary": profile.summary or "",
            "skills": profile.skills or [],
            "experience_years": 0,  # TODO: calculer depuis experiences
        }
    
    def _offer_to_dict(self, offer: JobOffer) -> Dict:
        """Convertit une offre en dict pour AI"""
        return {
            "title": offer.title,
            "description": offer.description or "",
            "requirements": offer.requirements or "",
            "company": offer.company,
            "location": offer.location
        }
    async def search_hybrid(
        self,
        db: AsyncSession,
        user_id: str,
        keywords: Optional[str] = None,
        location: Optional[str] = None,
        job_type: Optional[str] = None,
        company: Optional[str] = None,
        enable_scraping: bool = True,
        limit: int = 50
    ) -> Dict:
        """
        Recherche hybride: DB locale + Scraping Internet
        
        1. Cherche dans la DB de l'utilisateur
        2. Si scraping activé, lance le scraping
        3. Combine et déduplique les résultats
        4. Retourne la liste unifiée
        
        Args:
            db: Session DB
            user_id: ID utilisateur
            keywords: Mots-clés de recherche
            location: Localisation
            job_type: Type de contrat (Stage, CDI, etc.)
            company: Nom d'entreprise
            enable_scraping: Active/désactive le scraping
            limit: Nombre max de résultats
            
        Returns:
            Dict avec offres combinées et métadonnées
        """
        from app.services.job_offer_service import JobOfferService
        from uuid import UUID
        
        results = {
            "offers": [],
            "db_count": 0,
            "scraped_count": 0,
            "total_count": 0,
            "sources": []
        }
        
        # 1. Recherche dans la DB locale
        print(f"[SearchHybrid] Recherche DB pour user {user_id}")
        try:
            db_offers = await JobOfferService.search_job_offers(
                db=db,
                user_id=UUID(user_id),
                keyword=keywords,
                location=location,
                job_type=job_type,
                company_name=company,
                limit=limit,
                offset=0
            )
            
            # Convertir en format dict
            db_offers_dict = []
            for offer in db_offers:
                db_offers_dict.append({
                    "id": str(offer.id),
                    "title": offer.job_title,
                    "company": offer.company_name,
                    "location": offer.location,
                    "job_type": offer.job_type,
                    "description": offer.description,
                    "url": offer.source_url,
                    "source_platform": offer.source_platform or "database",
                    "created_at": offer.created_at.isoformat() if offer.created_at else None,
                    "source": "database"
                })
            
            results["db_count"] = len(db_offers_dict)
            results["sources"].append("database")
            print(f"[SearchHybrid] {len(db_offers_dict)} offres trouvées en DB")
            
        except Exception as e:
            print(f"[SearchHybrid] Erreur recherche DB: {e}")
            db_offers_dict = []
        
        # 2. Scraping Internet (si activé et keywords fourni)
        scraped_offers_dict = []
        if enable_scraping and keywords:
            print(f"[SearchHybrid] Lancement scraping pour '{keywords}'")
            try:
                scraping_result = await self.search_with_scraping(
                    db=db,
                    keywords=keywords,
                    location=location,
                    job_type=job_type,
                    company=company,
                    limit_per_platform=30,
                    user_id=user_id
                )
                
                # Convertir les offres scrapées au même format
                for offer in scraping_result.get("offers", []):
                    scraped_offers_dict.append({
                        "id": offer.get("id", ""),
                        "title": offer.get("title", ""),
                        "company": offer.get("company", ""),
                        "location": offer.get("location", ""),
                        "job_type": offer.get("job_type", ""),
                        "description": offer.get("description", ""),
                        "url": offer.get("url", ""),
                        "source_platform": offer.get("source_platform", "unknown"),
                        "created_at": offer.get("scraped_at"),
                        "source": "scraping"
                    })
                
                results["scraped_count"] = len(scraped_offers_dict)
                results["sources"].append("scraping")
                print(f"[SearchHybrid] {len(scraped_offers_dict)} offres scrapées")
                
            except Exception as e:
                print(f"[SearchHybrid] Erreur scraping: {e}")
                import traceback
                traceback.print_exc()
        
        # 3. Combiner les résultats
        all_offers = db_offers_dict + scraped_offers_dict
        print(f"[SearchHybrid] {len(all_offers)} offres avant déduplication")
        
        # 4. Déduplication (par URL et titre+entreprise)
        deduplicated = []
        seen_urls = set()
        seen_signatures = set()
        
        for offer in all_offers:
            # Déduplication par URL
            url = offer.get("url", "")
            if url and url in seen_urls:
                continue
            
            # Déduplication par signature
            title = offer.get("title", "").lower().strip()
            company = offer.get("company", "").lower().strip()
            signature = f"{title}|{company}"
            
            if signature in seen_signatures:
                continue
            
            # Ajouter l'offre
            deduplicated.append(offer)
            if url:
                seen_urls.add(url)
            if signature:
                seen_signatures.add(signature)
        
        print(f"[SearchHybrid] {len(deduplicated)} offres après déduplication")
        
        # 5. Limiter les résultats
        final_offers = deduplicated[:limit]
        
        results["offers"] = final_offers
        results["total_count"] = len(final_offers)
        
        return results



# Instance globale
search_service = SearchService()
