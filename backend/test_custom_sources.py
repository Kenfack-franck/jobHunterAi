"""
Test des endpoints Custom Sources
"""
import asyncio
import httpx
import json


BASE_URL = "http://localhost:8000/api/v1"
TOKEN = None  # Sera rempli après login


async def login():
    """Connexion pour obtenir le token."""
    global TOKEN
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/auth/login",
            json={"email": "test@example.com", "password": "password123"}
        )
        if response.status_code == 200:
            TOKEN = response.json()["access_token"]
            print(f"✅ Login OK - Token: {TOKEN[:20]}...")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(response.text)


async def test_url_analysis():
    """Test de l'analyse d'URL sans l'ajouter."""
    print("\n" + "="*60)
    print("TEST 1: Analyse URL (Google Careers)")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{BASE_URL}/sources/custom/test",
            params={"url": "https://careers.google.com"},
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        if response.status_code == 200:
            print(f"\n✅ Analyse: {data['message']}")
            print(f"   Scrapable: {data['analysis']['is_scrapable']}")
            print(f"   Jobs trouvés: {data['analysis']['has_jobs']}")
            print(f"   Anti-bot: {data['analysis']['has_anti_bot']}")
        else:
            print(f"\n❌ Échec: {data}")


async def test_add_source():
    """Test d'ajout d'une source."""
    print("\n" + "="*60)
    print("TEST 2: Ajout d'une source custom")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{BASE_URL}/sources/custom",
            json={
                "source_name": "Google Careers",
                "source_url": "https://careers.google.com",
                "scraping_frequency": "every_4_hours"
            },
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        if response.status_code == 201:
            print(f"\n✅ Source ajoutée: ID {data['id']}")
            print(f"   Type détecté: {data['source_type']}")
            print(f"   Active: {data['is_active']}")
            if data.get('analysis'):
                print(f"   Recommandation: {data['analysis']['recommendation']}")
            return data['id']
        else:
            print(f"\n❌ Échec: {data}")
            return None


async def test_list_sources():
    """Test de listing des sources."""
    print("\n" + "="*60)
    print("TEST 3: Liste des sources")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/sources/custom",
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        if response.status_code == 200:
            print(f"\n✅ {data['total']} source(s) trouvée(s)")
            for src in data['sources']:
                print(f"   - [{src['id']}] {src['source_name']} ({src['source_url']})")
        else:
            print(f"\n❌ Échec: {data}")


async def test_update_source(source_id: int):
    """Test de mise à jour d'une source."""
    print("\n" + "="*60)
    print(f"TEST 4: Mise à jour source #{source_id}")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.patch(
            f"{BASE_URL}/sources/custom/{source_id}",
            json={
                "source_name": "Google Careers (Updated)",
                "is_active": False
            },
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        if response.status_code == 200:
            print(f"\n✅ Source mise à jour")
            print(f"   Nouveau nom: {data['source_name']}")
            print(f"   Active: {data['is_active']}")
        else:
            print(f"\n❌ Échec: {data}")


async def test_delete_source(source_id: int):
    """Test de suppression d'une source."""
    print("\n" + "="*60)
    print(f"TEST 5: Suppression source #{source_id}")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.delete(
            f"{BASE_URL}/sources/custom/{source_id}",
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        if response.status_code == 200:
            print(f"\n✅ {data['message']}")
        else:
            print(f"\n❌ Échec: {data}")


async def main():
    """Exécute tous les tests."""
    print("\n" + "█"*60)
    print("█  TEST CUSTOM SOURCES API")
    print("█"*60)
    
    # Login
    await login()
    if not TOKEN:
        print("\n❌ Impossible de continuer sans token")
        return
    
    # Tests
    await test_url_analysis()
    
    source_id = await test_add_source()
    
    await test_list_sources()
    
    if source_id:
        await test_update_source(source_id)
        await test_delete_source(source_id)
    
    # Vérification finale
    await test_list_sources()
    
    print("\n" + "█"*60)
    print("█  FIN DES TESTS")
    print("█"*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
