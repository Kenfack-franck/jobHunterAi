"""
Schémas Pydantic pour la gestion des profils candidats.
"""
from datetime import date, datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from enum import Enum


# ==================== ENUMS ====================

class SkillLevel(str, Enum):
    """Niveau de maîtrise d'une compétence"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class SkillCategory(str, Enum):
    """Catégorie de compétence"""
    LANGUAGE = "language"
    FRAMEWORK = "framework"
    TOOL = "tool"
    SOFT_SKILL = "soft_skill"
    OTHER = "other"


# ==================== SKILL SCHEMAS ====================

class SkillBase(BaseModel):
    """Schéma de base pour une compétence"""
    name: str = Field(..., min_length=1, max_length=100)
    category: SkillCategory = SkillCategory.OTHER
    level: SkillLevel = SkillLevel.INTERMEDIATE


class SkillCreate(SkillBase):
    """Schéma pour créer une compétence"""
    pass


class SkillUpdate(BaseModel):
    """Schéma pour mettre à jour une compétence"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[SkillCategory] = None
    level: Optional[SkillLevel] = None


class SkillResponse(SkillBase):
    """Schéma de réponse pour une compétence"""
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== EDUCATION SCHEMAS ====================

class EducationBase(BaseModel):
    """Schéma de base pour une formation"""
    degree: str = Field(..., min_length=1, max_length=200)
    institution: str = Field(..., min_length=1, max_length=200)
    field_of_study: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=200)
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None
    
    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v, info):
        """Valide que la date de fin est après la date de début"""
        if v and 'start_date' in info.data:
            if v < info.data['start_date']:
                raise ValueError("end_date must be after start_date")
        return v


class EducationCreate(EducationBase):
    """Schéma pour créer une formation"""
    pass


class EducationUpdate(BaseModel):
    """Schéma pour mettre à jour une formation"""
    degree: Optional[str] = Field(None, min_length=1, max_length=200)
    institution: Optional[str] = Field(None, min_length=1, max_length=200)
    field_of_study: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=200)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None


class EducationResponse(EducationBase):
    """Schéma de réponse pour une formation"""
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== EXPERIENCE SCHEMAS ====================

class ExperienceBase(BaseModel):
    """Schéma de base pour une expérience professionnelle"""
    title: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=200)
    location: Optional[str] = Field(None, max_length=200)
    start_date: date
    end_date: Optional[date] = None
    current: bool = False
    description: Optional[str] = None
    technologies: Optional[List[str]] = Field(default_factory=list)
    
    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v, info):
        """Valide que la date de fin est après la date de début"""
        if v and 'start_date' in info.data:
            if v < info.data['start_date']:
                raise ValueError("end_date must be after start_date")
        return v
    
    @field_validator('end_date')
    @classmethod
    def validate_current(cls, v, info):
        """Si current=True, end_date doit être None"""
        if info.data.get('current') and v is not None:
            raise ValueError("end_date must be None when current is True")
        return v


class ExperienceCreate(ExperienceBase):
    """Schéma pour créer une expérience"""
    pass


class ExperienceUpdate(BaseModel):
    """Schéma pour mettre à jour une expérience"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    company: Optional[str] = Field(None, min_length=1, max_length=200)
    location: Optional[str] = Field(None, max_length=200)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    current: Optional[bool] = None
    description: Optional[str] = None
    technologies: Optional[List[str]] = None


class ExperienceResponse(ExperienceBase):
    """Schéma de réponse pour une expérience"""
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== PROFILE SCHEMAS ====================

class ProfileBase(BaseModel):
    """Schéma de base pour un profil"""
    title: str = Field(..., min_length=1, max_length=200, description="Titre professionnel (ex: 'Backend Developer')")
    summary: Optional[str] = Field(None, description="Résumé professionnel")
    location: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)
    linkedin_url: Optional[str] = Field(None, max_length=500)
    github_url: Optional[str] = Field(None, max_length=500)
    portfolio_url: Optional[str] = Field(None, max_length=500)


class ProfileCreate(ProfileBase):
    """Schéma pour créer un profil avec relations optionnelles"""
    experiences: Optional[List[ExperienceCreate]] = Field(default_factory=list)
    educations: Optional[List[EducationCreate]] = Field(default_factory=list)
    skills: Optional[List[SkillCreate]] = Field(default_factory=list)


class ProfileUpdate(BaseModel):
    """Schéma pour mettre à jour un profil"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    summary: Optional[str] = None
    location: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)
    linkedin_url: Optional[str] = Field(None, max_length=500)
    github_url: Optional[str] = Field(None, max_length=500)
    portfolio_url: Optional[str] = Field(None, max_length=500)


class ProfileResponse(ProfileBase):
    """Schéma de réponse pour un profil complet avec toutes les relations"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Relations
    experiences: List[ExperienceResponse] = Field(default_factory=list)
    educations: List[EducationResponse] = Field(default_factory=list)
    skills: List[SkillResponse] = Field(default_factory=list)
    
    class Config:
        from_attributes = True


class ProfileSummary(BaseModel):
    """Schéma résumé d'un profil (sans les relations)"""
    id: UUID
    title: str
    location: Optional[str] = None
    has_experiences: bool = False
    has_educations: bool = False
    has_skills: bool = False
    completion_percentage: int = Field(default=0, ge=0, le=100)
    
    class Config:
        from_attributes = True


# ==================== CV PARSING SCHEMAS ====================

class CVParseResponse(BaseModel):
    """Schéma pour la réponse du parsing de CV"""
    success: bool = True
    message: str = "CV analysé avec succès"
    profile_data: dict  # Contiendra les données extraites du CV
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "CV analysé avec succès ! Vérifiez les informations avant de sauvegarder.",
                "profile_data": {
                    "full_name": "Jean Dupont",
                    "title": "Développeur Full-Stack",
                    "summary": "Développeur passionné avec 5 ans d'expérience...",
                    "phone": "+33 6 12 34 56 78",
                    "location": "Paris, France",
                    "experiences": [],
                    "educations": [],
                    "skills": []
                }
            }
        }
