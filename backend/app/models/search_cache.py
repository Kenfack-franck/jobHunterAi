"""
Modèle de cache pour les résultats de recherche
"""
from sqlalchemy import Column, String, Integer, DateTime, func, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

from app.database import Base


class SearchResultsCache(Base):
    """Cache des résultats de recherche pour éviter rescraping"""
    __tablename__ = "search_results_cache"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Hash MD5 des paramètres de recherche pour unicité
    cache_key = Column(String(32), nullable=False, unique=True, index=True)
    
    # Paramètres de recherche (pour debug/audit)
    keywords = Column(String(500), nullable=False)
    location = Column(String(200), nullable=True)
    job_type = Column(String(50), nullable=True)
    work_mode = Column(String(50), nullable=True)
    company = Column(String(200), nullable=True)
    
    # Sources utilisées pour cette recherche
    sources_used = Column(JSONB, nullable=False)  # Liste des source_ids
    
    # Résultats (liste d'offres au format JSON)
    results = Column(JSONB, nullable=False)
    results_count = Column(Integer, nullable=False, default=0)
    
    # Statistiques
    scraped_count = Column(Integer, nullable=False, default=0)
    deduplicated_count = Column(Integer, nullable=False, default=0)
    execution_time_seconds = Column(Integer, nullable=False, default=0)
    
    # Métadonnées cache
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False, index=True)
    hit_count = Column(Integer, default=0, nullable=False)  # Nombre de fois réutilisé
    is_valid = Column(Boolean, default=True, nullable=False)
