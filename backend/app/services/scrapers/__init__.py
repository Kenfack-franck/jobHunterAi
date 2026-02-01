"""
Scrapers pour différentes plateformes d'emploi.
"""
from .indeed_scraper import IndeedScraper
from .wttj_scraper import WTTJScraper
from .remoteok_scraper import RemoteOKScraper

__all__ = [
    "IndeedScraper",
    "WTTJScraper",
    "RemoteOKScraper",
]
