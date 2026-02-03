"""
Adzuna Scraper - API pour offres d'emploi France
Difficulté : Très faible (API REST publique)
Rate limit : 1000 req/mois (gratuit)
Focus : Offres France (Indeed, Monster, autres)
"""
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
import aiohttp

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.scraping_service import BaseScraper


class AdzunaScraper(BaseScraper):
    """Scraper pour Adzuna API (offres France)"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.adzuna.com/v1/api/jobs"
        self.country = "fr"  # France
        
        # Clés API (demo keys - vous devez créer les vôtres sur https://developer.adzuna.com)
        # Pour MVP, on utilise les demo keys (limitées mais fonctionnelles)
        self.app_id = "b9bf21eb"  # À remplacer par votre APP_ID
        self.app_key = "55286951672061bdd3159854ba4d44b9"  # À remplacer par votre APP_KEY
        
        self.max_results_per_page = 50
        self.max_offers = 100
    
    async def scrape(
        self,
        keywords: Optional[str] = None,
        location: Optional[str] = None,
        job_type: Optional[str] = None,
        work_mode: Optional[str] = None,
        company: Optional[str] = None,
        max_results: int = 100
    ) -> List[Dict]:
        """
        Scrape offres depuis Adzuna API.
        
        Args:
            keywords: Mots-clés de recherche (ex: "Python Developer")
            location: Localisation (ex: "Paris", "Lyon")
            job_type: Type de contrat (fulltime, contract, internship, etc.)
            work_mode: Mode de travail (remote, hybrid, onsite)
            company: Nom de l'entreprise
            max_results: Nombre maximum de résultats
        
        Returns:
            Liste de dictionnaires contenant les offres
        """
        try:
            print(f"[Adzuna] Début scraping: keywords={keywords}, location={location}")
            
            offers = await self._scrape_from_api(
                keywords=keywords,
                location=location,
                company=company,
                max_results=max_results
            )
            
            # Filtrer par job_type et work_mode si nécessaire
            if job_type or work_mode:
                offers = self._filter_offers(offers, job_type, work_mode)
            
            print(f"[Adzuna] Scraping terminé. {len(offers)} offres récupérées.")
            return offers
        
        except Exception as e:
            print(f"[Adzuna] Erreur lors du scraping: {str(e)}")
            # Ne pas lever d'exception pour ne pas bloquer les autres scrapers
            return []
    
    async def _scrape_from_api(
        self,
        keywords: Optional[str],
        location: Optional[str],
        company: Optional[str],
        max_results: int
    ) -> List[Dict]:
        """
        Scraper depuis l'API Adzuna.
        
        Documentation: https://developer.adzuna.com/docs/search
        """
        offers = []
        
        # Si company fourni, l'ajouter aux keywords (Adzuna ne supporte pas le paramètre company séparé)
        search_keywords = keywords or ""
        if company:
            search_keywords = f"{search_keywords} {company}".strip()
            print(f"[Adzuna] Recherche avec filtrage: '{search_keywords}'")
        
        # Construire les paramètres de recherche
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "results_per_page": min(self.max_results_per_page, max_results),
            "what": search_keywords,  # Mots-clés + entreprise
            "where": location or "France",  # Localisation (par défaut France)
            "content-type": "application/json"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Adzuna supporte la pagination (page=1, 2, 3...)
                page = 1
                max_pages = (max_results // self.max_results_per_page) + 1
                
                while page <= max_pages and len(offers) < max_results:
                    # Construire l'URL avec page
                    url = f"{self.base_url}/{self.country}/search/{page}"
                    
                    async with session.get(url, params=params, timeout=30) as response:
                        if response.status != 200:
                            print(f"[Adzuna] API error: status {response.status}")
                            break
                        
                        data = await response.json()
                        
                        # Vérifier les résultats
                        results = data.get("results", [])
                        if not results:
                            break  # Pas de résultats, arrêter la pagination
                        
                        # Parser les offres
                        for job in results:
                            try:
                                offer = self._parse_api_job(job)
                                if offer:
                                    offers.append(offer)
                                
                                # Limiter le nombre de résultats
                                if len(offers) >= max_results:
                                    break
                            
                            except Exception as e:
                                print(f"[Adzuna] Erreur parsing job: {str(e)}")
                                continue
                        
                        # Passer à la page suivante
                        page += 1
                        
                        # Pause pour respecter rate limit
                        await asyncio.sleep(0.5)
        
        except asyncio.TimeoutError:
            print("[Adzuna] Timeout lors de la requête API")
        except Exception as e:
            print(f"[Adzuna] Erreur API: {str(e)}")
        
        return offers
    
    def _parse_api_job(self, job: Dict) -> Optional[Dict]:
        """Parser un job depuis l'API"""
        try:
            # ID de l'offre
            job_id = job.get("id")
            if not job_id:
                return None
            
            # Titre
            title = job.get("title", "").strip()
            if not title:
                return None
            
            # Entreprise
            company = job.get("company", {})
            company_name = company.get("display_name", "Non spécifié").strip()
            
            # Description
            description = job.get("description", "").strip()
            
            # URL
            url = job.get("redirect_url", "")
            if not url:
                return None
            
            # Localisation
            location_obj = job.get("location", {})
            location_display = location_obj.get("display_name", "Non spécifié")
            
            # Salaire
            salary = None
            salary_min = job.get("salary_min")
            salary_max = job.get("salary_max")
            if salary_min and salary_max:
                salary = f"€{int(salary_min):,} - €{int(salary_max):,}"
            elif salary_min:
                salary = f"€{int(salary_min):,}+"
            
            # Date de publication
            created = job.get("created")
            posted_date = None
            if created:
                try:
                    posted_date = datetime.fromisoformat(created.replace("Z", "+00:00"))
                except:
                    pass
            
            # Contrat type
            contract_type = job.get("contract_type", "").lower()
            contract_time = job.get("contract_time", "").lower()
            
            # Déterminer job_type
            job_type = self._detect_job_type(contract_type, contract_time, title, description)
            
            # Déterminer work_mode
            work_mode = self._detect_work_mode(title, description, location_display)
            
            # Catégorie
            category = job.get("category", {})
            category_label = category.get("label", "")
            
            offer = {
                "title": title,
                "company": company_name,
                "location": location_display,
                "description": description,
                "url": url,
                "source_platform": "adzuna",
                "job_type": job_type,
                "work_mode": work_mode,
                "salary": salary,
                "posted_date": posted_date,
                "category": category_label,
                "scraped_at": datetime.utcnow()
            }
            
            return offer
        
        except Exception as e:
            print(f"[Adzuna] Erreur parsing API job: {str(e)}")
            return None
    
    def _detect_job_type(self, contract_type: str, contract_time: str, title: str, description: str) -> str:
        """Détecter le type de contrat"""
        text = f"{contract_type} {contract_time} {title} {description}".lower()
        
        if any(kw in text for kw in ["stage", "intern", "internship", "stagiaire"]):
            return "internship"
        elif any(kw in text for kw in ["contract", "freelance", "contractor", "consultant"]):
            return "contract"
        elif "part" in contract_time or "temps partiel" in text:
            return "parttime"
        elif "permanent" in contract_type or "cdi" in text or "full" in contract_time:
            return "fulltime"
        else:
            return "fulltime"  # Par défaut
    
    def _detect_work_mode(self, title: str, description: str, location: str) -> str:
        """Détecter le mode de travail"""
        text = f"{title} {description} {location}".lower()
        
        if any(kw in text for kw in ["remote", "télétravail", "teletravail", "100% remote"]):
            return "remote"
        elif any(kw in text for kw in ["hybrid", "hybride", "mix"]):
            return "hybrid"
        else:
            return "onsite"  # Par défaut
    
    def _filter_offers(self, offers: List[Dict], job_type: Optional[str], work_mode: Optional[str]) -> List[Dict]:
        """Filtrer les offres par job_type et work_mode"""
        filtered = []
        
        for offer in offers:
            # Filtrer par job_type
            if job_type and offer.get("job_type") != job_type:
                continue
            
            # Filtrer par work_mode
            if work_mode and offer.get("work_mode") != work_mode:
                continue
            
            filtered.append(offer)
        
        return filtered
