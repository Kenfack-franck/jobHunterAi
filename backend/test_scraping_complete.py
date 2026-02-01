#!/usr/bin/env python3
"""
Script de test complet du scraping
Teste les 3 plateformes: RemoteOK, Indeed, WTTJ
"""
import asyncio
import sys
sys.path.insert(0, '/app')

from app.services.scraping_service import scraping_service
from app.platforms_config.platforms import get_enabled_platforms


async def test_scraping():
    """Test complet du scraping sur les 3 plateformes"""
    
    print("\n" + "="*70)
    print("🔍 TEST COMPLET DU SCRAPING")
    print("="*70)
    
    # 1. Vérifier les plateformes activées
    print("\n📋 ÉTAPE 1: Vérification des plateformes activées")
    print("-" * 70)
    
    enabled_platforms = get_enabled_platforms()
    print(f"Plateformes activées: {list(enabled_platforms.keys())}")
    
    for platform_name, config in enabled_platforms.items():
        print(f"  ✅ {platform_name}: enabled={config.get('enabled', False)}")
    
    if not enabled_platforms:
        print("❌ ERREUR: Aucune plateforme activée!")
        return
    
    # 2. Test de scraping avec mots-clés
    print("\n\n🌐 ÉTAPE 2: Test scraping avec 'Python Developer'")
    print("-" * 70)
    
    keywords = "Python Developer"
    location = "Paris"
    
    print(f"Mots-clés: {keywords}")
    print(f"Localisation: {location}")
    print(f"Limite par plateforme: 5 offres\n")
    
    try:
        results = await scraping_service.scrape_all_platforms(
            keywords=keywords,
            location=location,
            limit_per_platform=5
        )
        
        print("\n📊 RÉSULTATS PAR PLATEFORME:")
        print("-" * 70)
        
        total_offers = 0
        for platform_name, offers in results.items():
            count = len(offers) if offers else 0
            total_offers += count
            
            status = "✅" if count > 0 else "⚠️"
            print(f"{status} {platform_name.upper()}: {count} offres trouvées")
            
            # Afficher les 2 premières offres
            if offers and count > 0:
                for i, offer in enumerate(offers[:2], 1):
                    print(f"    {i}. {offer.get('title', 'N/A')} - {offer.get('company', 'N/A')}")
                if count > 2:
                    print(f"    ... et {count - 2} autres offres")
        
        print(f"\n🎯 TOTAL: {total_offers} offres trouvées sur {len(results)} plateformes")
        
        # 3. Afficher détails d'une offre
        if total_offers > 0:
            print("\n\n📄 ÉTAPE 3: Détails d'une offre exemple")
            print("-" * 70)
            
            # Prendre la première offre trouvée
            for platform_name, offers in results.items():
                if offers and len(offers) > 0:
                    offer = offers[0]
                    print(f"Plateforme: {platform_name.upper()}")
                    print(f"Titre: {offer.get('title', 'N/A')}")
                    print(f"Entreprise: {offer.get('company', 'N/A')}")
                    print(f"Localisation: {offer.get('location', 'N/A')}")
                    print(f"URL: {offer.get('url', 'N/A')}")
                    print(f"Source: {offer.get('source_platform', 'N/A')}")
                    print(f"Job Type: {offer.get('job_type', 'N/A')}")
                    print(f"Work Mode: {offer.get('work_mode', 'N/A')}")
                    description = offer.get('description', '')
                    if description:
                        print(f"Description: {description[:150]}...")
                    break
        
        # 4. Test avec "data-science"
        print("\n\n🌐 ÉTAPE 4: Test scraping avec 'data-science'")
        print("-" * 70)
        
        results2 = await scraping_service.scrape_all_platforms(
            keywords="data-science",
            location="Paris",
            limit_per_platform=3
        )
        
        total_data_science = 0
        for platform_name, offers in results2.items():
            count = len(offers) if offers else 0
            total_data_science += count
            status = "✅" if count > 0 else "⚠️"
            print(f"{status} {platform_name.upper()}: {count} offres 'data-science'")
        
        print(f"\n🎯 TOTAL: {total_data_science} offres data-science trouvées")
        
        # 5. Conclusion
        print("\n\n" + "="*70)
        print("✅ CONCLUSION")
        print("="*70)
        
        if total_offers > 0:
            print("✅ Le scraping fonctionne!")
            print(f"✅ {len(enabled_platforms)} plateformes testées")
            print(f"✅ {total_offers} offres trouvées pour 'Python Developer'")
            print(f"✅ {total_data_science} offres trouvées pour 'data-science'")
            
            # Vérifier chaque plateforme
            for platform_name in enabled_platforms.keys():
                if platform_name in results and results[platform_name]:
                    print(f"✅ {platform_name}: OPÉRATIONNEL")
                else:
                    print(f"⚠️ {platform_name}: PAS DE RÉSULTATS")
        else:
            print("❌ Le scraping ne fonctionne pas correctement")
            print("❌ Aucune offre trouvée")
        
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERREUR lors du scraping: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n🚀 Lancement du test de scraping...")
    asyncio.run(test_scraping())
