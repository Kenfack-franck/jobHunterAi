"""Test scraping simple"""
import asyncio
import sys
sys.path.insert(0, '/app')

async def main():
    from app.database import SessionLocal
    from app.services.company_watch_service import CompanyWatchService
    
    print("🧪 TEST SCRAPING")
    print("")
    
    db = SessionLocal()
    try:
        service = CompanyWatchService(db)
        result = await service.scrape_watched_companies()
        
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"✅ Entreprises: {result['total_companies_scraped']}")
        print(f"✅ Offres trouvées: {result['total_offers_found']}")
        print(f"✅ Offres sauvegardées: {result.get('total_offers_saved', 0)}")
        print(f"❌ Erreurs: {result['errors_count']}")
        for err in result.get('errors', []):
            print(f"   {err['company']}: {err['error'][:100]}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await db.close()

asyncio.run(main())
