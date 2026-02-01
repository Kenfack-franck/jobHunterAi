# Configuration des Scrapers API

## ✅ Sources actives

### 1. RemoteOK ✅
- **Type** : API publique gratuite
- **Configuration** : Aucune clé requise
- **Statut** : Fonctionnel
- **Offres** : ~20-50 par recherche (100% remote)

### 2. The Muse ✅
- **Type** : API publique gratuite
- **Configuration** : Aucune clé requise
- **Statut** : Fonctionnel
- **Offres** : ~20-100 par recherche (tech/startups)

### 3. JSearch (LinkedIn + Indeed + Glassdoor) 📋
- **Type** : API RapidAPI (gratuit + payant)
- **Configuration** : Clé RapidAPI requise
- **Statut** : Prêt (nécessite clé)
- **Offres** : ~50-500 par recherche (agrégateur global)

### 4. Adzuna ⚠️
- **Type** : API gratuite avec inscription
- **Configuration** : Clés API requises
- **Statut** : Prêt (nécessite clés)
- **Offres** : ~50-200 par recherche (France)

---

## 🔧 Configuration JSearch (LinkedIn + Indeed + Glassdoor)

JSearch est un **agrégateur** qui vous donne accès à LinkedIn, Indeed, Glassdoor et ZipRecruiter via une seule API sécurisée.

### Étape 1 : Créer un compte RapidAPI
1. Aller sur https://rapidapi.com/auth/sign-up
2. Créer un compte gratuit (email + mot de passe)
3. Vérifier l'email

### Étape 2 : S'abonner à JSearch API
1. Aller sur https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
2. Cliquer sur **"Subscribe to Test"**
3. Choisir le plan :
   - **Basic (Gratuit)** : 100 requêtes/mois
   - **Pro ($10/mois)** : 1000 requêtes/mois
   - **Ultra ($20/mois)** : 5000 requêtes/mois

### Étape 3 : Obtenir la clé API
1. Sur la page JSearch, cliquer sur **"Code Snippets"**
2. Dans les headers, copier la valeur de `X-RapidAPI-Key`
   ```
   X-RapidAPI-Key: abc123xyz789... (votre clé)
   ```

### Étape 4 : Configurer le backend

**Option A : Variable d'environnement (Recommandé)**

Éditer `docker-compose.yml` :
```yaml
backend:
  environment:
    - RAPIDAPI_KEY=votre_cle_ici
```

**Option B : Fichier scraper**

Éditer `backend/app/services/scrapers/jsearch_scraper.py` :
```python
# Ligne 23
self.api_key = os.getenv("RAPIDAPI_KEY", "votre_cle_ici")
```

### Étape 5 : Activer JSearch

Éditer `backend/app/platforms_config/platforms.py` :
```python
"jsearch": {"name": "JSearch", "enabled": True},
```

### Étape 6 : Redémarrer le backend
```bash
docker compose restart backend
```

---

## 🔧 Obtenir les clés Adzuna (optionnel)

Adzuna est **désactivé par défaut**. Pour l'activer :

### Étape 1 : Créer un compte
1. Aller sur https://developer.adzuna.com/signup
2. Créer un compte gratuit
3. Confirmer l'email

### Étape 2 : Obtenir les clés
1. Se connecter sur https://developer.adzuna.com/admin/applications
2. Créer une nouvelle application
3. Noter **APP_ID** et **APP_KEY**

### Étape 3 : Configurer le backend
Éditer `backend/app/services/scrapers/adzuna_scraper.py` :

```python
# Ligne 17-18
self.app_id = "VOTRE_APP_ID"
self.app_key = "VOTRE_APP_KEY"
```

Ou mieux, via variables d'environnement (Docker) :
```yaml
# docker-compose.yml
backend:
  environment:
    - ADZUNA_APP_ID=votre_app_id
    - ADZUNA_APP_KEY=votre_app_key
```

Puis dans `adzuna_scraper.py` :
```python
import os
self.app_id = os.getenv("ADZUNA_APP_ID", "test")
self.app_key = os.getenv("ADZUNA_APP_KEY", "test")
```

### Étape 4 : Activer Adzuna
```python
# platforms.py
"adzuna": {"enabled": True}
```

### Étape 5 : Redémarrer le backend
```bash
docker compose restart backend
```

---

## 📊 Résultats attendus

| Source | Offres France | Offres Remote | Tech | Stages | Gratuit |
|--------|---------------|---------------|------|--------|---------|
| RemoteOK | ❌ | ✅ (100%) | ✅ | ⚠️ | ✅ |
| The Muse | ⚠️ | ✅ (40%) | ✅ | ⚠️ | ✅ |
| **JSearch** | ✅ | ✅ (30%) | ✅ | ✅ | ✅ (100 req/mois) |
| Adzuna | ✅ | ⚠️ | ⚠️ | ✅ | ✅ (1000 req/mois) |

**Combinaison recommandée** :
- **Remote Tech** → RemoteOK + The Muse + JSearch (LinkedIn)
- **Paris + Tech** → JSearch (LinkedIn + Indeed) + Adzuna
- **Stage France** → Adzuna + JSearch

**Avec JSearch activé** :
- **100-500 offres** par recherche (au lieu de 40-100)
- Accès à LinkedIn, Indeed, Glassdoor
- Pas de risque de ban
- Légal et sécurisé

---

## 🚀 Test rapide

Une fois les clés configurées :

```bash
# Tester JSearch (LinkedIn + Indeed + Glassdoor)
docker compose exec backend python -c "
import asyncio
from app.services.scrapers.jsearch_scraper import JSearchScraper

async def test():
    scraper = JSearchScraper()
    offers = await scraper.scrape(keywords='Python Developer', location='Remote', max_results=10)
    print(f'JSearch: {len(offers)} offres')
    if offers:
        for i, offer in enumerate(offers[:3], 1):
            print(f'{i}. {offer[\"title\"]} - {offer[\"company\"]} (Source: {offer.get(\"original_source\", \"N/A\")})')

asyncio.run(test())
"

# Tester Adzuna
docker compose exec backend python -c "
import asyncio
from app.services.scrapers.adzuna_scraper import AdzunaScraper

async def test():
    scraper = AdzunaScraper()
    offers = await scraper.scrape(keywords='Python', location='Paris', max_results=5)
    print(f'Adzuna: {len(offers)} offres')

asyncio.run(test())
"

# Tester The Muse
docker compose exec backend python -c "
import asyncio
from app.services.scrapers.themuse_scraper import TheMuseScraper

async def test():
    scraper = TheMuseScraper()
    offers = await scraper.scrape(keywords='developer', location='remote', max_results=5)
    print(f'The Muse: {len(offers)} offres')

asyncio.run(test())
"
```

---

## 💰 Tarification JSearch (LinkedIn + Indeed)

| Plan | Prix | Requêtes/mois | Coût/recherche |
|------|------|---------------|----------------|
| **Basic** | Gratuit | 100 | €0 |
| **Pro** | $10/mois | 1000 | €0.01 |
| **Ultra** | $20/mois | 5000 | €0.004 |

**Pour un MVP** : Plan gratuit (100 req) = suffisant pour tester  
**Pour production** : Plan Pro ($10/mois) = ~30 recherches/jour

---

## 📝 Notes

- **Sans JSearch/Adzuna** : ~40-70 offres par recherche (RemoteOK + The Muse)
- **Avec JSearch** : ~100-500 offres par recherche (LinkedIn + Indeed + Glassdoor)
- **Avec tous activés** : ~200-700 offres par recherche

JSearch est particulièrement utile pour :
- ✅ **LinkedIn** (impossible à scraper autrement)
- ✅ **Indeed** (anti-bot très agressif)
- ✅ **Glassdoor** (API privée)
- ✅ **Recherches locales** (Paris, Lyon, etc.)

