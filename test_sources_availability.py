#!/usr/bin/env python3
"""
Script de test rapide pour vérifier la disponibilité des 30 sources
"""
import requests
import time
from typing import Dict, List

# 30 sources à tester
SOURCES = [
    # Agrégateurs
    {"name": "Indeed France", "url": "https://fr.indeed.com/jobs?q=developer&l=Paris", "type": "aggregator"},
    {"name": "RemoteOK", "url": "https://remoteok.com/api", "type": "aggregator"},
    {"name": "Welcome to the Jungle", "url": "https://www.welcometothejungle.com/fr/jobs", "type": "aggregator"},
    {"name": "LinkedIn Jobs", "url": "https://www.linkedin.com/jobs/search", "type": "aggregator"},
    
    # Tech & Consulting
    {"name": "Capgemini", "url": "https://www.capgemini.com/fr-fr/carrieres/", "type": "company"},
    {"name": "Atos", "url": "https://atos.net/fr/france/carrieres", "type": "company"},
    {"name": "Sopra Steria", "url": "https://www.soprasteria.com/fr/carrieres", "type": "company"},
    {"name": "Dassault Systèmes", "url": "https://careers.3ds.com/", "type": "company"},
    
    # Aéronautique & Défense
    {"name": "Airbus", "url": "https://www.airbus.com/en/careers", "type": "company"},
    {"name": "Safran", "url": "https://www.safran-group.com/fr/offres", "type": "company"},
    {"name": "Thales", "url": "https://www.thalesgroup.com/fr/carrieres", "type": "company"},
    {"name": "Dassault Aviation", "url": "https://www.dassault-aviation.com/fr/groupe/carrieres/", "type": "company"},
    
    # Énergie & Industrie
    {"name": "TotalEnergies", "url": "https://www.totalenergies.com/fr/carrieres", "type": "company"},
    {"name": "EDF", "url": "https://www.edf.fr/edf-recrute", "type": "company"},
    {"name": "Engie", "url": "https://www.engie.com/rejoignez-nous", "type": "company"},
    {"name": "Schneider Electric", "url": "https://www.se.com/fr/fr/about-us/careers/", "type": "company"},
    
    # Automobile
    {"name": "Renault", "url": "https://www.renaultgroup.com/talents/", "type": "company"},
    {"name": "Stellantis", "url": "https://www.stellantis.com/en/careers", "type": "company"},
    {"name": "Michelin", "url": "https://career.michelin.com/", "type": "company"},
    
    # Luxe & Retail
    {"name": "LVMH", "url": "https://www.lvmh.fr/talents/", "type": "company"},
    {"name": "L'Oréal", "url": "https://careers.loreal.com/", "type": "company"},
    {"name": "Hermès", "url": "https://careers.hermes.com/", "type": "company"},
    {"name": "Carrefour", "url": "https://www.carrefour.com/fr/rejoignez-nous", "type": "company"},
    
    # Banque & Finance
    {"name": "BNP Paribas", "url": "https://group.bnpparibas/emploi-carriere", "type": "company"},
    {"name": "Société Générale", "url": "https://careers.societegenerale.com/", "type": "company"},
    {"name": "Crédit Agricole", "url": "https://www.credit-agricole.com/nous-rejoindre", "type": "company"},
    
    # Télécoms
    {"name": "Orange", "url": "https://orange.jobs/", "type": "company"},
    {"name": "Bouygues Telecom", "url": "https://www.bouyguestelecom.fr/recrutement", "type": "company"},
    
    # Transport
    {"name": "SNCF", "url": "https://www.sncf.com/fr/groupe/rejoindre-sncf", "type": "company"},
    {"name": "Air France-KLM", "url": "https://www.airfranceklm.com/fr/carriere", "type": "company"},
]

def test_source(source: Dict) -> Dict:
    """Test si une source est accessible"""
    result = {
        "name": source["name"],
        "url": source["url"],
        "type": source["type"],
        "status": "unknown",
        "response_time": None,
        "status_code": None,
        "error": None,
        "scrapable": False,
        "notes": ""
    }
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        start = time.time()
        response = requests.get(source["url"], headers=headers, timeout=10, allow_redirects=True)
        response_time = time.time() - start
        
        result["response_time"] = round(response_time, 2)
        result["status_code"] = response.status_code
        
        if response.status_code == 200:
            result["status"] = "✅ OK"
            result["scrapable"] = True
            
            # Vérifier si c'est du HTML
            content_type = response.headers.get('Content-Type', '')
            if 'text/html' in content_type:
                result["notes"] = "HTML page"
            elif 'application/json' in content_type:
                result["notes"] = "JSON API"
            else:
                result["notes"] = f"Content-Type: {content_type}"
                
        elif response.status_code == 403:
            result["status"] = "⚠️ BLOQUÉ (403)"
            result["notes"] = "Besoin de bypass (Playwright/proxy)"
            
        elif response.status_code == 404:
            result["status"] = "❌ 404"
            result["notes"] = "URL invalide ou changée"
            
        elif response.status_code in [301, 302, 307, 308]:
            result["status"] = "🔄 REDIRECT"
            result["notes"] = f"Redirige vers {response.url}"
            
        else:
            result["status"] = f"⚠️ {response.status_code}"
            result["notes"] = "Code inhabituel"
            
    except requests.exceptions.Timeout:
        result["status"] = "⏱️ TIMEOUT"
        result["error"] = "Timeout après 10s"
        
    except requests.exceptions.SSLError as e:
        result["status"] = "🔒 SSL ERROR"
        result["error"] = str(e)[:100]
        
    except requests.exceptions.ConnectionError:
        result["status"] = "🔌 CONNECTION ERROR"
        result["error"] = "Impossible de se connecter"
        
    except Exception as e:
        result["status"] = "❌ ERROR"
        result["error"] = str(e)[:100]
    
    return result


def main():
    print("\n" + "="*80)
    print("🔍 TEST DE DISPONIBILITÉ DES 30 SOURCES")
    print("="*80 + "\n")
    
    results = []
    
    for i, source in enumerate(SOURCES, 1):
        print(f"[{i}/30] Testing {source['name']}...", end=" ", flush=True)
        result = test_source(source)
        results.append(result)
        print(f"{result['status']} ({result.get('response_time', '?')}s)")
        time.sleep(0.5)  # Petite pause pour éviter rate limiting
    
    # Statistiques
    print("\n" + "="*80)
    print("📊 RÉSULTATS")
    print("="*80 + "\n")
    
    ok_count = sum(1 for r in results if r['scrapable'])
    blocked_count = sum(1 for r in results if '403' in r['status'])
    error_count = sum(1 for r in results if r['status'].startswith('❌'))
    
    print(f"✅ Accessibles: {ok_count}/{len(SOURCES)} ({ok_count*100//len(SOURCES)}%)")
    print(f"⚠️ Bloquées (403): {blocked_count}/{len(SOURCES)}")
    print(f"❌ Erreurs: {error_count}/{len(SOURCES)}")
    
    # Détails par catégorie
    print("\n" + "-"*80)
    print("DÉTAILS PAR CATÉGORIE")
    print("-"*80 + "\n")
    
    aggregators = [r for r in results if r['type'] == 'aggregator']
    companies = [r for r in results if r['type'] == 'company']
    
    print(f"🌐 AGRÉGATEURS ({len(aggregators)}):")
    for r in aggregators:
        print(f"  • {r['name']:25} {r['status']:20} {r['notes']}")
    
    print(f"\n🏢 ENTREPRISES ({len(companies)}):")
    for r in companies:
        print(f"  • {r['name']:25} {r['status']:20} {r['notes']}")
    
    # Sources problématiques
    problematic = [r for r in results if not r['scrapable']]
    if problematic:
        print("\n" + "-"*80)
        print("⚠️ SOURCES PROBLÉMATIQUES (nécessitent attention)")
        print("-"*80 + "\n")
        for r in problematic:
            print(f"  • {r['name']}")
            print(f"    URL: {r['url']}")
            print(f"    Problème: {r['status']} - {r.get('error', r.get('notes', ''))}")
            print()
    
    # Recommandations
    print("\n" + "="*80)
    print("💡 RECOMMANDATIONS")
    print("="*80 + "\n")
    
    if ok_count >= 15:
        print("✅ Faisabilité EXCELLENTE : Suffisamment de sources accessibles")
        print(f"   → {ok_count} sources prêtes immédiatement")
        print(f"   → {blocked_count} sources nécessitent Playwright/proxy")
    elif ok_count >= 10:
        print("⚠️ Faisabilité MOYENNE : Certaines sources posent problème")
        print(f"   → {ok_count} sources prêtes")
        print(f"   → Besoin d'optimiser les {len(SOURCES) - ok_count} autres")
    else:
        print("❌ Faisabilité FAIBLE : Beaucoup de sources inaccessibles")
        print("   → Revoir la liste ou stratégie de scraping")
    
    print("\n📝 Prochaines étapes:")
    print("  1. Pour les sources bloquées (403) : Utiliser Playwright avec rotation IP")
    print("  2. Pour les 404/erreurs : Vérifier URLs ou retirer de la liste")
    print("  3. Pour les accessibles : Implémenter scrapers spécifiques")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
