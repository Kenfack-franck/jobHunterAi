"""
Script de test pour scraping entreprises
Usage: docker exec jobhunter_backend python /app/test_company_scraping.py
"""
import asyncio
import sys
sys.path.insert(0, '/app')

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config import settings
from app.services.company_watch_service import CompanyWatchService

# Créer engine et session
engine = create_async_engine(settings.DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def main():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🧪 TEST SCRAPING ENTREPRISES SURVEILLÉES")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("")
    
    async with async_session_maker() as db:
        try:
            # Créer service
            service = CompanyWatchService(db)
            
            # Lancer scraping
            print("🚀 Lancement du scraping...")
            result = await service.scrape_watched_companies()
            
            print("")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("📊 RÉSULTATS")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"Success: {result['success']}")
            print(f"Entreprises scrapées: {result['total_companies_scraped']}")
            print(f"Offres trouvées: {result['total_offers_found']}")
            print(f"Offres sauvegardées: {result.get('total_offers_saved', 0)}")
            print(f"Erreurs: {result['errors_count']}")
            
            if result['errors']:
                print("\n❌ Erreurs détaillées:")
                for error in result['errors']:
                    print(f"  - {error['company']}: {error['error']}")
            
            print("")
            print("✅ Test terminé")
            
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
