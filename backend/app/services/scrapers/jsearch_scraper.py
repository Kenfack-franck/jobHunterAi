"""
JSearch Scraper - API RapidAPI pour LinkedIn, Indeed, Glassdoor
Difficulté : Très faible (API REST sécurisée)
Rate limit : Gratuit 100 req/mois → Payant $10/mois pour 1000 req
Focus : Agrégateur global (LinkedIn + Indeed + Glassdoor + ZipRecruiter)
"""
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
import aiohttp
import os

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.scraping_service import BaseScraper


class JSearchScraper(BaseScraper):
    """Scraper pour JSearch API (LinkedIn + Indeed + Glassdoor via RapidAPI)"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://jsearch.p.rapidapi.com/search"
        
        # Clé API RapidAPI (à configurer)
        # Pour obtenir la clé :
        # 1. S'inscrire sur https://rapidapi.com
        # 2. S'abonner à JSearch API (gratuit 100 req/mois)
        # 3. Copier X-RapidAPI-Key
        self.api_key = os.getenv("RAPIDAPI_KEY", "VOTRE_CLE_RAPIDAPI")
        
        self.max_results_per_page = 10  # JSearch max 10 par page
        self.max_offers = 3  # LIMITE À 3 pour les tests (changeable ensuite)
    
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
        Scrape offres depuis JSearch API (LinkedIn + Indeed + Glassdoor).
        
        Args:
            keywords: Mots-clés de recherche (ex: "Python Developer")
            location: Localisation (ex: "Paris", "Remote")
            job_type: Type de contrat (fulltime, contract, internship, etc.)
            work_mode: Mode de travail (remote, hybrid, onsite)
            company: Nom de l'entreprise
            max_results: Nombre maximum de résultats
        
        Returns:
            Liste de dictionnaires contenant les offres
        """
        # Vérifier la clé API
        if self.api_key == "VOTRE_CLE_RAPIDAPI":
            print("[JSearch] ⚠️ Clé API non configurée. Voir SCRAPERS_CONFIG.md")
            return []
        
        try:
            print(f"[JSearch] Début scraping: keywords={keywords}, location={location}")
            
            offers = await self._scrape_from_api(
                keywords=keywords,
                location=location,
                job_type=job_type,
                work_mode=work_mode,
                company=company,
                max_results=max_results
            )
            
            print(f"[JSearch] Scraping terminé. {len(offers)} offres récupérées.")
            return offers
        
        except Exception as e:
            print(f"[JSearch] Erreur lors du scraping: {str(e)}")
            # Ne pas lever d'exception pour ne pas bloquer les autres scrapers
            return []
    
    async def _scrape_from_api(
        self,
        keywords: Optional[str],
        location: Optional[str],
        job_type: Optional[str],
        work_mode: Optional[str],
        company: Optional[str],
        max_results: int
    ) -> List[Dict]:
        """
        Scraper depuis l'API JSearch.
        
        Documentation: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
        """
        offers = []
        
        # Construire la requête de recherche
        query_parts = []
        if keywords:
            query_parts.append(keywords)
        if company:
            query_parts.append(f"company:{company}")
        
        query = " ".join(query_parts) if query_parts else "software"
        
        # Construire les paramètres de recherche
        params = {
            "query": query,
            "num_pages": "1",  # On gérera la pagination manuellement
            "date_posted": "all",  # all, today, 3days, week, month
        }
        
        # Localisation
        if location:
            if location.lower() in ["remote", "télétravail", "teletravail"]:
                params["remote_jobs_only"] = "true"
            else:
                params["location"] = location
        
        # Type de contrat (JSearch utilise employment_types)
        if job_type:
            employment_type = self._map_job_type(job_type)
            if employment_type:
                params["employment_types"] = employment_type
        
        # Headers RapidAPI
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # JSearch supporte la pagination (page=1, 2, 3...)
                page = 1
                max_pages = min(10, (max_results // self.max_results_per_page) + 1)
                
                while page <= max_pages and len(offers) < max_results:
                    params["page"] = str(page)
                    
                    async with session.get(
                        self.base_url,
                        params=params,
                        headers=headers,
                        timeout=30
                    ) as response:
                        if response.status != 200:
                            error_text = await response.text()
                            print(f"[JSearch] API error: status {response.status} - {error_text}")
                            break
                        
                        data = await response.json()
                        
                        # Vérifier les résultats
                        results = data.get("data", [])
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
                                print(f"[JSearch] Erreur parsing job: {str(e)}")
                                continue
                        
                        # Passer à la page suivante
                        page += 1
                        
                        # Pause pour respecter rate limit
                        await asyncio.sleep(1)
        
        except asyncio.TimeoutError:
            print("[JSearch] Timeout lors de la requête API")
        except Exception as e:
            print(f"[JSearch] Erreur API: {str(e)}")
        
        return offers
    
    def _parse_api_job(self, job: Dict) -> Optional[Dict]:
        """Parser un job depuis l'API"""
        try:
            # ID de l'offre
            job_id = job.get("job_id")
            if not job_id:
                return None
            
            # Titre
            title = job.get("job_title", "").strip()
            if not title:
                return None
            
            # Entreprise
            company_name = job.get("employer_name", "Non spécifié").strip()
            
            # Description
            description = job.get("job_description", "").strip()
            if len(description) > 1000:
                description = description[:1000] + "..."
            
            # URL
            url = job.get("job_apply_link") or job.get("job_google_link", "")
            if not url:
                return None
            
            # Localisation
            location_city = job.get("job_city", "")
            location_country = job.get("job_country", "")
            location_state = job.get("job_state", "")
            
            location_parts = [p for p in [location_city, location_state, location_country] if p]
            location_display = ", ".join(location_parts) if location_parts else "Non spécifié"
            
            # Remote
            is_remote = job.get("job_is_remote", False)
            if is_remote:
                location_display = "Remote"
            
            # Salaire
            salary = None
            salary_min = job.get("job_min_salary")
            salary_max = job.get("job_max_salary")
            salary_currency = job.get("job_salary_currency", "USD")
            
            if salary_min and salary_max:
                salary = f"{salary_currency} {int(salary_min):,} - {int(salary_max):,}"
            elif salary_min:
                salary = f"{salary_currency} {int(salary_min):,}+"
            
            # Date de publication
            posted_at = job.get("job_posted_at_datetime_utc")
            posted_date = None
            if posted_at:
                try:
                    posted_date = datetime.fromisoformat(posted_at.replace("Z", "+00:00"))
                except:
                    pass
            
            # Type de contrat
            employment_type = job.get("job_employment_type", "FULLTIME")
            job_type = self._parse_employment_type(employment_type)
            
            # Mode de travail
            work_mode = "remote" if is_remote else "onsite"
            
            # Logo entreprise
            logo_url = job.get("employer_logo")
            
            # Source (LinkedIn, Indeed, etc.)
            job_source = job.get("job_publisher", "JSearch")
            
            offer = {
                "title": title,
                "company": company_name,
                "location": location_display,
                "description": description,
                "url": url,
                "source_platform": "jsearch",  # Badge principal
                "original_source": job_source,  # LinkedIn, Indeed, etc.
                "job_type": job_type,
                "work_mode": work_mode,
                "salary": salary,
                "posted_date": posted_date,
                "logo_url": logo_url,
                "scraped_at": datetime.utcnow()
            }
            
            return offer
        
        except Exception as e:
            print(f"[JSearch] Erreur parsing API job: {str(e)}")
            return None
    
    def _map_job_type(self, job_type: str) -> Optional[str]:
        """Mapper notre job_type vers JSearch employment_types"""
        mapping = {
            "fulltime": "FULLTIME",
            "parttime": "PARTTIME",
            "contract": "CONTRACTOR",
            "internship": "INTERN",
            "freelance": "CONTRACTOR"
        }
        return mapping.get(job_type.lower())
    
    def _parse_employment_type(self, employment_type: str) -> str:
        """Parser le type d'emploi de JSearch vers notre format"""
        mapping = {
            "FULLTIME": "fulltime",
            "PARTTIME": "parttime",
            "CONTRACTOR": "contract",
            "INTERN": "internship"
        }
        return mapping.get(employment_type, "fulltime")
