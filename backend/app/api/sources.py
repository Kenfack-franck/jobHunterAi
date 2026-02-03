from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.user_source_preferences import UserSourcePreferences
from app.schemas.source_preferences import (
    SourcePreferencesCreate,
    SourcePreferencesUpdate,
    SourcePreferencesResponse,
    SourcesListResponse,
    PredefinedSourceInfo
)
from app.core.predefined_sources import (
    PREDEFINED_SOURCES,
    get_default_enabled_sources,
    get_aggregators,
    get_source_by_id,
    SourceType
)
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/predefined", response_model=SourcesListResponse)
def get_predefined_sources(current_user: User = Depends(get_current_user)):
    """
    Récupère toutes les sources prédéfinies disponibles
    """
    all_sources_info = [
        PredefinedSourceInfo(
            id=s.id,
            name=s.name,
            url=s.url,
            source_type=s.source_type.value,
            logo_url=s.logo_url,
            scraper_type=s.scraper_type,
            priority=s.priority,
            enabled_by_default=s.enabled_by_default
        )
        for s in PREDEFINED_SOURCES
    ]
    
    aggregators = [s for s in all_sources_info if s.source_type == SourceType.AGGREGATOR.value]
    companies = [s for s in all_sources_info if s.source_type != SourceType.AGGREGATOR.value]
    
    return SourcesListResponse(
        aggregators=aggregators,
        companies=companies,
        all_sources=all_sources_info,
        total_count=len(all_sources_info)
    )


@router.get("/preferences", response_model=SourcePreferencesResponse)
async def get_user_preferences(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les préférences de sources de l'utilisateur.
    Si elles n'existent pas, crée des préférences par défaut.
    """
    stmt = select(UserSourcePreferences).where(
        UserSourcePreferences.user_id == current_user.id
    )
    result = await db.execute(stmt)
    prefs = result.scalar_one_or_none()
    
    if not prefs:
        # Créer des préférences par défaut
        default_sources = get_default_enabled_sources()
        prefs = UserSourcePreferences(
            user_id=current_user.id,
            enabled_sources=default_sources,
            priority_sources=default_sources[:3],  # Les 3 premiers par défaut
            use_cache=True,
            cache_ttl_hours=24,
            max_priority_sources=3,
            background_scraping_enabled=True
        )
        db.add(prefs)
        await db.commit()
        await db.refresh(prefs)
    
    return prefs


@router.put("/preferences", response_model=SourcePreferencesResponse)
async def update_user_preferences(
    preferences: SourcePreferencesUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Met à jour les préférences de sources de l'utilisateur
    """
    stmt = select(UserSourcePreferences).where(
        UserSourcePreferences.user_id == current_user.id
    )
    result = await db.execute(stmt)
    prefs = result.scalar_one_or_none()
    
    if not prefs:
        # Créer si n'existe pas
        prefs = UserSourcePreferences(user_id=current_user.id)
        db.add(prefs)
    
    # Mettre à jour les champs fournis
    update_data = preferences.model_dump(exclude_unset=True)
    
    # Validation : vérifier que les sources existent
    if "enabled_sources" in update_data:
        for source_id in update_data["enabled_sources"]:
            if not get_source_by_id(source_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Source inconnue : {source_id}"
                )
    
    if "priority_sources" in update_data:
        for source_id in update_data["priority_sources"]:
            if not get_source_by_id(source_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Source inconnue : {source_id}"
                )
        
        # Vérifier la limite de sources prioritaires
        max_allowed = prefs.max_priority_sources if "max_priority_sources" not in update_data else update_data["max_priority_sources"]
        if len(update_data["priority_sources"]) > max_allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Nombre maximum de sources prioritaires : {max_allowed}"
            )
    
    for key, value in update_data.items():
        setattr(prefs, key, value)
    
    await db.commit()
    await db.refresh(prefs)
    
    return prefs


@router.post("/preferences/reset", response_model=SourcePreferencesResponse)
async def reset_user_preferences(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Réinitialise les préférences aux valeurs par défaut
    """
    stmt = select(UserSourcePreferences).where(
        UserSourcePreferences.user_id == current_user.id
    )
    result = await db.execute(stmt)
    prefs = result.scalar_one_or_none()
    
    default_sources = get_default_enabled_sources()
    
    if not prefs:
        prefs = UserSourcePreferences(user_id=current_user.id)
        db.add(prefs)
    
    prefs.enabled_sources = default_sources
    prefs.priority_sources = default_sources[:3]
    prefs.use_cache = True
    prefs.cache_ttl_hours = 24
    prefs.max_priority_sources = 3
    prefs.background_scraping_enabled = True
    
    await db.commit()
    await db.refresh(prefs)
    
    return prefs
