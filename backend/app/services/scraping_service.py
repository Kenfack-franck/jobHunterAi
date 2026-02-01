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
        limit: int = 100
    ) -> List[Dict]:
        """
        Scrape une plateforme spécifique
        
        Args:
            platform: Nom de la plateforme
            keywords: Mots-clés de recherche
            location: Localisation
            limit: Nombre max d'offres
            
        Returns:
            List[Dict]: Liste d'offres
        """
        if platform not in self.enabled_platforms:
            raise ValueError(f"Plateforme {platform} non supportée")
        
        # Obtenir le scraper approprié
        scraper = self._get_scraper(platform)
        
        try:
            # Appeler scrape() du scraper
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


# Instance globale
scraping_service = ScrapingService()
