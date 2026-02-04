"""
Modèle UserLimits - Suivi des limites d'utilisation par utilisateur
"""
from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from datetime import date

from app.database import Base


# Default limits for free plan
DEFAULT_LIMITS = {
    'max_saved_offers': 50,
    'max_searches_per_day': 50,
    'max_profiles': 3,
    'max_applications': 30,
    'max_cv_parses': 5,
    'max_watched_companies': 5,
    'max_generated_cv_per_day': 4
}


class UserLimits(Base):
    """Suivi des limites et de l'utilisation pour chaque utilisateur"""
    __tablename__ = "user_limits"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True, index=True)
    
    # Current usage counters
    saved_offers_count = Column(Integer, nullable=False, default=0)
    searches_today_count = Column(Integer, nullable=False, default=0)
    profiles_count = Column(Integer, nullable=False, default=0)
    applications_count = Column(Integer, nullable=False, default=0)
    cv_parsed_count = Column(Integer, nullable=False, default=0)
    watched_companies_count = Column(Integer, nullable=False, default=0)
    generated_cv_today_count = Column(Integer, nullable=False, default=0)
    
    # Custom limits (NULL = use default)
    max_saved_offers = Column(Integer, nullable=True)
    max_searches_per_day = Column(Integer, nullable=True)
    max_profiles = Column(Integer, nullable=True)
    max_applications = Column(Integer, nullable=True)
    max_cv_parses = Column(Integer, nullable=True)
    max_watched_companies = Column(Integer, nullable=True)
    max_generated_cv_per_day = Column(Integer, nullable=True)
    
    # Metadata for daily resets
    last_search_date = Column(Date, nullable=True)
    last_cv_generation_date = Column(Date, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    user = relationship("User", back_populates="limits")
    
    def get_limit(self, limit_type: str) -> int:
        """
        Get the effective limit for a given type.
        Returns custom limit if set, otherwise returns default.
        """
        custom_value = getattr(self, f"max_{limit_type}", None)
        if custom_value is not None:
            return custom_value
        return DEFAULT_LIMITS.get(f"max_{limit_type}", 0)
    
    def get_current(self, limit_type: str) -> int:
        """Get current usage count for a given type"""
        return getattr(self, f"{limit_type}_count", 0)
    
    def reset_daily_if_needed(self):
        """Reset daily counters if date has changed"""
        today = date.today()
        
        # Reset search counter
        if self.last_search_date != today:
            self.searches_today_count = 0
            self.last_search_date = today
        
        # Reset CV generation counter
        if self.last_cv_generation_date != today:
            self.generated_cv_today_count = 0
            self.last_cv_generation_date = today
    
    def __repr__(self):
        return f"<UserLimits user_id={self.user_id}>"
