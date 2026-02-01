"""Debug RemoteOK companies"""
import asyncio
import sys
sys.path.insert(0, '/app')

async def main():
    from app.services.scrapers.remoteok_scraper import RemoteOKScraper
    
    print("🔍 DEBUG: Noms d'entreprises dans RemoteOK\n")
    
    scraper = RemoteOKScraper()
    
    # Test Google
    print("━━━ Recherche 'Google' ━━━")
    offers = await scraper.scrape(keywords="Google", location=None, max_results=15)
    print(f"Total: {len(offers)} offres\n")
    print("Entreprises trouvées:")
    for i, o in enumerate(offers[:10], 1):
        print(f"  {i}. '{o.get('company', 'N/A')}'")
    
    print("\n━━━ Recherche 'Microsoft' ━━━")
    offers = await scraper.scrape(keywords="Microsoft", location=None, max_results=10)
    print(f"Total: {len(offers)} offres\n")
    print("Entreprises trouvées:")
    for i, o in enumerate(offers[:10], 1):
        print(f"  {i}. '{o.get('company', 'N/A')}'")

asyncio.run(main())
