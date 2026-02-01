"""
Script de test pour valider les scrapers
"""
import asyncio
import sys
import os

# Ajouter le chemin du backend au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.scrapers.indeed_scraper import IndeedScraper
from app.services.scrapers.wttj_scraper import WTTJScraper
from app.services.scrapers.remoteok_scraper import RemoteOKScraper


async def test_indeed():
    """Tester IndeedScraper"""
    print("\n" + "="*80)
    print("🔍 TEST: IndeedScraper")
    print("="*80)
    
    scraper = IndeedScraper()
    
    try:
        offers = await scraper.scrape(
            keywords="Python Developer",
            location="Paris",
            max_results=5
        )
        
        print(f"\n✅ IndeedScraper: {len(offers)} offres trouvées")
        
        # Afficher les 3 premières offres
        for i, offer in enumerate(offers[:3], 1):
            print(f"\n--- Offre {i} ---")
            print(f"Titre: {offer['title']}")
            print(f"Entreprise: {offer['company']}")
            print(f"Localisation: {offer['location']}")
            print(f"Type: {offer['job_type']} | Mode: {offer['work_mode']}")
            print(f"URL: {offer['url'][:80]}...")
            print(f"Description: {offer['description'][:150]}...")
        
        return True
    
    except Exception as e:
        print(f"\n❌ Erreur IndeedScraper: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_wttj():
    """Tester WTTJScraper"""
    print("\n" + "="*80)
    print("🔍 TEST: WTTJScraper (Welcome to the Jungle)")
    print("="*80)
    
    scraper = WTTJScraper()
    
    try:
        offers = await scraper.scrape(
            keywords="Developer",
            location="Paris",
            max_results=5
        )
        
        print(f"\n✅ WTTJScraper: {len(offers)} offres trouvées")
        
        # Afficher les 3 premières offres
        for i, offer in enumerate(offers[:3], 1):
            print(f"\n--- Offre {i} ---")
            print(f"Titre: {offer['title']}")
            print(f"Entreprise: {offer['company']}")
            print(f"Localisation: {offer['location']}")
            print(f"Type: {offer['job_type']} | Mode: {offer['work_mode']}")
            print(f"URL: {offer['url'][:80]}...")
            print(f"Tags: {', '.join(offer.get('tags', [])[:5])}")
        
        return True
    
    except Exception as e:
        print(f"\n❌ Erreur WTTJScraper: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_remoteok():
    """Tester RemoteOKScraper"""
    print("\n" + "="*80)
    print("🔍 TEST: RemoteOKScraper")
    print("="*80)
    
    scraper = RemoteOKScraper()
    
    try:
        offers = await scraper.scrape(
            keywords="Python",
            max_results=5
        )
        
        print(f"\n✅ RemoteOKScraper: {len(offers)} offres trouvées")
        
        # Afficher les 3 premières offres
        for i, offer in enumerate(offers[:3], 1):
            print(f"\n--- Offre {i} ---")
            print(f"Titre: {offer['title']}")
            print(f"Entreprise: {offer['company']}")
            print(f"Localisation: {offer['location']}")
            print(f"Type: {offer['job_type']} | Mode: {offer['work_mode']}")
            print(f"URL: {offer['url'][:80]}...")
            print(f"Tags: {', '.join(offer.get('tags', [])[:5])}")
            if offer.get('salary'):
                print(f"Salaire: {offer['salary']}")
        
        return True
    
    except Exception as e:
        print(f"\n❌ Erreur RemoteOKScraper: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Tester tous les scrapers"""
    print("\n" + "🚀"*40)
    print("🧪 TESTS DES SCRAPERS - PHASE 2")
    print("🚀"*40)
    
    results = {}
    
    # Test RemoteOK en premier (API, plus rapide et fiable)
    print("\n\n📍 Test 1/3: RemoteOK (API)")
    results['remoteok'] = await test_remoteok()
    
    # Test WTTJ
    print("\n\n📍 Test 2/3: Welcome to the Jungle")
    results['wttj'] = await test_wttj()
    
    # Test Indeed (le plus complexe, anti-bot)
    print("\n\n📍 Test 3/3: Indeed")
    results['indeed'] = await test_indeed()
    
    # Résumé
    print("\n" + "="*80)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*80)
    
    for platform, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{platform:20} : {status}")
    
    total = len(results)
    passed = sum(1 for s in results.values() if s)
    
    print(f"\n🎯 Score: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS !")
    else:
        print(f"\n⚠️  {total - passed} test(s) ont échoué")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    asyncio.run(main())
