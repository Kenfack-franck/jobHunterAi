"""
The Muse Scraper - API pour offres d'emploi Tech/Startups
Difficulté : Très faible (API REST publique)
Rate limit : Pas de limite stricte (API publique)
Focus : Tech, Startups, Remote-friendly
"""
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
import aiohttp

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.scraping_service import BaseScraper


class TheMuseScraper(BaseScraper):
    """Scraper pour The Muse API (offres tech/startups)"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.themuse.com/api/public/jobs"
        self.max_results_per_page = 100  # Max 100 par page selon la doc
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
        Scrape offres depuis The Muse API.
        
        Args:
            keywords: Mots-clés de recherche (ex: "Python Developer")
            location: Localisation (ex: "Remote", "San Francisco")
            job_type: Type de contrat (fulltime, contract, internship, etc.)
            work_mode: Mode de travail (remote, hybrid, onsite)
            company: Nom de l'entreprise
            max_results: Nombre maximum de résultats
        
        Returns:
            Liste de dictionnaires contenant les offres
        """
        try:
            print(f"[TheMuse] Début scraping: keywords={keywords}, location={location}")
            
            offers = await self._scrape_from_api(
                keywords=keywords,
                location=location,
                company=company,
                max_results=max_results
            )
            
            # Filtrer par job_type et work_mode si nécessaire
            if job_type or work_mode:
                offers = self._filter_offers(offers, job_type, work_mode)
            
            print(f"[TheMuse] Scraping terminé. {len(offers)} offres récupérées.")
            return offers
        
        except Exception as e:
            print(f"[TheMuse] Erreur lors du scraping: {str(e)}")
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
        Scraper depuis l'API The Muse.
        
        Documentation: https://www.themuse.com/developers/api/v2
        """
        offers = []
        
        # Construire les paramètres de recherche
        params = {
            "page": 0,  # The Muse utilise page 0-indexed
            "descending": "true",  # Plus récents en premier
        }
        
        # Mots-clés - The Muse n'a pas de recherche full-text dans l'API publique
        # On filtre après récupération
        
        # Localisation
        if location:
            # The Muse supporte "Flexible / Remote" comme location
            if location.lower() in ["remote", "télétravail", "teletravail"]:
                params["location"] = "Flexible / Remote"
            else:
                params["location"] = location
        
        # Entreprise
        if company:
            params["company"] = company
        
        try:
            async with aiohttp.ClientSession() as session:
                # The Muse supporte la pagination (page=0, 1, 2...)
                page = 0
                max_pages = (max_results // self.max_results_per_page) + 1
                
                while page < max_pages and len(offers) < max_results:
                    params["page"] = page
                    
                    async with session.get(self.base_url, params=params, timeout=30) as response:
                        if response.status != 200:
                            print(f"[TheMuse] API error: status {response.status}")
                            break
                        
                        data = await response.json()
                        
                        # Vérifier les résultats
                        results = data.get("results", [])
                        if not results:
                            break  # Pas de résultats, arrêter la pagination
                        
                        # Parser les offres
                        for job in results:
                            try:
                                # Filtrer par keywords si fourni
                                if keywords:
                                    job_text = (
                                        job.get("name", "").lower() + " " +
                                        job.get("contents", "").lower() + " " +
                                        " ".join([cat.get("name", "") for cat in job.get("categories", [])]).lower()
                                    )
                                    if not any(kw.lower() in job_text for kw in keywords.split()):
                                        continue
                                
                                offer = self._parse_api_job(job)
                                if offer:
                                    offers.append(offer)
                                
                                # Limiter le nombre de résultats
                                if len(offers) >= max_results:
                                    break
                            
                            except Exception as e:
                                print(f"[TheMuse] Erreur parsing job: {str(e)}")
                                continue
                        
                        # Passer à la page suivante
                        page += 1
                        
                        # Pause pour être respectueux de l'API
                        await asyncio.sleep(0.5)
        
        except asyncio.TimeoutError:
            print("[TheMuse] Timeout lors de la requête API")
        except Exception as e:
            print(f"[TheMuse] Erreur API: {str(e)}")
        
        return offers
    
    def _parse_api_job(self, job: Dict) -> Optional[Dict]:
        """Parser un job depuis l'API"""
        try:
            # ID de l'offre
            job_id = job.get("id")
            if not job_id:
                return None
            
            # Titre
            title = job.get("name", "").strip()
            if not title:
                return None
            
            # Entreprise
            company_obj = job.get("company", {})
            company_name = company_obj.get("name", "Non spécifié").strip()
            
            # Description
            contents = job.get("contents", "")
            if contents:
                description = contents[:500]  # Limiter à 500 caractères
            else:
                description = ""
            
            # URL
            refs = job.get("refs", {})
            landing_page = refs.get("landing_page", "")
            if not landing_page:
                return None
            
            # Localisation
            locations = job.get("locations", [])
            if locations:
                location_display = locations[0].get("name", "Non spécifié")
            else:
                location_display = "Non spécifié"
            
            # Catégories
            categories = job.get("categories", [])
            category_names = [cat.get("name", "") for cat in categories]
            
            # Niveaux
            levels = job.get("levels", [])
            level_names = [lvl.get("name", "") for lvl in levels]
            
            # Date de publication
            publication_date = job.get("publication_date")
            posted_date = None
            if publication_date:
                try:
                    posted_date = datetime.fromisoformat(publication_date.replace("Z", "+00:00"))
                except:
                    pass
            
            # Type de contrat (The Muse n'a pas ce champ direct)
            job_type = self._detect_job_type(title, contents, level_names)
            
            # Mode de travail
            work_mode = self._detect_work_mode(location_display, contents)
            
            # Logo entreprise
            company_logo = company_obj.get("refs", {}).get("logo_image", None)
            
            offer = {
                "title": title,
                "company": company_name,
                "location": location_display,
                "description": description,
                "url": landing_page,
                "source_platform": "themuse",
                "job_type": job_type,
                "work_mode": work_mode,
                "posted_date": posted_date,
                "categories": category_names,
                "levels": level_names,
                "logo_url": company_logo,
                "scraped_at": datetime.utcnow()
            }
            
            return offer
        
        except Exception as e:
            print(f"[TheMuse] Erreur parsing API job: {str(e)}")
            return None
    
    def _detect_job_type(self, title: str, description: str, levels: List[str]) -> str:
        """Détecter le type de contrat"""
        text = f"{title} {description} {' '.join(levels)}".lower()
        
        if any(kw in text for kw in ["intern", "internship", "stage", "stagiaire"]):
            return "internship"
        elif any(kw in text for kw in ["contract", "freelance", "contractor", "consultant"]):
            return "contract"
        elif "entry level" in text or "junior" in text:
            return "fulltime"  # Junior positions sont généralement fulltime
        else:
            return "fulltime"  # Par défaut
    
    def _detect_work_mode(self, location: str, description: str) -> str:
        """Détecter le mode de travail"""
        text = f"{location} {description}".lower()
        
        if any(kw in text for kw in ["flexible / remote", "remote", "télétravail", "work from home"]):
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
