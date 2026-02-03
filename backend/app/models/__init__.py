"""
Package models - Importe tous les modèles pour Alembic
"""
from app.models.user import User
from app.models.profile import Profile, Experience, Education, Skill
from app.models.job_offer import JobOffer
from app.models.generated_document import GeneratedDocument
from app.models.user_source_preferences import UserSourcePreferences
from app.models.search_cache import SearchResultsCache

__all__ = [
    "User",
    "Profile",
    "Experience",
    "Education",
    "Skill",
    "JobOffer",
    "GeneratedDocument",
    "UserSourcePreferences",
    "SearchResultsCache"
]
