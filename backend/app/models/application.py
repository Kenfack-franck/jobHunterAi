"""
Application model - Candidatures utilisateur
"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import uuid

from app.database import Base


class ApplicationStatus(str, enum.Enum):
    """Status possible d'une candidature"""
    PENDING = "pending"
    REPLIED = "replied"
    INTERVIEW = "interview"
    REJECTED = "rejected"
    ACCEPTED = "accepted"


class Application(Base):
    """Modèle pour les candidatures envoyées"""
    __tablename__ = "applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_offer_id = Column(UUID(as_uuid=True), ForeignKey("job_offers.id", ondelete="SET NULL"), nullable=True)
    
    company_name = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=False)
    email_to = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    notes = Column(Text, nullable=True)
    documents_sent = Column(JSONB, nullable=True)
    
    applied_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relations
    user = relationship("User", back_populates="applications")
    job_offer = relationship("JobOffer", back_populates="applications")
