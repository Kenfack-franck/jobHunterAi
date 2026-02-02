"""
Service de veille entreprise (Company Watch)
Permet aux utilisateurs de surveiller les offres d'entreprises spécifiques
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc
from sqlalchemy.orm import selectinload

from app.models.watched_company import WatchedCompany, UserCompanyWatch
from app.models.job_offer import JobOffer
from app.models.profile import Profile
from app.services.scraping_service import ScrapingService
from app.services.ai_service import AIService


class CompanyWatchService:
    """Service de gestion de la veille entreprise"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai_service = AIService()
    
    async def add_company_watch(
        self,
        user_id: UUID,
        company_name: str,
        profile_id: Optional[UUID] = None,
        alert_threshold: int = 70,
        linkedin_url: Optional[str] = None,
        careers_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ajoute une entreprise à surveiller pour un utilisateur
        
        Args:
            user_id: ID utilisateur
            company_name: Nom de l'entreprise
            profile_id: ID profil pour scoring (optionnel)
            alert_threshold: Score minimum pour alerte (défaut: 70)
            linkedin_url: URL LinkedIn entreprise (optionnel)
            careers_url: URL page carrières (optionnel)
        
        Returns:
            Dict avec informations sur la veille créée
        """
        # Normaliser le nom d'entreprise
        company_slug = self._slugify_company_name(company_name)
        
        # Vérifier si l'entreprise existe déjà (mutualisation)
        query = select(WatchedCompany).where(WatchedCompany.company_slug == company_slug)
        result = await self.db.execute(query)
        company = result.scalar_one_or_none()
        
        if not company:
            # Créer nouvelle entreprise surveillée
            company = WatchedCompany(
                company_name=company_name,
                company_slug=company_slug,
                linkedin_url=linkedin_url,
                careers_url=careers_url,
                total_watchers=0,
                total_offers_found=0,
                scraping_frequency=24  # Par défaut: 1x/jour
            )
            self.db.add(company)
            await self.db.flush()
        
        # Vérifier si l'utilisateur surveille déjà cette entreprise
        watch_query = select(UserCompanyWatch).where(
            and_(
                UserCompanyWatch.user_id == user_id,
                UserCompanyWatch.watched_company_id == company.id
            )
        )
        result = await self.db.execute(watch_query)
        existing_watch = result.scalar_one_or_none()
        
        if existing_watch:
            return {
                "success": False,
                "message": f"Vous surveillez déjà {company_name}",
                "watch_id": str(existing_watch.id),
                "company_id": str(company.id)
            }
        
        # Créer la relation utilisateur → entreprise
        user_watch = UserCompanyWatch(
            user_id=user_id,
            watched_company_id=company.id,
            profile_id=profile_id,
            alert_threshold=alert_threshold
        )
        self.db.add(user_watch)
        
        # Incrémenter le compteur de watchers
        company.total_watchers += 1
        
        await self.db.commit()
        
        # Lancer un scraping immédiat pour cette entreprise (optionnel)
        # await self._scrape_company_offers(company)
        
        return {
            "success": True,
            "message": f"Veille activée pour {company_name}",
            "watch_id": str(user_watch.id),
            "company_id": str(company.id),
            "company_slug": company_slug,
            "total_watchers": company.total_watchers
        }
    
    async def get_user_watches(
        self,
        user_id: UUID,
        page: int = 1,
        per_page: int = 20
    ) -> Dict[str, Any]:
        """
        Récupère toutes les veilles d'un utilisateur
        
        Args:
            user_id: ID utilisateur
            page: Page (pagination)
            per_page: Résultats par page
        
        Returns:
            Dict avec liste des veilles et métadonnées
        """
        # Requête avec jointure pour récupérer les infos de l'entreprise
        offset = (page - 1) * per_page
        query = (
            select(UserCompanyWatch)
            .options(selectinload(UserCompanyWatch.watched_company))
            .where(UserCompanyWatch.user_id == user_id)
            .order_by(desc(UserCompanyWatch.created_at))
            .offset(offset)
            .limit(per_page)
        )
        result = await self.db.execute(query)
        watches = result.scalars().all()
        
        # Compter le total
        count_query = select(func.count(UserCompanyWatch.id)).where(
            UserCompanyWatch.user_id == user_id
        )
        total = (await self.db.execute(count_query)).scalar()
        
        # Formater les résultats
        formatted_watches = []
        for watch in watches:
            company = watch.watched_company
            formatted_watches.append({
                "watch_id": str(watch.id),
                "company_id": str(company.id),
                "company_name": company.company_name,
                "company_slug": company.company_slug,
                "alert_threshold": watch.alert_threshold,
                "profile_id": str(watch.profile_id) if watch.profile_id else None,
                "total_watchers": company.total_watchers,
                "total_offers_found": company.total_offers_found,
                "last_scraped_at": company.last_scraped_at.isoformat() if company.last_scraped_at else None,
                "linkedin_url": company.linkedin_url,
                "careers_url": company.careers_url,
                "created_at": watch.created_at.isoformat()
            })
        
        return {
            "success": True,
            "watches": formatted_watches,
            "count": len(formatted_watches),
            "total": total,
            "page": page,
            "per_page": per_page
        }
    
    async def remove_company_watch(
        self,
        user_id: UUID,
        watch_id: UUID
    ) -> Dict[str, Any]:
        """
        Supprime une veille entreprise pour un utilisateur
        
        Args:
            user_id: ID utilisateur
            watch_id: ID de la veille à supprimer
        
        Returns:
            Dict avec résultat de la suppression
        """
        # Récupérer la veille
        query = select(UserCompanyWatch).where(
            and_(
                UserCompanyWatch.id == watch_id,
                UserCompanyWatch.user_id == user_id
            )
        )
        result = await self.db.execute(query)
        watch = result.scalar_one_or_none()
        
        if not watch:
            return {
                "success": False,
                "message": "Veille non trouvée ou vous n'avez pas les droits"
            }
        
        company_id = watch.watched_company_id
        
        # Supprimer la veille
        await self.db.delete(watch)
        
        # Décrémenter le compteur de l'entreprise
        company_query = select(WatchedCompany).where(WatchedCompany.id == company_id)
        result = await self.db.execute(company_query)
        company = result.scalar_one_or_none()
        
        if company:
            company.total_watchers = max(0, company.total_watchers - 1)
            
            # Supprimer l'entreprise si plus personne ne la surveille
            if company.total_watchers == 0:
                await self.db.delete(company)
        
        await self.db.commit()
        
        return {
            "success": True,
            "message": "Veille supprimée avec succès"
        }
    
    async def get_company_offers(
        self,
        company_id: UUID,
        user_id: Optional[UUID] = None,
        profile_id: Optional[UUID] = None,
        limit: int = 50,
        min_score: int = 0
    ) -> Dict[str, Any]:
        """
        Récupère les offres d'une entreprise surveillée
        
        Args:
            company_id: ID entreprise surveillée
            user_id: ID utilisateur (optionnel, pour filtrer)
            profile_id: ID profil pour scoring (optionnel)
            limit: Nombre max d'offres
            min_score: Score minimum (si profile_id fourni)
        
        Returns:
            Dict avec liste des offres et scores
        """
        # Récupérer l'entreprise
        company_query = select(WatchedCompany).where(WatchedCompany.id == company_id)
        result = await self.db.execute(company_query)
        company = result.scalar_one_or_none()
        
        if not company:
            return {
                "success": False,
                "message": "Entreprise non trouvée"
            }
        
        # Récupérer les offres de cette entreprise (30 derniers jours)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        offers_query = (
            select(JobOffer)
            .where(
                and_(
                    JobOffer.company_name.ilike(f"%{company.company_name}%"),
                    JobOffer.scraped_at >= thirty_days_ago
                )
            )
            .order_by(desc(JobOffer.scraped_at))
            .limit(limit)
        )
        result = await self.db.execute(offers_query)
        offers = result.scalars().all()
        
        # Si profile_id fourni, calculer scores de compatibilité
        formatted_offers = []
        if profile_id:
            # Récupérer le profil
            profile_query = select(CandidateProfile).where(CandidateProfile.id == profile_id)
            result = await self.db.execute(profile_query)
            profile = result.scalar_one_or_none()
            
            if profile and profile.embedding:
                for offer in offers:
                    if offer.embedding:
                        # Calculer score sémantique
                        score = await self.ai_service.calculate_compatibility_score(
                            profile_embedding=profile.embedding,
                            offer_embedding=offer.embedding
                        )
                        
                        if score >= min_score:
                            formatted_offers.append({
                                "id": str(offer.id),
                                "title": offer.job_title,
                                "company": offer.company_name,
                                "location": offer.location,
                                "job_type": offer.job_type,
                                "work_mode": offer.work_mode,
                                "url": offer.source_url,
                                "scraped_at": offer.scraped_at.isoformat() if offer.scraped_at else None,
                                "compatibility_score": round(score, 2)
                            })
                    else:
                        # Pas d'embedding, ajouter sans score
                        formatted_offers.append({
                            "id": str(offer.id),
                            "title": offer.job_title,
                            "company": offer.company_name,
                            "location": offer.location,
                            "job_type": offer.job_type,
                            "work_mode": offer.work_mode,
                            "url": offer.source_url,
                            "scraped_at": offer.scraped_at.isoformat() if offer.scraped_at else None,
                            "compatibility_score": None
                        })
            else:
                # Profil sans embedding, retourner offres sans score
                for offer in offers:
                    formatted_offers.append({
                        "id": str(offer.id),
                        "title": offer.job_title,
                        "company": offer.company_name,
                        "location": offer.location,
                        "job_type": offer.job_type,
                        "work_mode": offer.work_mode,
                        "url": offer.source_url,
                        "scraped_at": offer.scraped_at.isoformat() if offer.scraped_at else None,
                        "compatibility_score": None
                    })
        else:
            # Pas de profil, retourner toutes les offres sans score
            for offer in offers:
                formatted_offers.append({
                    "id": str(offer.id),
                    "title": offer.job_title,
                    "company": offer.company_name,
                    "location": offer.location,
                    "job_type": offer.job_type,
                    "work_mode": offer.work_mode,
                    "url": offer.source_url,
                    "scraped_at": offer.scraped_at.isoformat() if offer.scraped_at else None,
                    "compatibility_score": None
                })
        
        # Trier par score décroissant si scores disponibles
        if profile_id:
            formatted_offers.sort(key=lambda x: x.get("compatibility_score") or 0, reverse=True)
        
        return {
            "success": True,
            "company_name": company.company_name,
            "company_slug": company.company_slug,
            "offers": formatted_offers,
            "count": len(formatted_offers),
            "total_offers_found": company.total_offers_found,
            "last_scraped_at": company.last_scraped_at.isoformat() if company.last_scraped_at else None
        }
    
    async def scrape_watched_companies(self) -> Dict[str, Any]:
        """
        Scrape toutes les entreprises surveillées (tâche Celery)
        Mutualisation: 1 scraping pour N users
        
        Returns:
            Dict avec statistiques du scraping
        """
        from app.models.job_offer import JobOffer
        from datetime import datetime
        
        # Récupérer toutes les entreprises avec watchers actifs
        query = select(WatchedCompany).where(WatchedCompany.total_watchers > 0)
        result = await self.db.execute(query)
        companies = result.scalars().all()
        
        total_companies = len(companies)
        total_offers = 0
        total_saved = 0
        errors = []
        
        print(f"[CompanyWatch] Scraping {total_companies} entreprises surveillées...")
        
        for company in companies:
            try:
                print(f"[CompanyWatch] Scraping {company.company_name}...")
                
                # Scraper les offres pour cette entreprise
                offers = await self._scrape_company_offers(company)
                total_offers += len(offers)
                
                # Sauvegarder les offres en DB
                saved_count = 0
                for offer_data in offers:
                    try:
                        # Vérifier si l'offre existe déjà (par URL)
                        existing_query = select(JobOffer).where(
                            JobOffer.source_url == offer_data.get("url")
                        )
                        existing = (await self.db.execute(existing_query)).scalar_one_or_none()
                        
                        if not existing:
                            # Créer nouvelle offre
                            # Récupérer les watchers pour assigner user_id
                            watch_query = select(UserCompanyWatch).where(
                                UserCompanyWatch.watched_company_id == company.id
                            ).limit(1)
                            first_watch = (await self.db.execute(watch_query)).scalar_one_or_none()
                            
                            if first_watch:
                                job_offer = JobOffer(
                                    user_id=first_watch.user_id,  # Assigner au premier watcher
                                    job_title=offer_data.get("title"),
                                    company_name=company.company_name,
                                    location=offer_data.get("location"),
                                    job_type=offer_data.get("job_type"),
                                    work_mode=offer_data.get("work_mode", "onsite"),
                                    description=offer_data.get("description", "")[:5000],
                                    source_url=offer_data.get("url"),
                                    source_platform=offer_data.get("source", "indeed"),
                                    scraped_at=datetime.utcnow()
                                )
                                self.db.add(job_offer)
                                saved_count += 1
                    
                    except Exception as e:
                        print(f"[CompanyWatch] Erreur sauvegarde offre: {str(e)}")
                
                # Commit par entreprise
                await self.db.commit()
                total_saved += saved_count
                
                # Mettre à jour les stats de l'entreprise
                company.total_offers_found += saved_count
                company.last_scraped_at = datetime.utcnow()
                
                print(f"[CompanyWatch] ✅ {company.company_name}: {len(offers)} trouvées, {saved_count} sauvegardées")
                
            except Exception as e:
                print(f"[CompanyWatch] ❌ Erreur {company.company_name}: {str(e)}")
                errors.append({
                    "company": company.company_name,
                    "error": str(e)
                })
        
        await self.db.commit()
        
        return {
            "success": True,
            "total_companies_scraped": total_companies,
            "total_offers_found": total_offers,
            "total_offers_saved": total_saved,
            "errors_count": len(errors),
            "errors": errors
        }
    
    async def _scrape_company_offers(self, company: WatchedCompany) -> List[Dict[str, Any]]:
        """
        Scrape les offres d'une entreprise spécifique
        
        Stratégie multi-sources (par ordre de priorité) :
        1. Indeed avec filtre entreprise (fallback principal)
        2. RemoteOK si offres remote (recherche par company)
        3. Career page si fournie (TODO)
        
        Args:
            company: Entreprise à scraper
        
        Returns:
            Liste des offres trouvées
        """
        offers = []
        
        try:
            # Import local pour éviter erreurs circulaires
            from app.services.scrapers.indeed_scraper import IndeedScraper
            from app.services.scrapers.remoteok_scraper import RemoteOKScraper
            
            # Méthode 1 : Indeed avec filtre entreprise (priorité principale)
            print(f"[CompanyWatch] Scraping {company.company_name} via Indeed...")
            try:
                indeed_scraper = IndeedScraper()
                indeed_offers = await indeed_scraper.scrape(
                    keywords="",  # Vide = toutes offres de l'entreprise
                    company=company.company_name,
                    location="France",
                    max_results=50
                )
                offers.extend(indeed_offers)
                print(f"[CompanyWatch] ✅ Indeed : {len(indeed_offers)} offres trouvées")
            except Exception as e:
                print(f"[CompanyWatch] ❌ Indeed error: {str(e)}")
            
            # Méthode 2 : RemoteOK (pour offres remote)
            print(f"[CompanyWatch] Scraping {company.company_name} via RemoteOK...")
            try:
                remoteok_scraper = RemoteOKScraper()
                # RemoteOK recherche par keywords (company name)
                remote_offers = await remoteok_scraper.scrape(
                    keywords=company.company_name,
                    location=None,
                    max_results=30
                )
                # Filtrer avec fuzzy matching (75%+ similarité)
                filtered_remote = [
                    o for o in remote_offers 
                    if self._fuzzy_match_company(
                        company.company_name, 
                        o.get("company", ""),
                        threshold=0.75  # 75% similarité minimum
                    )
                ]
                offers.extend(filtered_remote)
                print(f"[CompanyWatch] ✅ RemoteOK : {len(filtered_remote)}/{len(remote_offers)} offres matchées (fuzzy 75%)")
            except Exception as e:
                print(f"[CompanyWatch] ❌ RemoteOK error: {str(e)}")
            
            # TODO Méthode 3 : Career page si fournie
            # if company.careers_url:
            #     career_offers = await self._scrape_career_page(company.careers_url)
            #     offers.extend(career_offers)
            
            # TODO Méthode 4 : LinkedIn Jobs si URL fournie
            # if company.linkedin_url:
            #     linkedin_offers = await self._scrape_linkedin_jobs(company.linkedin_url)
            #     offers.extend(linkedin_offers)
            
            print(f"[CompanyWatch] Total offres {company.company_name}: {len(offers)}")
            
        except Exception as e:
            print(f"[CompanyWatch] Erreur scraping {company.company_name}: {str(e)}")
        
        return offers
    
    def _normalize_company_name(self, name: str) -> str:
        """
        Normalise un nom d'entreprise pour matching
        
        Args:
            name: Nom brut de l'entreprise
        
        Returns:
            Nom normalisé (lowercase, sans suffixes légaux)
        """
        import re
        
        # Lowercase
        normalized = name.lower().strip()
        
        # Supprimer suffixes légaux communs
        suffixes = [
            r'\s+(inc\.?|incorporated)$',
            r'\s+(llc\.?|ltd\.?|limited)$',
            r'\s+(corp\.?|corporation)$',
            r'\s+(sa|sas|sarl|sasu)$',
            r'\s+(gmbh|ag)$',
            r'\s+(bv|nv)$',
            r'\s+company$',
            r'\s+group$',
        ]
        
        for suffix_pattern in suffixes:
            normalized = re.sub(suffix_pattern, '', normalized, flags=re.IGNORECASE)
        
        # Supprimer caractères spéciaux
        normalized = re.sub(r'[^\w\s]', '', normalized)
        
        # Supprimer espaces multiples
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        return normalized
    
    def _fuzzy_match_company(self, company_name: str, offer_company: str, threshold: float = 0.75) -> bool:
        """
        Vérifie si deux noms d'entreprises matchent (fuzzy)
        
        Args:
            company_name: Nom entreprise surveillée
            offer_company: Nom entreprise dans l'offre
            threshold: Seuil de similarité (0.0-1.0, défaut: 0.75)
        
        Returns:
            True si match, False sinon
        """
        from difflib import SequenceMatcher
        
        # Normaliser les deux noms
        norm_company = self._normalize_company_name(company_name)
        norm_offer = self._normalize_company_name(offer_company)
        
        # Match exact après normalisation
        if norm_company == norm_offer:
            return True
        
        # Match si l'un contient l'autre (après normalisation)
        if norm_company in norm_offer or norm_offer in norm_company:
            return True
        
        # Fuzzy matching avec SequenceMatcher
        similarity = SequenceMatcher(None, norm_company, norm_offer).ratio()
        
        return similarity >= threshold
    
    async def _scrape_and_save_company_offers(
        self,
        company_name: str,
        company_id: UUID,
        user_id: Optional[UUID] = None
    ) -> int:
        """
        Scrappe une entreprise ET sauvegarde les offres en DB.
        Utilisé par les tâches Celery.
        
        Args:
            company_name: Nom de l'entreprise
            company_id: ID de l'entreprise en DB
            user_id: ID utilisateur (optionnel, pour attribution)
            
        Returns:
            Nombre d'offres trouvées et sauvegardées
        """
        from app.models.job_offer import JobOffer
        from sqlalchemy import select
        
        # Récupérer l'objet company
        stmt = select(WatchedCompany).where(WatchedCompany.id == company_id)
        result = await self.db.execute(stmt)
        company = result.scalar_one()
        
        # Scraper
        offers = await self._scrape_company_offers(company)
        
        if not offers:
            # Mettre à jour last_scraped_at même si 0 offres
            company.last_scraped_at = datetime.now()
            await self.db.commit()
            return 0
        
        # Sauvegarder les offres (dédoublonnage par source_url)
        saved_count = 0
        for offer_data in offers:
            # Vérifier si existe déjà
            check_stmt = select(JobOffer).where(
                JobOffer.source_url == offer_data.get('url')
            )
            existing = await self.db.execute(check_stmt)
            if existing.scalar_one_or_none():
                continue  # Skip si déjà en DB
            
            # Créer nouvelle offre
            job_offer = JobOffer(
                user_id=user_id,  # Peut être None pour scraping global
                job_title=offer_data.get('title'),
                company_name=company_name,
                location=offer_data.get('location'),
                contract_type=offer_data.get('contract_type'),
                work_mode=offer_data.get('work_mode'),
                salary=offer_data.get('salary'),
                description=offer_data.get('description'),
                required_skills=offer_data.get('required_skills', []),
                source_platform=offer_data.get('source', 'scraping'),
                source_url=offer_data.get('url'),
                scraped_at=datetime.now()
            )
            
            self.db.add(job_offer)
            saved_count += 1
        
        # Mettre à jour la company
        company.last_scraped_at = datetime.now()
        company.total_offers_found += saved_count
        
        await self.db.commit()
        
        return saved_count
    
    def _slugify_company_name(self, company_name: str) -> str:
        """
        Crée un slug unique à partir du nom de l'entreprise
        
        Args:
            company_name: Nom de l'entreprise
        
        Returns:
            Slug normalisé (ex: "Google" -> "google", "LVMH Group" -> "lvmh-group")
        """
        import re
        # Convertir en minuscules
        slug = company_name.lower()
        # Supprimer les accents
        slug = slug.replace('é', 'e').replace('è', 'e').replace('ê', 'e')
        slug = slug.replace('à', 'a').replace('â', 'a')
        slug = slug.replace('ù', 'u').replace('û', 'u')
        slug = slug.replace('ô', 'o').replace('ö', 'o')
        slug = slug.replace('ç', 'c')
        # Remplacer espaces et caractères spéciaux par tirets
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        # Supprimer tirets début/fin
        slug = slug.strip('-')
        return slug
