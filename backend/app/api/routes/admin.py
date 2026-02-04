"""
Routes Admin - Gestion des utilisateurs et statistiques
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional, List
from datetime import datetime, timedelta
import uuid

from app.database import get_db
from app.models.user import User
from app.models.user_limits import UserLimits
from app.api.dependencies.admin import require_admin
from app.services.limit_service import LimitService
from app.schemas.admin import (
    UserListResponse,
    UserDetailResponse,
    UpdateUserLimitsRequest,
    UserStatsResponse,
    AdminDashboardStats
)

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=UserListResponse)
async def list_users(
    search: Optional[str] = Query(None, description="Recherche par email"),
    status_filter: Optional[str] = Query('all', description="active | blocked | all"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Liste tous les utilisateurs avec leurs statistiques d'utilisation.
    Accessible uniquement par les admins.
    """
    # Build query
    stmt = select(User)
    
    # Apply filters
    if search:
        stmt = stmt.where(User.email.ilike(f"%{search}%"))
    
    if status_filter == 'active':
        stmt = stmt.where(User.is_active == True)
    elif status_filter == 'blocked':
        stmt = stmt.where(User.is_active == False)
    
    # Get total count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0
    
    # Pagination
    offset = (page - 1) * per_page
    stmt = stmt.order_by(desc(User.created_at)).offset(offset).limit(per_page)
    
    result = await db.execute(stmt)
    users = result.scalars().all()
    
    # Format user data (sans les stats d'usage pour l'instant)
    user_data = []
    for user in users:
        # Usage stats simplifiés (à implémenter plus tard avec LimitService async)
        usage = {
            "saved_offers": {"current": 0, "limit": 50, "percentage": 0},
            "searches_today": {"current": 0, "limit": 50, "percentage": 0},
            "profiles": {"current": 0, "limit": 3, "percentage": 0},
            "applications": {"current": 0, "limit": 30, "percentage": 0}
        }
        
        user_data.append({
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "usage": usage
        })
    
    return {
        "users": user_data,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page if total > 0 else 0
    }


@router.get("/users/{user_id}", response_model=UserDetailResponse)
async def get_user_detail(
    user_id: uuid.UUID,
    current_admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Récupère les détails complets d'un utilisateur.
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    # Get usage stats
    limit_service = LimitService(db)
    usage = limit_service.get_user_usage_stats(user.id)
    
    # Get custom limits if any
    limits = db.query(UserLimits).filter(UserLimits.user_id == user_id).first()
    custom_limits = {}
    if limits:
        for field in ['max_saved_offers', 'max_searches_per_day', 'max_profiles', 
                      'max_applications', 'max_cv_parses', 'max_watched_companies', 
                      'max_generated_cv_per_day']:
            value = getattr(limits, field, None)
            if value is not None:
                custom_limits[field] = value
    
    return {
        "id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active,
        "language": user.language,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        "usage": usage,
        "custom_limits": custom_limits if custom_limits else None
    }


@router.put("/users/{user_id}/toggle-active")
async def toggle_user_active(
    user_id: uuid.UUID,
    current_admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Bloquer ou débloquer un utilisateur (toggle is_active).
    """
    from sqlalchemy import select
    
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    # Don't allow admin to block themselves
    if user.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous ne pouvez pas vous bloquer vous-même"
        )
    
    # Toggle active status
    user.is_active = not user.is_active
    await db.commit()
    await db.refresh(user)
    
    return {
        "user_id": str(user.id),
        "email": user.email,
        "is_active": user.is_active,
        "message": f"Utilisateur {'activé' if user.is_active else 'bloqué'} avec succès"
    }


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: uuid.UUID,
    confirm: str = Query(..., description="Tapez 'yes' pour confirmer"),
    current_admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Supprimer complètement un utilisateur et toutes ses données.
    Nécessite confirmation (confirm=yes).
    """
    from sqlalchemy import select, delete as sql_delete
    
    if confirm != 'yes':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Confirmation requise. Ajoutez ?confirm=yes"
        )
    
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    # Don't allow admin to delete themselves
    if user.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous ne pouvez pas supprimer votre propre compte"
        )
    
    # Count related data before deletion (for response)
    email = user.email
    profiles_count = 1 if user.profile else 0
    job_offers_count = len(user.job_offers) if user.job_offers else 0
    applications_count = len(user.applications) if user.applications else 0
    
    # Delete user (CASCADE will delete related data)
    await db.delete(user)
    await db.commit()
    
    return {
        "message": "Utilisateur et toutes ses données supprimés",
        "email": email,
        "deleted": {
            "user": True,
            "profiles": profiles_count,
            "job_offers": job_offers_count,
            "applications": applications_count
        }
    }


@router.get("/stats", response_model=AdminDashboardStats)
async def get_admin_stats(
    current_admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Statistiques globales pour le dashboard admin.
    """
    # Total users
    result = await db.execute(select(func.count(User.id)))
    total_users = result.scalar() or 0
    
    result = await db.execute(select(func.count(User.id)).where(User.is_active == True))
    active_users = result.scalar() or 0
    
    result = await db.execute(select(func.count(User.id)).where(User.is_active == False))
    blocked_users = result.scalar() or 0
    
    # New users this week
    week_ago = datetime.now() - timedelta(days=7)
    result = await db.execute(
        select(func.count(User.id)).where(User.created_at >= week_ago)
    )
    new_users_this_week = result.scalar() or 0
    
    # New users today
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    result = await db.execute(
        select(func.count(User.id)).where(User.created_at >= today_start)
    )
    new_users_today = result.scalar() or 0
    
    # Users near limit - Simplified (à implémenter plus tard avec LimitService async)
    users_near_limit = []
    
    # Registrations last 7 days
    registrations_last_7_days = {}
    for i in range(7):
        day = datetime.now() - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        result = await db.execute(
            select(func.count(User.id)).where(
                User.created_at >= day_start,
                User.created_at < day_end
            )
        )
        count = result.scalar() or 0
        
        registrations_last_7_days[day.strftime('%Y-%m-%d')] = count
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "blocked_users": blocked_users,
        "new_users_this_week": new_users_this_week,
        "new_users_today": new_users_today,
        "users_near_limit": users_near_limit,  # Temporairement vide
        "registrations_last_7_days": registrations_last_7_days
    }
