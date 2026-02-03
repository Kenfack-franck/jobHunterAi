from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from urllib.parse import urlparse
import asyncio
from playwright.async_api import async_playwright, Browser, Page

from app.platforms_config.platforms import get_platform_config, get_enabled_platforms


class BaseScraper(ABC):
    """
    Interface commune pour tous les scrapers de plateformes
    """
    
    def __init__(self, platform_name: Optional[str] = None):
        self.platform_name = platform_name or self.get_platform_name()
        try:
            self.config = get_platform_config(self.platform_name)
        except:
            self.config = {}
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
    
    def get_platform_name(self) -> str:
        """Retourne le nom de la plateforme (à override si nécessaire)"""
        return self.__class__.__name__.replace("Scraper", "").lower()
    
    @abstractmethod
    async def scrape(self, url: str, limit: int = 100) -> List[Dict]:
        """
        Méthode abstraite à implémenter par chaque scraper
        
        Returns:
            List[Dict]: Liste d'offres avec structure:
                {
                    "title": str,
                    "company": str,
                    "location": str,
                    "description": str,
                    "url": str,
                    "job_type": str,
                    "work_mode": str,
                    "published_at": datetime,
                }
        """
        pass
    
    async def init_browser(self):
        """Initialise Playwright et le navigateur"""
        if not self.browser:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            self.page = await self.browser.new_page()
            
            # User-Agent aléatoire
            await self.page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
    
    async def close_browser(self):
        """Ferme le navigateur"""
        if self.browser:
            await self.browser.close()
            self.browser = None
            self.page = None
    
    async def wait_random(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """Attente aléatoire pour éviter détection bot"""
        import random
        await asyncio.sleep(random.uniform(min_seconds, max_seconds))


class ScrapingService:
    """
    Service principal de scraping multi-plateformes
    """
    
    def __init__(self):
        self.enabled_platforms = get_enabled_platforms()
    
    def detect_platform(self, url: str) -> Optional[str]:
        """
        Détecte la plateforme depuis une URL
        
        Args:
            url: URL à analyser
            
        Returns:
            str: Nom de la plateforme (indeed, wttj, etc.) ou None
        """
        parsed = urlparse(url.lower())
        domain = parsed.netloc.replace('www.', '')
        
        platform_mapping = {
            'indeed.com': 'indeed',
            'indeed.fr': 'indeed',
            'welcometothejungle.com': 'welcometothejungle',
            'remoteok.com': 'remoteok',
            'remoteok.io': 'remoteok',
            'jobteaser.com': 'jobteaser',
            'linkedin.com': 'linkedin',
        }
        
        return platform_mapping.get(domain)
    
    async def test_scraping(self, url: str) -> Dict:
        """
        Teste si le scraping d'une URL est possible
        
        Args:
            url: URL à tester
            
        Returns:
            Dict: {
                "success": bool,
                "platform": str,
                "offers_count": int,
                "error": Optional[str]
            }
        """
        platform = self.detect_platform(url)
        
        if not platform:
            return {
                "success": False,
                "platform": None,
                "offers_count": 0,
                "error": "Plateforme non reconnue"
            }
        
        if platform not in self.enabled_platforms:
            return {
                "success": False,
                "platform": platform,
                "offers_count": 0,
                "error": f"Plateforme {platform} non supportée ou désactivée"
            }
        
        # Test de scraping (limite 5 offres pour test)
        try:
            scraper = self._get_scraper(platform)
            offers = await scraper.scrape(url, limit=5)
            await scraper.close_browser()
            
            return {
                "success": True,
                "platform": platform,
                "offers_count": len(offers),
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "platform": platform,
                "offers_count": 0,
                "error": str(e)
            }
    
    def _get_scraper(self, platform: str) -> BaseScraper:
        """
        Retourne le scraper approprié pour une plateforme
        
        Args:
            platform: Nom de la plateforme
            
        Returns:
            BaseScraper: Instance du scraper
        """
        # Import des scrapers concrets
        from .scrapers.indeed_scraper import IndeedScraper
        from .scrapers.wttj_scraper import WTTJScraper
        from .scrapers.remoteok_scraper import RemoteOKScraper
        from .scrapers.adzuna_scraper import AdzunaScraper
        from .scrapers.themuse_scraper import TheMuseScraper
        from .scrapers.jsearch_scraper import JSearchScraper
        
        scrapers = {
            "indeed": IndeedScraper,
            "welcometothejungle": WTTJScraper,
            "remoteok": RemoteOKScraper,
            "adzuna": AdzunaScraper,
            "themuse": TheMuseScraper,
            "jsearch": JSearchScraper,
        }
        
        scraper_class = scrapers.get(platform)
        if not scraper_class:
            raise ValueError(f"Scraper non implémenté pour {platform}")
        
        return scraper_class()
    
    async def scrape_platform(
        self,
        platform: str,
        keywords: str,
        location: str = "",
        limit: int = 100,
        company: Optional[str] = None
    ) -> List[Dict]:
        """
        Scrape une plateforme spécifique
        
        Args:
            platform: Nom de la plateforme
            keywords: Mots-clés de recherche
            location: Localisation
            limit: Nombre max d'offres
            company: Nom de l'entreprise (pour filtre JSearch)
            
        Returns:
            List[Dict]: Liste d'offres
        """
        if platform not in self.enabled_platforms:
            raise ValueError(f"Plateforme {platform} non supportée")
        
        # Obtenir le scraper approprié
        scraper = self._get_scraper(platform)
        
        try:
            # Pour JSearch et Adzuna, passer le paramètre company si fourni
            if platform in ["jsearch", "adzuna"] and company:
                print(f"[ScrapingService] 🏢 {platform.upper()} avec filtre company='{company}'")
                offers = await scraper.scrape(
                    keywords=keywords,
                    location=location if location else None,
                    company=company,
                    max_results=limit
                )
            else:
                # Appeler scrape() du scraper normalement
                offers = await scraper.scrape(
                    keywords=keywords,
                    location=location if location else None,
                    max_results=limit
                )
            return offers
        except Exception as e:
            print(f"❌ Erreur scraping {platform}: {e}")
            return []
    
    async def scrape_all_platforms(
        self,
        keywords: str,
        location: str = "",
        limit_per_platform: int = 100
    ) -> Dict[str, List[Dict]]:
        """
        Scrape toutes les plateformes activées en parallèle
        
        Args:
            keywords: Mots-clés de recherche
            location: Localisation
            limit_per_platform: Limite par plateforme
            
        Returns:
            Dict[str, List[Dict]]: {platform_name: [offers]}
        """
        results = {}
        
        # Scraping parallèle
        tasks = []
        for platform_name in self.enabled_platforms.keys():
            task = self.scrape_platform(
                platform_name,
                keywords,
                location,
                limit_per_platform
            )
            tasks.append((platform_name, task))
        
        # Attendre tous les scrapings
        for platform_name, task in tasks:
            try:
                offers = await task
                results[platform_name] = offers
            except Exception as e:
                print(f"❌ Erreur scraping {platform_name}: {e}")
                results[platform_name] = []
        
        total_offers = sum(len(offers) for offers in results.values())
        print(f"\n✅ Total: {total_offers} offres trouvées sur {len(results)} plateformes")
        
        return results
    
    async def scrape_priority_sources(
        self,
        priority_sources: List[str],
        keywords: str,
        location: str = "",
        limit_per_source: int = 100
    ) -> Dict[str, List[Dict]]:
        """
        Scrape uniquement les sources prioritaires de l'utilisateur
        
        Args:
            priority_sources: Liste des source_ids (ex: ["remoteok", "wttj", "airbus"])
            keywords: Mots-clés de recherche
            location: Localisation
            limit_per_source: Limite par source
            
        Returns:
            Dict[str, List[Dict]]: {source_id: [offers]}
        """
        results = {}
        
        print(f"[ScrapingService] Scraping {len(priority_sources)} sources prioritaires...")
        
        # Scraping parallèle des sources prioritaires uniquement
        tasks = []
        for source_id in priority_sources:
            # Mapper source_id → platform_name
            platform = self._map_source_to_platform(source_id)
            if platform:
                # Extraire le nom de l'entreprise depuis le source_id si c'est JSearch ou Adzuna
                company_name = self._get_company_name(source_id) if platform in ["jsearch", "adzuna"] else None
                
                task = self.scrape_platform(
                    platform,
                    keywords,
                    location,
                    limit_per_source,
                    company=company_name  # Passer le nom de l'entreprise
                )
                tasks.append((source_id, task))
            else:
                print(f"⚠️ Source {source_id} non mappée à une plateforme")
        
        # Attendre tous les scrapings
        for source_id, task in tasks:
            try:
                offers = await task
                results[source_id] = offers
                print(f"✅ {source_id}: {len(offers)} offres")
            except Exception as e:
                print(f"❌ Erreur scraping {source_id}: {e}")
                results[source_id] = []
        
        total_offers = sum(len(offers) for offers in results.values())
        print(f"\n✅ Total prioritaires: {total_offers} offres sur {len(results)} sources")
        
        return results
    
    def _get_company_name(self, source_id: str) -> Optional[str]:
        """
        Extraire le nom de l'entreprise depuis le source_id pour le filtre JSearch
        
        Args:
            source_id: ID de la source (ex: "capgemini", "loreal")
            
        Returns:
            Nom de l'entreprise pour la recherche (ex: "Capgemini", "L'Oréal")
        """
        company_mapping = {
            # Tech
            "capgemini": "Capgemini",
            "sopra_steria": "Sopra Steria",
            "dassault_systemes": "Dassault Systemes",
            
            # Aérospatial
            "airbus": "Airbus",
            "thales": "Thales",
            "dassault_aviation": "Dassault Aviation",
            "safran": "Safran",
            
            # Énergie
            "totalenergies": "TotalEnergies",
            "edf": "EDF",
            
            # Automobile
            "renault": "Renault",
            "stellantis": "Stellantis",
            
            # Luxe
            "lvmh": "LVMH",
            "loreal": "L'Oréal",
            
            # Banque
            "bnp_paribas": "BNP Paribas",
            "societe_generale": "Société Générale",
            
            # Telecom
            "orange": "Orange",
        }
        
        return company_mapping.get(source_id)
    
    def _map_source_to_platform(self, source_id: str) -> Optional[str]:
        """
        Mapper un source_id (predefined_sources.py) → platform_name (scraper existant)
        
        Args:
            source_id: ID de la source prédéfinie (ex: "remoteok", "wttj", "airbus")
            
        Returns:
            Nom de la plateforme pour le scraper ou None si non supporté
        """
        # Mapping des sources prédéfinies vers les scrapers existants
        mapping = {
            # Agrégateurs (scrapers existants)
            "remoteok": "remoteok",           # ✅ Scraping direct RemoteOK
            "wttj": "welcometothejungle",     # À implémenter
            "linkedin": "adzuna",             # Via Adzuna (agrégateur)
            
            # Entreprises Tech (via Adzuna - filtre company)
            "capgemini": "adzuna",            # Adzuna(company="Capgemini")
            "sopra_steria": "adzuna",         # Adzuna(company="Sopra Steria")
            "dassault_systemes": "adzuna",    # Adzuna(company="Dassault Systemes")
            
            # Aérospatial (via Adzuna)
            "airbus": "adzuna",               # Adzuna(company="Airbus")
            "thales": "adzuna",               # Adzuna(company="Thales")
            "dassault_aviation": "adzuna",    # Adzuna(company="Dassault Aviation")
            "safran": "adzuna",               # Adzuna(company="Safran")
            
            # Énergie (via Adzuna)
            "totalenergies": "adzuna",        # Adzuna(company="TotalEnergies")
            "edf": "adzuna",                  # Adzuna(company="EDF")
            
            # Automobile (via Adzuna)
            "renault": "adzuna",              # Adzuna(company="Renault")
            "stellantis": "adzuna",           # Adzuna(company="Stellantis")
            
            # Luxe (via Adzuna)
            "lvmh": "adzuna",                 # Adzuna(company="LVMH")
            "loreal": "adzuna",               # Adzuna(company="L'Oréal")
            
            # Banque (via Adzuna)
            "bnp_paribas": "adzuna",          # Adzuna(company="BNP Paribas")
            "societe_generale": "adzuna",     # Adzuna(company="Société Générale")
            
            # Telecom (via Adzuna)
            "orange": "adzuna",               # Adzuna(company="Orange")
        }
        
        return mapping.get(source_id)


# Instance globale
scraping_service = ScrapingService()
