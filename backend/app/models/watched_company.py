from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class WatchedCompany(Base):
    __tablename__ = "watched_companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String(200), nullable=False)
    company_slug = Column(String(200), unique=True, nullable=False, index=True)
    
    # URLs des différentes plateformes
    linkedin_url = Column(String(500), nullable=True)
    careers_url = Column(String(500), nullable=True)
    indeed_url = Column(String(500), nullable=True)
    wttj_url = Column(String(500), nullable=True)
    
    # Métadonnées scraping
    last_scraped_at = Column(DateTime, nullable=True)
    scraping_frequency = Column(Integer, default=24, nullable=False)  # Heures
    
    # Statistiques
    total_watchers = Column(Integer, default=0, nullable=False)
    total_offers_found = Column(Integer, default=0, nullable=False)
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relations
    user_watches = relationship("UserCompanyWatch", back_populates="watched_company", cascade="all, delete-orphan")


class UserCompanyWatch(Base):
    __tablename__ = "user_company_watches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    watched_company_id = Column(UUID(as_uuid=True), ForeignKey("watched_companies.id", ondelete="CASCADE"), nullable=False, index=True)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="SET NULL"), nullable=True)
    
    alert_threshold = Column(Integer, default=70, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relations
    watched_company = relationship("WatchedCompany", back_populates="user_watches")
