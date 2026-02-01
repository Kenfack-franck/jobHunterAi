"""
Welcome to the Jungle Scraper - Scraper pour WTTJ
Difficulté : Faible (site permissif)
Rate limit : 200 req/h
Focus : France, startups
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


class WTTJScraper(BaseScraper):
    """Scraper pour Welcome to the Jungle"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.welcometothejungle.com"
        self.max_offers = 50
        self.rate_limit = 200  # req/h
        self.delay_between_requests = 3600 / self.rate_limit  # 18 secondes
    
    async def scrape(
        self,
        keywords: Optional[str] = None,
        location: Optional[str] = None,
        job_type: Optional[str] = None,
        work_mode: Optional[str] = None,
        company: Optional[str] = None,
        max_results: int = 50
    ) -> List[Dict]:
        """
        Scrape offres depuis Welcome to the Jungle.
        
        Args:
            keywords: Mots-clés de recherche (ex: "Python Developer")
            location: Localisation (ex: "Paris", "Lyon")
            job_type: Type de contrat (ex: "fulltime", "internship")
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
            
            print(f"[WTTJ] Scraping URL: {search_url}")
            
            # Accéder à la page de recherche
            page = await self.browser.new_page()
            await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
            await self.wait_random(2, 4)
            
            # Gérer la popup de cookies si présente
            try:
                cookie_button = await page.query_selector(
                    "button[id*='cookie'], button[class*='cookie'], button:has-text('Accept')"
                )
                if cookie_button:
                    await cookie_button.click()
                    await self.wait_random(1, 2)
            except:
                pass
            
            # Scraper les offres
            offers = []
            scroll_attempts = 0
            max_scrolls = 10
            
            print(f"[WTTJ] Début du scraping (scroll progressif)...")
            
            while len(offers) < min(max_results, self.max_offers) and scroll_attempts < max_scrolls:
                # Extraire les offres visibles
                page_offers = await self._extract_offers_from_page(page)
                
                # Ajouter seulement les nouvelles offres (éviter doublons)
                existing_urls = {o["url"] for o in offers}
                new_offers = [o for o in page_offers if o["url"] not in existing_urls]
                
                if new_offers:
                    offers.extend(new_offers)
                    print(f"[WTTJ] {len(new_offers)} nouvelles offres. Total: {len(offers)}")
                
                # Scroller pour charger plus d'offres (lazy loading)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await self.wait_random(2, 3)
                scroll_attempts += 1
                
                # Si aucune nouvelle offre après 2 scrolls, arrêter
                if not new_offers:
                    scroll_attempts += 1
                else:
                    scroll_attempts = 0  # Reset si nouvelles offres
            
            print(f"[WTTJ] Scraping terminé. {len(offers)} offres récupérées.")
            return offers[:max_results]
        
        except Exception as e:
            print(f"[WTTJ] Erreur lors du scraping: {str(e)}")
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
        """Construire l'URL de recherche WTTJ"""
        # URL de base pour les jobs en France
        url = f"{self.base_url}/fr/jobs?"
        
        params = []
        
        # Mots-clés (query)
        if keywords:
            params.append(f"query={keywords.replace(' ', '%20')}")
        
        # Entreprise (dans query)
        if company:
            if keywords:
                params.append(f"query={keywords.replace(' ', '%20')}%20{company.replace(' ', '%20')}")
            else:
                params.append(f"query={company.replace(' ', '%20')}")
        
        # Localisation (WTTJ utilise des slugs pour les villes)
        if location:
            # Simplification : mapper quelques villes courantes
            location_slug_map = {
                "paris": "paris",
                "lyon": "lyon",
                "marseille": "marseille",
                "toulouse": "toulouse",
                "nantes": "nantes",
                "bordeaux": "bordeaux",
                "lille": "lille",
                "nice": "nice",
                "france": "france"
            }
            loc_slug = location_slug_map.get(location.lower(), location.lower())
            params.append(f"refinementList[offices.city][]={loc_slug}")
        
        # Type de contrat
        if job_type:
            jt_map = {
                "fulltime": "FULL_TIME",
                "parttime": "PART_TIME",
                "internship": "INTERNSHIP",
                "stage": "INTERNSHIP",
                "alternance": "APPRENTICESHIP",
                "freelance": "FREELANCE"
            }
            jt = jt_map.get(job_type.lower())
            if jt:
                params.append(f"refinementList[contract_type][]={jt}")
        
        # Mode de travail (remote)
        if work_mode:
            if work_mode.lower() in ["remote", "télétravail"]:
                params.append("refinementList[remote][]=fulltime")
        
        # Tri par date (plus récent)
        params.append("sortBy=most-recent")
        
        if params:
            url += "&".join(params)
        
        return url
    
    async def _extract_offers_from_page(self, page: Page) -> List[Dict]:
        """Extraire les offres de la page courante"""
        offers = []
        
        try:
            # Attendre que les résultats soient chargés
            await page.wait_for_selector(
                "[data-testid='jobs-search-item'], .sc-job-card, li[role='listitem']",
                timeout=10000
            )
            
            # Sélectionner tous les conteneurs d'offres
            job_cards = await page.query_selector_all(
                "[data-testid='jobs-search-item'], .sc-job-card, li[role='listitem']"
            )
            
            for card in job_cards:
                try:
                    offer = await self._extract_offer_data(card, page)
                    if offer:
                        offers.append(offer)
                except Exception as e:
                    print(f"[WTTJ] Erreur extraction offre: {str(e)}")
                    continue
            
        except PlaywrightTimeout:
            print("[WTTJ] Timeout lors de l'attente des résultats")
        except Exception as e:
            print(f"[WTTJ] Erreur extraction page: {str(e)}")
        
        return offers
    
    async def _extract_offer_data(self, card, page: Page) -> Optional[Dict]:
        """Extraire les données d'une offre"""
        try:
            # URL de l'offre (prioritaire pour éviter doublons)
            link_elem = await card.query_selector("a[href*='/jobs/']")
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
            
            # Titre du poste
            title_elem = await card.query_selector(
                "[data-testid='job-title'], .job-card-title, h3, h4"
            )
            title = await title_elem.inner_text() if title_elem else None
            if not title:
                return None
            title = title.strip()
            
            # Entreprise
            company_elem = await card.query_selector(
                "[data-testid='job-company'], .company-name, [class*='CompanyName']"
            )
            company = await company_elem.inner_text() if company_elem else "Non spécifié"
            company = company.strip()
            
            # Localisation
            location_elem = await card.query_selector(
                "[data-testid='job-location'], .location, [class*='Location']"
            )
            location = await location_elem.inner_text() if location_elem else "Non spécifié"
            location = location.strip()
            
            # Description (snippet si disponible)
            description_elem = await card.query_selector(
                "[data-testid='job-description'], .description, p"
            )
            description = await description_elem.inner_text() if description_elem else ""
            description = description.strip()
            
            # Tags (contract type, remote, etc.)
            tags = []
            tag_elems = await card.query_selector_all(
                "[data-testid='job-tag'], .tag, [class*='Tag']"
            )
            for tag_elem in tag_elems:
                tag_text = await tag_elem.inner_text()
                tags.append(tag_text.strip().lower())
            
            # Déterminer work_mode
            work_mode = self._detect_work_mode(tags, location, description)
            
            # Déterminer job_type
            job_type = self._detect_job_type(tags, title, description)
            
            offer = {
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "url": offer_url,
                "source_platform": "wttj",
                "job_type": job_type,
                "work_mode": work_mode,
                "tags": tags,
                "scraped_at": datetime.utcnow()
            }
            
            return offer
        
        except Exception as e:
            print(f"[WTTJ] Erreur extraction données offre: {str(e)}")
            return None
    
    def _detect_work_mode(self, tags: List[str], location: str, description: str) -> str:
        """Détecter le mode de travail"""
        text = " ".join(tags + [location, description]).lower()
        
        if any(kw in text for kw in ["remote", "télétravail", "full remote", "100% remote"]):
            return "remote"
        elif any(kw in text for kw in ["hybrid", "hybride", "partiel"]):
            return "hybrid"
        else:
            return "onsite"
    
    def _detect_job_type(self, tags: List[str], title: str, description: str) -> str:
        """Détecter le type de contrat"""
        text = " ".join(tags + [title, description]).lower()
        
        if any(kw in text for kw in ["stage", "intern", "stagiaire", "internship"]):
            return "internship"
        elif any(kw in text for kw in ["alternance", "apprentice", "apprenticeship"]):
            return "alternance"
        elif any(kw in text for kw in ["cdi", "permanent", "full-time", "full_time", "fulltime"]):
            return "fulltime"
        elif any(kw in text for kw in ["cdd", "contract", "temporary", "part_time"]):
            return "contract"
        elif any(kw in text for kw in ["freelance", "consultant"]):
            return "freelance"
        else:
            return "fulltime"  # Par défaut
