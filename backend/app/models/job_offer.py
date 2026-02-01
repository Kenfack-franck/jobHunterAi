"""
Modèle JobOffer - Offre d'emploi analysée
"""
from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
import uuid

from app.database import Base


class JobOffer(Base):
    """Offre d'emploi analysée"""
    __tablename__ = "job_offers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Source
    source_url = Column(String(1000))
    source_platform = Column(String(100))  # "LinkedIn", "Indeed", "Manual"
    
    # Détails de l'offre
    company_name = Column(String(255))
    job_title = Column(String(255), nullable=False)
    location = Column(String(255))
    job_type = Column(String(50))  # "CDI", "CDD", "Stage", "Remote"
    work_mode = Column(String(20))  # "remote", "hybrid", "onsite"
    description = Column(Text)
    requirements = Column(Text)
    
    # Données extraites
    extracted_keywords = Column(JSONB)  # Liste de mots-clés/compétences
    
    # Embedding vectoriel pour recherche sémantique (Phase 4)
    embedding = Column(Vector(384), nullable=True)
    
    # Timestamps
    scraped_at = Column(DateTime(timezone=True))
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User", back_populates="job_offers")
    generated_documents = relationship("GeneratedDocument", back_populates="job_offer", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<JobOffer {self.job_title} @ {self.company_name}>"
    applications = relationship("Application", back_populates="job_offer")
