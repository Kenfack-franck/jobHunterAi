"""
RemoteOK Scraper - Scraper pour RemoteOK
Difficulté : Très faible (API publique + site simple)
Rate limit : 500 req/h
Focus : 100% Remote jobs
"""
import asyncio
import re
from typing import List, Dict, Optional
from datetime import datetime
from playwright.async_api import Page, TimeoutError as PlaywrightTimeout
import json

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.scraping_service import BaseScraper


class RemoteOKScraper(BaseScraper):
    """Scraper pour RemoteOK"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://remoteok.com"
        self.api_url = "https://remoteok.com/api"
        self.max_offers = 100
        self.rate_limit = 500  # req/h
        self.delay_between_requests = 3600 / self.rate_limit  # 7.2 secondes
    
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
        Scrape offres depuis RemoteOK.
        
        Note: RemoteOK a une API publique, on privilégie l'API plutôt que le scraping HTML.
        
        Args:
            keywords: Mots-clés de recherche (ex: "Python", "Developer")
            location: Localisation (ignoré car 100% remote)
            job_type: Type de contrat (non supporté par RemoteOK)
            work_mode: Mode de travail (toujours "remote")
            company: Nom de l'entreprise
            max_results: Nombre maximum de résultats
        
        Returns:
            Liste de dictionnaires contenant les offres
        """
        try:
            # Essayer d'abord l'API (plus rapide et fiable)
            try:
                offers = await self._scrape_from_api(
                    keywords=keywords,
                    company=company,
                    max_results=max_results
                )
                if offers:
                    print(f"[RemoteOK] API: {len(offers)} offres récupérées.")
                    return offers
            except Exception as e:
                print(f"[RemoteOK] Erreur API, fallback vers scraping HTML: {str(e)}")
            
            # Fallback: scraping HTML si API échoue
            await self.init_browser()
            
            # Construire l'URL de recherche
            search_url = self._build_search_url(
                keywords=keywords,
                company=company
            )
            
            print(f"[RemoteOK] Scraping URL: {search_url}")
            
            # Accéder à la page de recherche
            page = await self.browser.new_page()
            await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
            await self.wait_random(2, 4)
            
            # Scraper les offres
            offers = await self._extract_offers_from_page(page, max_results)
            
            print(f"[RemoteOK] Scraping terminé. {len(offers)} offres récupérées.")
            return offers
        
        except Exception as e:
            print(f"[RemoteOK] Erreur lors du scraping: {str(e)}")
            raise
        finally:
            await self.close_browser()
    
    async def _scrape_from_api(
        self,
        keywords: Optional[str],
        company: Optional[str],
        max_results: int
    ) -> List[Dict]:
        """
        Scraper depuis l'API RemoteOK.
        
        L'API retourne un JSON avec toutes les offres actives.
        """
        import aiohttp
        
        offers = []
        
        async with aiohttp.ClientSession() as session:
            # L'API RemoteOK retourne toutes les offres en un seul call
            async with session.get(self.api_url, timeout=30) as response:
                if response.status != 200:
                    raise Exception(f"API error: status {response.status}")
                
                data = await response.json()
                
                # Le premier élément est des métadonnées, on le skip
                if data and isinstance(data, list) and len(data) > 1:
                    jobs = data[1:]  # Skip first element (metadata)
                    
                    for job in jobs:
                        try:
                            # Filtrer par mots-clés si fournis
                            if keywords:
                                job_text = (
                                    job.get("position", "").lower() + " " +
                                    job.get("description", "").lower() + " " +
                                    " ".join(job.get("tags", [])).lower()
                                )
                                if not any(kw.lower() in job_text for kw in keywords.split()):
                                    continue
                            
                            # Filtrer par entreprise si fourni
                            if company:
                                job_company = job.get("company", "").lower()
                                if company.lower() not in job_company:
                                    continue
                            
                            # Extraire les données
                            offer = self._parse_api_job(job)
                            if offer:
                                offers.append(offer)
                            
                            # Limiter le nombre de résultats
                            if len(offers) >= max_results:
                                break
                        
                        except Exception as e:
                            print(f"[RemoteOK] Erreur parsing job API: {str(e)}")
                            continue
        
        return offers
    
    def _parse_api_job(self, job: Dict) -> Optional[Dict]:
        """Parser un job depuis l'API"""
        try:
            # ID de l'offre
            job_id = job.get("id")
            if not job_id:
                return None
            
            # Titre
            title = job.get("position", "").strip()
            if not title:
                return None
            
            # Entreprise
            company = job.get("company", "Non spécifié").strip()
            
            # Description
            description = job.get("description", "").strip()
            
            # URL
            slug = job.get("slug", "")
            url = f"{self.base_url}/remote-jobs/{slug}" if slug else f"{self.base_url}/remote-jobs/{job_id}"
            
            # Localisation (souvent vide car remote)
            location = job.get("location", "Remote").strip() or "Remote"
            
            # Tags
            tags = job.get("tags", [])
            
            # Salaire
            salary = None
            salary_min = job.get("salary_min")
            salary_max = job.get("salary_max")
            if salary_min and salary_max:
                salary = f"${salary_min} - ${salary_max}"
            
            # Date de publication
            posted_date = job.get("date")
            
            # Logo
            logo_url = job.get("logo")
            
            # Déterminer job_type depuis tags
            job_type = self._detect_job_type_from_tags(tags, title, description)
            
            offer = {
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "url": url,
                "source_platform": "remoteok",
                "job_type": job_type,
                "work_mode": "remote",  # Toujours remote sur RemoteOK
                "salary": salary,
                "posted_date": posted_date,
                "tags": tags,
                "logo_url": logo_url,
                "scraped_at": datetime.utcnow()
            }
            
            return offer
        
        except Exception as e:
            print(f"[RemoteOK] Erreur parsing API job: {str(e)}")
            return None
    
    def _build_search_url(
        self,
        keywords: Optional[str],
        company: Optional[str]
    ) -> str:
        """Construire l'URL de recherche RemoteOK"""
        # RemoteOK utilise des tags pour la recherche
        if keywords:
            # Prendre le premier mot-clé comme tag
            tag = keywords.split()[0].lower().replace(" ", "-")
            url = f"{self.base_url}/remote-{tag}-jobs"
        else:
            url = f"{self.base_url}/remote-jobs"
        
        # RemoteOK n'a pas de filtre entreprise dans l'URL
        # On filtrera côté extraction
        
        return url
    
    async def _extract_offers_from_page(self, page: Page, max_results: int) -> List[Dict]:
        """Extraire les offres de la page HTML (fallback)"""
        offers = []
        
        try:
            # Attendre que les résultats soient chargés
            await page.wait_for_selector(
                "tr.job, [itemtype='http://schema.org/JobPosting']",
                timeout=10000
            )
            
            # Sélectionner tous les conteneurs d'offres
            job_rows = await page.query_selector_all(
                "tr.job, [itemtype='http://schema.org/JobPosting']"
            )
            
            for row in job_rows:
                try:
                    offer = await self._extract_offer_data(row, page)
                    if offer:
                        offers.append(offer)
                    
                    if len(offers) >= max_results:
                        break
                
                except Exception as e:
                    print(f"[RemoteOK] Erreur extraction offre: {str(e)}")
                    continue
            
        except PlaywrightTimeout:
            print("[RemoteOK] Timeout lors de l'attente des résultats")
        except Exception as e:
            print(f"[RemoteOK] Erreur extraction page: {str(e)}")
        
        return offers
    
    async def _extract_offer_data(self, row, page: Page) -> Optional[Dict]:
        """Extraire les données d'une offre depuis HTML"""
        try:
            # Titre
            title_elem = await row.query_selector(
                "h2[itemprop='title'], .company_and_position h2"
            )
            title = await title_elem.inner_text() if title_elem else None
            if not title:
                return None
            title = title.strip()
            
            # URL
            link_elem = await row.query_selector("a.preventLink, a[href*='/remote-jobs/']")
            offer_url = None
            if link_elem:
                href = await link_elem.get_attribute("href")
                if href:
                    if href.startswith("/"):
                        offer_url = f"{self.base_url}{href}"
                    else:
                        offer_url = href
            
            if not offer_url:
                return None
            
            # Entreprise
            company_elem = await row.query_selector(
                "h3[itemprop='name'], .company h3"
            )
            company = await company_elem.inner_text() if company_elem else "Non spécifié"
            company = company.strip()
            
            # Localisation (souvent "Remote" ou vide)
            location_elem = await row.query_selector(".location, [itemprop='jobLocation']")
            location = await location_elem.inner_text() if location_elem else "Remote"
            location = location.strip() or "Remote"
            
            # Tags
            tags = []
            tag_elems = await row.query_selector_all(".tag, .tags a")
            for tag_elem in tag_elems:
                tag_text = await tag_elem.inner_text()
                tags.append(tag_text.strip().lower())
            
            # Salaire (si présent)
            salary_elem = await row.query_selector(".salary, [itemprop='baseSalary']")
            salary = await salary_elem.inner_text() if salary_elem else None
            
            # Description courte (si disponible)
            description = " ".join(tags)  # Tags comme description basique
            
            # Déterminer job_type
            job_type = self._detect_job_type_from_tags(tags, title, description)
            
            offer = {
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "url": offer_url,
                "source_platform": "remoteok",
                "job_type": job_type,
                "work_mode": "remote",
                "salary": salary,
                "tags": tags,
                "scraped_at": datetime.utcnow()
            }
            
            return offer
        
        except Exception as e:
            print(f"[RemoteOK] Erreur extraction données offre: {str(e)}")
            return None
    
    def _detect_job_type_from_tags(self, tags: List[str], title: str, description: str) -> str:
        """Détecter le type de contrat depuis les tags"""
        text = " ".join(tags + [title, description]).lower()
        
        if any(kw in text for kw in ["intern", "internship", "stage"]):
            return "internship"
        elif any(kw in text for kw in ["contract", "contractor"]):
            return "contract"
        elif any(kw in text for kw in ["freelance", "consultant"]):
            return "freelance"
        else:
            return "fulltime"  # Par défaut
