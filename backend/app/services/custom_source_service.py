"""
Service de gestion des sources custom (career pages)
Permet aux utilisateurs d'ajouter leurs propres URLs à scraper
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc, func
import httpx
from bs4 import BeautifulSoup

from app.models.custom_source import CustomSource


class CustomSourceService:
    """Service de gestion des sources personnalisées"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def add_custom_source(
        self,
        user_id: UUID,
        source_name: str,
        source_url: str,
        scraping_frequency: str = "every_4_hours"
    ) -> Dict[str, Any]:
        """
        Ajoute une source personnalisée après analyse
        
        Args:
            user_id: ID utilisateur
            source_name: Nom de la source (ex: "Airbnb Careers")
            source_url: URL à scraper
            scraping_frequency: Fréquence de scraping
        
        Returns:
            Dict avec résultat et métadonnées
        
        Raises:
            ValueError: Si URL déjà existante ou non accessible
        """
        # Vérifier si URL existe déjà pour cet utilisateur
        from sqlalchemy import select
        existing = await self.db.execute(
            select(CustomSource).where(
                CustomSource.user_id == user_id,
                CustomSource.source_url == source_url
            )
        )
        if existing.scalar_one_or_none():
            raise ValueError("Cette URL a déjà été ajoutée")
        
        # Analyser l'URL
        analysis = await self.analyze_url(source_url)
        
        if not analysis["is_accessible"]:
            raise ValueError(f"URL non accessible: {analysis.get('recommendation', 'Inconnu')}")
        
        # Créer source
        custom_source = CustomSource(
            user_id=user_id,
            source_url=source_url,
            source_type=analysis.get("content_type", "html"),
            is_active=analysis.get("is_scrapable", False),  # Auto-activer si scrapable
            scraping_frequency=scraping_frequency
        )
        # Définir le nom après initialisation
        custom_source.source_name = source_name
        
        self.db.add(custom_source)
        await self.db.commit()
        await self.db.refresh(custom_source)
        
        return {
            "id": custom_source.id,
            "user_id": custom_source.user_id,
            "source_name": custom_source.source_name,
            "source_url": custom_source.source_url,
            "source_type": custom_source.source_type,
            "is_active": custom_source.is_active,
            "scraping_frequency": custom_source.scraping_frequency,
            "created_at": custom_source.created_at,
            "last_scraped_at": custom_source.last_scraped_at,
            "total_offers_found": custom_source.total_offers_found or 0,
            "analysis": analysis
        }
    
    async def analyze_url(self, url: str) -> Dict[str, Any]:
        """
        Analyse une URL pour déterminer si elle est scrapable
        
        Args:
            url: URL à analyser
        
        Returns:
            Dict avec métadonnées : accessible, type, has_jobs, anti_bot
        """
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                response = await client.get(
                    url,
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                )
            
            if response.status_code != 200:
                return {
                    "accessible": False,
                    "error": f"HTTP {response.status_code}",
                    "type": None,
                    "has_jobs": False
                }
            
            content_type = response.headers.get("content-type", "").lower()
            
            # Déterminer le type
            if "application/json" in content_type:
                source_type = "json"
                has_jobs = "job" in response.text.lower() or "position" in response.text.lower()
            elif "text/html" in content_type:
                source_type = "html"
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Détecter si page contient offres
                job_keywords = ["job", "career", "position", "hiring", "vacancy", "opening", "emploi", "poste"]
                text_lower = soup.get_text().lower()
                has_jobs = any(keyword in text_lower for keyword in job_keywords)
                
                # Détecter nombre potentiel d'offres
                # Heuristique: chercher des patterns communs
                job_elements = (
                    soup.find_all(class_=lambda x: x and ('job' in x.lower() or 'position' in x.lower())) +
                    soup.find_all('div', attrs={'data-job': True}) +
                    soup.find_all('a', href=lambda x: x and '/job' in x.lower())
                )
                estimated_jobs = len(set(str(el) for el in job_elements[:20]))  # Dédoublonner
            else:
                source_type = "unknown"
                has_jobs = False
                estimated_jobs = 0
            
            # Détecter anti-bot (basique)
            anti_bot_indicators = ["cloudflare", "captcha", "recaptcha", "bot detection", "access denied"]
            has_antibot = any(indicator in response.text.lower() for indicator in anti_bot_indicators)
            
            # Déterminer scrapabilité
            is_scrapable = has_jobs and not has_antibot
            
            # Mots-clés trouvés
            job_keywords_found = []
            if has_jobs:
                keywords_list = ["job", "career", "position", "hiring", "vacancy", "opening", "emploi", "poste"]
                text_lower = response.text.lower()
                job_keywords_found = [kw for kw in keywords_list if kw in text_lower]
            
            # Indicateurs anti-bot trouvés
            anti_bot_found = []
            if has_antibot:
                anti_bot_indicators = ["cloudflare", "captcha", "recaptcha", "bot detection", "access denied"]
                text_lower = response.text.lower()
                anti_bot_found = [ind for ind in anti_bot_indicators if ind in text_lower]
            
            recommendation = self._get_recommendation(has_jobs, has_antibot, source_type)
            
            return {
                "is_accessible": True,
                "content_type": source_type,
                "has_jobs": has_jobs,
                "job_keywords_found": job_keywords_found,
                "estimated_job_count": estimated_jobs if source_type == "html" else None,
                "has_anti_bot": has_antibot,
                "anti_bot_indicators": anti_bot_found,
                "recommendation": recommendation,
                "is_scrapable": is_scrapable
            }
        
        except Exception as e:
            return {
                "is_accessible": False,
                "content_type": "unknown",
                "has_jobs": False,
                "job_keywords_found": [],
                "estimated_job_count": None,
                "has_anti_bot": False,
                "anti_bot_indicators": [],
                "recommendation": f"❌ Erreur: {str(e)}",
                "is_scrapable": False
            }
    
    def _get_recommendation(self, has_jobs: bool, has_antibot: bool, source_type: str) -> str:
        """Recommandation pour l'utilisateur"""
        if not has_jobs:
            return "⚠️ Aucune offre détectée. Cette URL ne semble pas être une page carrières."
        elif has_antibot:
            return "⚠️ Anti-bot détecté. Le scraping peut échouer. Nous recommandons de tester."
        elif source_type == "json":
            return "✅ API JSON détectée. Scraping facile et fiable."
        else:
            return "✅ Page HTML avec offres détectées. Scraping possible."
    
    async def get_user_sources(
        self,
        user_id: UUID,
        page: int = 1,
        per_page: int = 20,
        active_only: bool = False
    ) -> Dict[str, Any]:
        """Liste les sources d'un utilisateur"""
        offset = (page - 1) * per_page
        
        # Base query
        query = select(CustomSource).where(CustomSource.user_id == user_id)
        
        # Filtrer si active_only
        if active_only:
            query = query.where(CustomSource.is_active == True)
        
        query = query.order_by(desc(CustomSource.created_at)).offset(offset).limit(per_page)
        
        result = await self.db.execute(query)
        sources = result.scalars().all()
        
        # Query total count
        count_query = select(func.count(CustomSource.id)).where(CustomSource.user_id == user_id)
        if active_only:
            count_query = count_query.where(CustomSource.is_active == True)
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        formatted = []
        for s in sources:
            formatted.append({
                "id": s.id,
                "user_id": s.user_id,
                "source_name": s.source_name,
                "source_url": s.source_url,
                "source_type": s.source_type,
                "is_active": s.is_active,
                "scraping_frequency": s.scraping_frequency,
                "last_scraped_at": s.last_scraped_at,
                "created_at": s.created_at,
                "total_offers_found": s.total_offers_found or 0
            })
        
        return {
            "sources": formatted,
            "total": total,
            "page": page,
            "per_page": per_page
        }
    
    async def delete_source(self, user_id: UUID, source_id: int) -> bool:
        """
        Supprime une source personnalisée
        
        Args:
            user_id: ID de l'utilisateur
            source_id: ID de la source à supprimer
            
        Returns:
            bool: True si supprimée, False sinon
        """
        query = select(CustomSource).where(
            and_(
                CustomSource.id == source_id,
                CustomSource.user_id == user_id
            )
        )
        result = await self.db.execute(query)
        source = result.scalar_one_or_none()
        
        if not source:
            return False
        
        await self.db.delete(source)
        await self.db.commit()
        
        return True
