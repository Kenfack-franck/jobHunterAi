"""
Modèle GeneratedDocument - Documents générés (CV, LM)
"""
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base


class GeneratedDocument(Base):
    """Document généré (CV ou Lettre de Motivation)"""
    __tablename__ = "generated_documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    job_offer_id = Column(UUID(as_uuid=True), ForeignKey("job_offers.id", ondelete="CASCADE"), nullable=False)
    
    # Type de document
    document_type = Column(String(50), nullable=False)  # "resume" ou "cover_letter"
    
    # Contenu
    content = Column(Text)  # Markdown (CV) ou texte brut (LM)
    pdf_path = Column(String(500))  # Path vers le PDF stocké (ex: "storage/documents/uuid.pdf")
    
    # Paramètres de génération (pour régénérer si besoin)
    generation_params = Column(JSONB)  # {"tone": "professional", "language": "fr", "length": "medium"}
    
    # Métadonnées
    language = Column(String(10), default="fr")
    filename = Column(String(255))  # Nom convivial (ex: "CV_TechCorp_2026.pdf")
    file_size = Column(Integer)     # Taille en bytes
    
    # Timestamps
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    user = relationship("User", back_populates="generated_documents")
    profile = relationship("Profile", back_populates="generated_documents")
    job_offer = relationship("JobOffer", back_populates="generated_documents")
    
    def __repr__(self):
        return f"<GeneratedDocument {self.document_type} for {self.job_offer_id}>"

