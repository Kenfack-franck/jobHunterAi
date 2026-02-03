from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class UserSourcePreferences(Base):
    """Préférences utilisateur pour les sources de recherche d'offres"""
    __tablename__ = "user_source_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="SET NULL"), nullable=True)
    
    # Sources activées (liste des IDs de sources prédéfinies)
    enabled_sources = Column(ARRAY(String), nullable=False, default=list)
    
    # Sources prioritaires (3-5 sources scrapées en temps réel)
    priority_sources = Column(ARRAY(String), nullable=False, default=list)
    
    # Configuration cache
    use_cache = Column(Boolean, default=True, nullable=False)
    cache_ttl_hours = Column(Integer, default=24, nullable=False)
    
    # Configuration scraping
    max_priority_sources = Column(Integer, default=3, nullable=False)  # Limite pour temps réel
    background_scraping_enabled = Column(Boolean, default=True, nullable=False)
    
    # Métadonnées
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
