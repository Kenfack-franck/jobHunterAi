"""
Indeed Scraper - Scraper pour Indeed.com/fr
Difficulté : Moyenne (anti-bot modéré)
Rate limit : 100 req/h
"""
import asyncio
import re
from typing import List, Dict, Optional
from datetime import datetime
from playwright.async_api import Page, TimeoutError as PlaywrightTimeout

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.scraping_service import BaseScraper


class IndeedScraper(BaseScraper):
    """Scraper pour Indeed"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://fr.indeed.com"
        self.max_offers = 100
        self.rate_limit = 100  # req/h
        self.delay_between_requests = 3600 / self.rate_limit  # 36 secondes
    
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
        Scrape offres depuis Indeed.
        
        Args:
            keywords: Mots-clés de recherche (ex: "Python Developer")
            location: Localisation (ex: "Paris", "Remote")
            job_type: Type de contrat (ex: "fulltime", "contract", "internship")
            work_mode: Mode de travail (ex: "remote", "hybrid", "onsite")
            company: Nom de l'entreprise
            max_results: Nombre maximum de résultats
        
        Returns:
            Liste de dictionnaires contenant les offres
        """
        try:
            await self.init_browser()
            
            # Construire l'URL de recherche
            search_url = self._build_search_url(
                keywords=keywords,
                location=location,
                job_type=job_type,
                work_mode=work_mode,
                company=company
            )
            
            print(f"[Indeed] Scraping URL: {search_url}")
            
            # Accéder à la page de recherche
            page = await self.browser.new_page()
            await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
            await self.wait_random(2, 4)
            
            # Scraper les offres
            offers = []
            page_num = 0
            
            while len(offers) < min(max_results, self.max_offers):
                print(f"[Indeed] Scraping page {page_num + 1}...")
                
                # Extraire les offres de la page courante
                page_offers = await self._extract_offers_from_page(page)
                
                if not page_offers:
                    print(f"[Indeed] Aucune offre trouvée sur la page {page_num + 1}, arrêt.")
                    break
                
                offers.extend(page_offers)
                print(f"[Indeed] {len(page_offers)} offres trouvées. Total: {len(offers)}")
                
                # Vérifier s'il y a une page suivante
                has_next = await self._has_next_page(page)
                if not has_next or len(offers) >= min(max_results, self.max_offers):
                    break
                
                # Aller à la page suivante
                await self._go_to_next_page(page, page_num)
                page_num += 1
                await self.wait_random(3, 5)
            
            print(f"[Indeed] Scraping terminé. {len(offers)} offres récupérées.")
            return offers[:max_results]
        
        except Exception as e:
            print(f"[Indeed] Erreur lors du scraping: {str(e)}")
            raise
        finally:
            await self.close_browser()
    
    def _build_search_url(
        self,
        keywords: Optional[str],
        location: Optional[str],
        job_type: Optional[str],
        work_mode: Optional[str],
        company: Optional[str]
    ) -> str:
        """Construire l'URL de recherche Indeed"""
        url = f"{self.base_url}/jobs?"
        
        # Mots-clés
        if keywords:
            url += f"q={keywords.replace(' ', '+')}"
        
        # Entreprise
        if company:
            if keywords:
                url += f"+{company.replace(' ', '+')}"
            else:
                url += f"q={company.replace(' ', '+')}"
        
        # Localisation
        if location:
            url += f"&l={location.replace(' ', '+')}"
        
        # Type de contrat (Indeed utilise 'jt')
        if job_type:
            jt_map = {
                "fulltime": "fulltime",
                "parttime": "parttime",
                "contract": "contract",
                "temporary": "temporary",
                "internship": "internship",
                "stage": "internship",
                "alternance": "internship"
            }
            jt = jt_map.get(job_type.lower(), job_type)
            url += f"&jt={jt}"
        
        # Mode de travail (remote)
        if work_mode and work_mode.lower() in ["remote", "télétravail"]:
            url += "&remotejob=1"
        
        # Tri par date (plus récent d'abord)
        url += "&sort=date"
        
        return url
    
    async def _extract_offers_from_page(self, page: Page) -> List[Dict]:
        """Extraire les offres de la page courante"""
        offers = []
        
        try:
            # Attendre que les résultats soient chargés
            await page.wait_for_selector(".job_seen_beacon, .jobsearch-ResultsList", timeout=10000)
            
            # Sélectionner tous les conteneurs d'offres
            # Indeed utilise plusieurs formats selon les régions
            job_cards = await page.query_selector_all(
                ".job_seen_beacon, .jobsearch-SerpJobCard, .slider_item, .result"
            )
            
            for card in job_cards:
                try:
                    offer = await self._extract_offer_data(card, page)
                    if offer:
                        offers.append(offer)
                except Exception as e:
                    print(f"[Indeed] Erreur extraction offre: {str(e)}")
                    continue
            
        except PlaywrightTimeout:
            print("[Indeed] Timeout lors de l'attente des résultats")
        except Exception as e:
            print(f"[Indeed] Erreur extraction page: {str(e)}")
        
        return offers
    
    async def _extract_offer_data(self, card, page: Page) -> Optional[Dict]:
        """Extraire les données d'une offre"""
        try:
            # Titre du poste
            title_elem = await card.query_selector("h2.jobTitle, .jobTitle span")
            title = await title_elem.inner_text() if title_elem else None
            if not title:
                return None
            title = title.strip()
            
            # URL de l'offre
            link_elem = await card.query_selector("a[data-jk], h2.jobTitle a")
            offer_url = None
            if link_elem:
                href = await link_elem.get_attribute("href")
                if href:
                    if href.startswith("/"):
                        offer_url = f"{self.base_url}{href}"
                    else:
                        offer_url = href
            
            # Entreprise
            company_elem = await card.query_selector(
                "[data-testid='company-name'], .companyName, .company"
            )
            company = await company_elem.inner_text() if company_elem else "Non spécifié"
            company = company.strip()
            
            # Localisation
            location_elem = await card.query_selector(
                "[data-testid='text-location'], .companyLocation, .location"
            )
            location = await location_elem.inner_text() if location_elem else "Non spécifié"
            location = location.strip()
            
            # Description (snippet)
            description_elem = await card.query_selector(
                ".jobCardShelfContainer, .job-snippet, .summary"
            )
            description = await description_elem.inner_text() if description_elem else ""
            description = description.strip()
            
            # Salaire (optionnel)
            salary_elem = await card.query_selector(
                "[data-testid='attribute_snippet_testid'], .salary-snippet"
            )
            salary = await salary_elem.inner_text() if salary_elem else None
            
            # Date de publication (si disponible)
            date_elem = await card.query_selector(".date")
            posted_date = await date_elem.inner_text() if date_elem else None
            
            # Déterminer work_mode depuis description ou tags
            work_mode = self._detect_work_mode(description, location)
            
            # Déterminer job_type depuis tags
            job_type = self._detect_job_type(title, description)
            
            offer = {
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "url": offer_url or "URL non disponible",
                "source_platform": "indeed",
                "job_type": job_type,
                "work_mode": work_mode,
                "salary": salary,
                "posted_date": posted_date,
                "scraped_at": datetime.utcnow()
            }
            
            return offer
        
        except Exception as e:
            print(f"[Indeed] Erreur extraction données offre: {str(e)}")
            return None
    
    def _detect_work_mode(self, description: str, location: str) -> str:
        """Détecter le mode de travail depuis la description"""
        text = (description + " " + location).lower()
        
        if any(kw in text for kw in ["remote", "télétravail", "100% remote", "full remote"]):
            return "remote"
        elif any(kw in text for kw in ["hybrid", "hybride", "flex"]):
            return "hybrid"
        else:
            return "onsite"
    
    def _detect_job_type(self, title: str, description: str) -> str:
        """Détecter le type de contrat depuis le titre/description"""
        text = (title + " " + description).lower()
        
        if any(kw in text for kw in ["stage", "intern", "stagiaire"]):
            return "internship"
        elif any(kw in text for kw in ["alternance", "apprentice"]):
            return "alternance"
        elif any(kw in text for kw in ["cdi", "permanent", "full-time", "fulltime"]):
            return "fulltime"
        elif any(kw in text for kw in ["cdd", "contract", "temporary"]):
            return "contract"
        elif any(kw in text for kw in ["freelance", "consultant"]):
            return "freelance"
        else:
            return "fulltime"  # Par défaut
    
    async def _has_next_page(self, page: Page) -> bool:
        """Vérifier s'il y a une page suivante"""
        try:
            # Chercher le bouton "Suivant" ou la pagination
            next_button = await page.query_selector(
                "a[data-testid='pagination-page-next'], a[aria-label*='Suivant'], .pagination a[aria-label='Next']"
            )
            return next_button is not None
        except:
            return False
    
    async def _go_to_next_page(self, page: Page, current_page: int):
        """Aller à la page suivante"""
        try:
            # Cliquer sur "Suivant"
            next_button = await page.query_selector(
                "a[data-testid='pagination-page-next'], a[aria-label*='Suivant'], .pagination a[aria-label='Next']"
            )
            if next_button:
                await next_button.click()
                await page.wait_for_load_state("domcontentloaded")
            else:
                # Fallback: construire l'URL avec &start=
                current_url = page.url
                start = (current_page + 1) * 10
                if "start=" in current_url:
                    new_url = re.sub(r"start=\d+", f"start={start}", current_url)
                else:
                    new_url = f"{current_url}&start={start}"
                await page.goto(new_url, wait_until="domcontentloaded")
        except Exception as e:
            print(f"[Indeed] Erreur navigation page suivante: {str(e)}")
            raise
