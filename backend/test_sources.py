#!/usr/bin/env python3
"""
Script de test pour valider chaque source individuellement
Teste que chaque source retourne bien des résultats
"""
import asyncio
import sys
sys.path.append('/app')

from app.services.scraping_service import scraping_service
from app.core.predefined_sources import PREDEFINED_SOURCES, get_source_by_id

async def test_source(source_id: str, keywords: str = "Python"):
    """
    Teste une source spécifique
    
    Args:
        source_id: ID de la source à tester
        keywords: Mots-clés de recherche
    """
    print(f"\n{'='*60}")
    print(f"🧪 TEST: {source_id}")
    print(f"{'='*60}")
    
    source = get_source_by_id(source_id)
    if not source:
        print(f"❌ Source '{source_id}' non trouvée")
        return {
            "source_id": source_id,
            "status": "NOT_FOUND",
            "offers_count": 0,
            "error": "Source non définie"
        }
    
    print(f"📋 Source: {source.name}")
    print(f"🌐 URL: {source.url}")
    print(f"🔧 Scraper: {source.scraper_type}")
    print(f"🔍 Keywords: {keywords}")
    
    try:
        # Tenter de scraper
        results = await scraping_service.scrape_priority_sources(
            priority_sources=[source_id],
            keywords=keywords,
            location="France",
            limit_per_source=10
        )
        
        offers = results.get(source_id, [])
        count = len(offers)
        
        if count > 0:
            print(f"✅ SUCCÈS: {count} offres trouvées")
            print("\n📦 Exemples d'offres:")
            for i, offer in enumerate(offers[:3], 1):
                print(f"  {i}. {offer.get('title', 'N/A')} - {offer.get('company', 'N/A')}")
                print(f"     📍 {offer.get('location', 'N/A')}")
            
            return {
                "source_id": source_id,
                "source_name": source.name,
                "status": "SUCCESS",
                "offers_count": count,
                "sample_offers": offers[:3]
            }
        else:
            print(f"⚠️ AVERTISSEMENT: Aucune offre trouvée")
            return {
                "source_id": source_id,
                "source_name": source.name,
                "status": "NO_RESULTS",
                "offers_count": 0
            }
            
    except Exception as e:
        print(f"❌ ERREUR: {type(e).__name__}: {str(e)}")
        return {
            "source_id": source_id,
            "source_name": source.name if source else "Unknown",
            "status": "ERROR",
            "offers_count": 0,
            "error": str(e)
        }

async def test_all_sources(keywords: str = "Python"):
    """
    Teste toutes les 18 sources prédéfinies
    """
    print("\n" + "="*60)
    print("🚀 DÉBUT DES TESTS - 18 SOURCES PRÉDÉFINIES")
    print("="*60)
    
    results = []
    
    for source in PREDEFINED_SOURCES:
        result = await test_source(source.id, keywords)
        results.append(result)
        await asyncio.sleep(1)  # Pause entre chaque test
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60)
    
    success = [r for r in results if r["status"] == "SUCCESS"]
    no_results = [r for r in results if r["status"] == "NO_RESULTS"]
    errors = [r for r in results if r["status"] == "ERROR"]
    not_found = [r for r in results if r["status"] == "NOT_FOUND"]
    
    print(f"\n✅ FONCTIONNELLES: {len(success)}/{len(results)}")
    for r in success:
        print(f"   • {r['source_name']}: {r['offers_count']} offres")
    
    print(f"\n⚠️ SANS RÉSULTATS: {len(no_results)}/{len(results)}")
    for r in no_results:
        print(f"   • {r['source_name']}")
    
    print(f"\n❌ ERREURS: {len(errors)}/{len(results)}")
    for r in errors:
        print(f"   • {r['source_name']}: {r.get('error', 'Unknown')}")
    
    if not_found:
        print(f"\n❓ NON TROUVÉES: {len(not_found)}/{len(results)}")
        for r in not_found:
            print(f"   • {r['source_id']}")
    
    print(f"\n📈 TAUX DE SUCCÈS: {len(success)}/{len(results)} ({len(success)*100//len(results)}%)")
    
    return results

async def test_user_selection(keywords: str = "Python"):
    """
    Teste la sélection actuelle de l'utilisateur:
    - Capgemini
    - Sopra Steria
    - Dassault Systèmes
    - L'Oréal
    """
    print("\n" + "="*60)
    print("👤 TEST SÉLECTION UTILISATEUR")
    print("="*60)
    
    user_sources = ["capgemini", "sopra_steria", "dassault_systemes", "loreal"]
    
    results = []
    for source_id in user_sources:
        result = await test_source(source_id, keywords)
        results.append(result)
        await asyncio.sleep(1)
    
    # Résumé sélection utilisateur
    print("\n" + "="*60)
    print("📊 RÉSUMÉ SÉLECTION UTILISATEUR")
    print("="*60)
    
    success = [r for r in results if r["status"] == "SUCCESS"]
    
    if success:
        print(f"\n✅ {len(success)}/{len(results)} sources fonctionnelles")
        for r in success:
            print(f"   • {r['source_name']}: {r['offers_count']} offres")
    else:
        print(f"\n❌ AUCUNE source ne retourne de résultats")
        print("\n💡 DIAGNOSTIC:")
        print("   Les scrapers pour ces entreprises ne sont pas encore implémentés.")
        print("   Voir backend/app/services/scraping_service.py ligne 340-367")
        print("   Mapping: capgemini → None, sopra_steria → None, etc.")
    
    return results

if __name__ == "__main__":
    print("🎯 Script de test des sources de scraping")
    print("Appuyez sur Ctrl+C pour arrêter\n")
    
    # Choix du test
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "user":
            asyncio.run(test_user_selection())
        elif sys.argv[1] == "all":
            asyncio.run(test_all_sources())
        else:
            source_id = sys.argv[1]
            keywords = sys.argv[2] if len(sys.argv) > 2 else "Python"
            asyncio.run(test_source(source_id, keywords))
    else:
        # Par défaut: tester sélection utilisateur
        asyncio.run(test_user_selection())
