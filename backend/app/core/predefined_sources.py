"""
Configuration des 18 sources prédéfinies accessibles
"""
from enum import Enum
from typing import List, Dict

class SourceType(str, Enum):
    AGGREGATOR = "aggregator"
    TECH = "tech"
    AEROSPACE = "aerospace"
    ENERGY = "energy"
    AUTO = "auto"
    LUXURY = "luxury"
    BANKING = "banking"
    TELECOM = "telecom"

class PredefinedSource:
    def __init__(
        self,
        id: str,
        name: str,
        url: str,
        source_type: SourceType,
        logo_url: str = None,
        scraper_type: str = "generic",
        priority: int = 1,
        enabled_by_default: bool = True
    ):
        self.id = id
        self.name = name
        self.url = url
        self.source_type = source_type
        self.logo_url = logo_url
        self.scraper_type = scraper_type
        self.priority = priority
        self.enabled_by_default = enabled_by_default

# 18 sources accessibles validées par le test
PREDEFINED_SOURCES = [
    # ==================== AGRÉGATEURS (3/4) ====================
    PredefinedSource(
        id="remoteok",
        name="RemoteOK",
        url="https://remoteok.com/remote-jobs",
        source_type=SourceType.AGGREGATOR,
        scraper_type="remoteok_api",
        priority=1,
        enabled_by_default=True
    ),
    PredefinedSource(
        id="wttj",
        name="Welcome to the Jungle",
        url="https://www.welcometothejungle.com/fr/jobs",
        source_type=SourceType.AGGREGATOR,
        scraper_type="wttj_html",
        priority=1,
        enabled_by_default=True
    ),
    PredefinedSource(
        id="linkedin",
        name="LinkedIn Jobs",
        url="https://www.linkedin.com/jobs/",
        source_type=SourceType.AGGREGATOR,
        scraper_type="linkedin_html",
        priority=1,
        enabled_by_default=True
    ),
    
    # ==================== TECH (3/4) ====================
    PredefinedSource(
        id="capgemini",
        name="Capgemini",
        url="https://www.capgemini.com/fr-fr/carrieres/",
        source_type=SourceType.TECH,
        scraper_type="generic_html",
        priority=2
    ),
    PredefinedSource(
        id="sopra_steria",
        name="Sopra Steria",
        url="https://www.soprasteria.com/fr/carrieres",
        source_type=SourceType.TECH,
        scraper_type="generic_html",
        priority=2
    ),
    PredefinedSource(
        id="dassault_systemes",
        name="Dassault Systèmes",
        url="https://careers.3ds.com/",
        source_type=SourceType.TECH,
        scraper_type="generic_html",
        priority=2
    ),
    
    # ==================== AÉROSPATIAL (3/4) ====================
    PredefinedSource(
        id="airbus",
        name="Airbus",
        url="https://www.airbus.com/en/careers",
        source_type=SourceType.AEROSPACE,
        scraper_type="generic_html",
        priority=2
    ),
    PredefinedSource(
        id="thales",
        name="Thales",
        url="https://www.thalesgroup.com/fr/carrieres",
        source_type=SourceType.AEROSPACE,
        scraper_type="generic_html",
        priority=2
    ),
    PredefinedSource(
        id="dassault_aviation",
        name="Dassault Aviation",
        url="https://www.dassault-aviation.com/fr/groupe/carrieres/",
        source_type=SourceType.AEROSPACE,
        scraper_type="generic_html",
        priority=2
    ),
    
    # ==================== ÉNERGIE (2/4) ====================
    PredefinedSource(
        id="totalenergies",
        name="TotalEnergies",
        url="https://www.totalenergies.com/fr/carrieres",
        source_type=SourceType.ENERGY,
        scraper_type="generic_html",
        priority=2
    ),
    PredefinedSource(
        id="edf",
        name="EDF",
        url="https://www.edf.fr/edf-recrute",
        source_type=SourceType.ENERGY,
        scraper_type="generic_html",
        priority=2
    ),
    
    # ==================== AUTOMOBILE (2/3) ====================
    PredefinedSource(
        id="renault",
        name="Renault Group",
        url="https://www.renaultgroup.com/talents/",
        source_type=SourceType.AUTO,
        scraper_type="generic_html",
        priority=2
    ),
    PredefinedSource(
        id="stellantis",
        name="Stellantis",
        url="https://www.stellantis.com/fr/carrieres",
        source_type=SourceType.AUTO,
        scraper_type="generic_html",
        priority=2
    ),
    
    # ==================== LUXE (2/4) ====================
    PredefinedSource(
        id="lvmh",
        name="LVMH",
        url="https://www.lvmh.fr/talents/",
        source_type=SourceType.LUXURY,
        scraper_type="generic_html",
        priority=3
    ),
    PredefinedSource(
        id="loreal",
        name="L'Oréal",
        url="https://www.loreal.com/fr/careers/",
        source_type=SourceType.LUXURY,
        scraper_type="generic_html",
        priority=3
    ),
    
    # ==================== BANQUE (2/3) ====================
    PredefinedSource(
        id="bnp_paribas",
        name="BNP Paribas",
        url="https://group.bnpparibas/emploi-carriere",
        source_type=SourceType.BANKING,
        scraper_type="generic_html",
        priority=3
    ),
    PredefinedSource(
        id="societe_generale",
        name="Société Générale",
        url="https://careers.societegenerale.com/",
        source_type=SourceType.BANKING,
        scraper_type="generic_html",
        priority=3
    ),
    
    # ==================== TELECOM (1/2) ====================
    PredefinedSource(
        id="orange",
        name="Orange",
        url="https://careers.orange.com/",
        source_type=SourceType.TELECOM,
        scraper_type="generic_html",
        priority=3
    ),
]

def get_sources_by_type(source_type: SourceType) -> List[PredefinedSource]:
    """Récupère les sources par type"""
    return [s for s in PREDEFINED_SOURCES if s.source_type == source_type]

def get_source_by_id(source_id: str) -> PredefinedSource:
    """Récupère une source par son ID"""
    for source in PREDEFINED_SOURCES:
        if source.id == source_id:
            return source
    return None

def get_default_enabled_sources() -> List[str]:
    """Récupère les IDs des sources activées par défaut"""
    return [s.id for s in PREDEFINED_SOURCES if s.enabled_by_default]

def get_sources_by_priority(priority: int) -> List[PredefinedSource]:
    """Récupère les sources par priorité"""
    return [s for s in PREDEFINED_SOURCES if s.priority == priority]

def get_aggregators() -> List[PredefinedSource]:
    """Récupère uniquement les agrégateurs"""
    return get_sources_by_type(SourceType.AGGREGATOR)

def get_all_source_ids() -> List[str]:
    """Récupère tous les IDs de sources"""
    return [s.id for s in PREDEFINED_SOURCES]
