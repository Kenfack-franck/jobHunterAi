"""
Package models - Importe tous les modèles pour Alembic
"""
from app.models.user import User
from app.models.profile import Profile, Experience, Education, Skill
from app.models.job_offer import JobOffer
from app.models.generated_document import GeneratedDocument

__all__ = [
    "User",
    "Profile",
    "Experience",
    "Education",
    "Skill",
    "JobOffer",
    "GeneratedDocument"
]
