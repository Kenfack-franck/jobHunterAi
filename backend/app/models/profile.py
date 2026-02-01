"""
Modèle Profile - Profil du candidat
"""
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, UniqueConstraint, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
import uuid

from app.database import Base


class Profile(Base):
    """Modèle profil candidat (V1: un seul profil par user)"""
    __tablename__ = "profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Informations générales
    title = Column(String(255))  # Ex: "Développeur Full-Stack"
    summary = Column(Text)  # Résumé professionnel
    phone = Column(String(50))
    location = Column(String(255))
    
    # Liens sociaux
    linkedin_url = Column(String(500))
    github_url = Column(String(500))
    portfolio_url = Column(String(500))
    
    # Embedding vectoriel pour recherche sémantique (Phase 4)
    embedding = Column(Vector(384), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    user = relationship("User", back_populates="profile")
    experiences = relationship("Experience", back_populates="profile", cascade="all, delete-orphan", order_by="Experience.order_index.desc()")
    educations = relationship("Education", back_populates="profile", cascade="all, delete-orphan", order_by="Education.order_index.desc()")
    skills = relationship("Skill", back_populates="profile", cascade="all, delete-orphan")
    generated_documents = relationship("GeneratedDocument", back_populates="profile", cascade="all, delete-orphan")
    
    # Contrainte: un seul profil par user en V1
    __table_args__ = (
        UniqueConstraint('user_id', name='uq_user_profile'),
    )
    
    def __repr__(self):
        return f"<Profile {self.title}>"


class Experience(Base):
    """Expérience professionnelle"""
    __tablename__ = "experiences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    
    title = Column(String(255), nullable=False)  # Poste occupé
    company = Column(String(255), nullable=False)
    location = Column(String(255))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)  # NULL si poste actuel
    current = Column(Boolean, default=False)  # True si poste en cours
    description = Column(Text)
    technologies = Column(ARRAY(String))  # Liste de technologies PostgreSQL
    order_index = Column(Integer, default=0)  # Pour tri personnalisé
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relation
    profile = relationship("Profile", back_populates="experiences")
    
    def __repr__(self):
        return f"<Experience {self.title} @ {self.company}>"


class Education(Base):
    """Formation académique"""
    __tablename__ = "educations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    
    degree = Column(String(255), nullable=False)
    institution = Column(String(255), nullable=False)
    location = Column(String(255))  # Localisation de l'établissement
    field_of_study = Column(String(255))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    description = Column(Text)
    order_index = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relation
    profile = relationship("Profile", back_populates="educations")
    
    def __repr__(self):
        return f"<Education {self.degree} @ {self.institution}>"


class Skill(Base):
    """Compétence"""
    __tablename__ = "skills"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String(100), nullable=False)
    category = Column(String(50))  # "language", "framework", "tool", "soft_skill"
    level = Column(String(50))  # "beginner", "intermediate", "advanced", "expert"
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relation
    profile = relationship("Profile", back_populates="skills")
    
    def __repr__(self):
        return f"<Skill {self.name}>"
