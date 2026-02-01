"""API Routes pour la recherche d'offres et le feed personnalisé"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime
from sqlalchemy import select, and_, or_, func

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.job_offer import JobOffer
from app.schemas.search import SearchRequest, SearchResponse, FeedResponse, OfferResponse
from app.services.search_service import search_service

router = APIRouter(prefix="/search", tags=["search"])

@router.post("/scrape", response_model=SearchResponse)
async def search_with_scraping(
    request: SearchRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Recherche avec scraping des plateformes"""
    try:
        result = await search_service.search_with_scraping(
            db=db, keywords=request.keywords, location=request.location,
            job_type=request.job_type, work_mode=request.work_mode,
            company=request.company, limit_per_platform=request.limit_per_platform,
            user_id=str(current_user.id)
        )
        formatted_offers = [OfferResponse(
            title=o.get("title", ""), company=o.get("company", ""),
            location=o.get("location", ""), description=o.get("description", "")[:500],
            url=o.get("url", ""), source_platform=o.get("source_platform", ""),
            job_type=o.get("job_type"), work_mode=o.get("work_mode"),
            scraped_at=o.get("scraped_at").isoformat() if isinstance(o.get("scraped_at"), datetime) else o.get("scraped_at")
        ) for o in result.get("offers", [])]
        
        return SearchResponse(
            success=result["success"], offers=formatted_offers, count=result["count"],
            scraped_count=result.get("scraped_count"), deduplicated_count=result.get("deduplicated_count"),
            saved_count=result.get("saved_count"), platforms_scraped=result.get("platforms_scraped"),
            search_params=result.get("search_params"), scraped_at=result.get("scraped_at"),
            duration_seconds=result.get("duration_seconds")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur scraping: {str(e)}")

@router.get("/feed", response_model=FeedResponse)
async def get_personalized_feed(
    profile_id: str = Query(...),
    limit: int = Query(50, ge=1, le=100),
    min_score: float = Query(60.0, ge=0, le=100),
    max_age_days: int = Query(7, ge=1, le=30),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Feed personnalisé d'offres"""
    try:
        result = await search_service.get_feed(
            db=db, user_id=str(current_user.id), profile_id=profile_id,
            limit=limit, min_score=min_score, max_age_days=max_age_days
        )
        if not result["success"]:
            return FeedResponse(success=False, offers=[], count=0, error=result.get("error"))
        
        formatted_offers = [OfferResponse(**o) for o in result.get("offers", [])]
        return FeedResponse(
            success=True, offers=formatted_offers, count=result["count"],
            total_analyzed=result.get("total_analyzed"), min_score_applied=result.get("min_score_applied"),
            max_age_days=result.get("max_age_days"), message=result.get("message")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur feed: {str(e)}")

@router.get("/offers", response_model=SearchResponse)
async def list_offers(
    keywords: Optional[str] = None, location: Optional[str] = None,
    job_type: Optional[str] = None, work_mode: Optional[str] = None,
    page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Liste des offres sauvegardées avec filtres"""
    try:
        query = select(JobOffer)
        filters = []
        if keywords:
            filters.append(or_(JobOffer.title.ilike(f"%{keywords}%"), JobOffer.description.ilike(f"%{keywords}%")))
        if location:
            filters.append(JobOffer.location.ilike(f"%{location}%"))
        if job_type:
            filters.append(JobOffer.job_type == job_type)
        if work_mode:
            filters.append(JobOffer.work_mode == work_mode)
        if filters:
            query = query.where(and_(*filters))
        
        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page).order_by(JobOffer.created_at.desc())
        result = await db.execute(query)
        offers = result.scalars().all()
        
        count_query = select(func.count(JobOffer.id))
        if filters:
            count_query = count_query.where(and_(*filters))
        total = (await db.execute(count_query)).scalar()
        
        formatted_offers = [OfferResponse(
            id=str(o.id), title=o.job_title, company=o.company_name, location=o.location,
            description=(o.description or "")[:500], url=o.source_url or "",
            source_platform=o.source_platform or "unknown", job_type=o.job_type,
            work_mode=o.work_mode, scraped_at=o.scraped_at.isoformat() if o.scraped_at else None
        ) for o in offers]
        
        return SearchResponse(success=True, offers=formatted_offers, count=len(formatted_offers),
                            message=f"Page {page}/{(total + per_page - 1) // per_page}, Total: {total}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")
