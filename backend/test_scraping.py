"""Test scraping final"""
import asyncio
import sys
sys.path.insert(0, '/app')

async def main():
    from app.database import AsyncSessionLocal
    from app.services.company_watch_service import CompanyWatchService
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🧪 TEST SCRAPING ENTREPRISES SURVEILLÉES")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("")
    
    async with AsyncSessionLocal() as db:
        try:
            service = CompanyWatchService(db)
            print("🚀 Lancement scraping (2-3 min si Indeed répond)...")
            print("")
            
            result = await service.scrape_watched_companies()
            
            print("")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("📊 RÉSULTATS")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"✅ Entreprises scrapées: {result['total_companies_scraped']}")
            print(f"✅ Offres trouvées: {result['total_offers_found']}")
            print(f"✅ Offres sauvegardées: {result.get('total_offers_saved', 0)}")
            print(f"❌ Erreurs: {result['errors_count']}")
            
            if result.get('errors'):
                print("\n📋 Détails erreurs:")
                for err in result['errors']:
                    error_msg = err['error'][:150] if len(err['error']) > 150 else err['error']
                    print(f"   • {err['company']}: {error_msg}")
            
            print("\n✅ Test terminé")
            
        except Exception as e:
            print(f"\n❌ Erreur globale: {e}")
            import traceback
            traceback.print_exc()

asyncio.run(main())
