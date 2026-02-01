# 🔑 Guide : Obtenir une clé JSearch (LinkedIn + Indeed + Glassdoor)

## 🎯 Pourquoi JSearch ?

JSearch vous donne accès à **LinkedIn, Indeed et Glassdoor** de manière **légale et sécurisée** :
- ✅ Pas de scraping direct (pas de ban)
- ✅ Pas besoin de compte LinkedIn/Indeed
- ✅ API officielle et stable
- ✅ **Gratuit** : 100 recherches/mois

---

## 📋 Étapes (5 minutes)

### 1️⃣ Créer un compte RapidAPI

🔗 **Lien** : https://rapidapi.com/auth/sign-up

1. Cliquer sur **"Sign Up"**
2. Choisir :
   - Email + mot de passe
   - Ou connexion Google/GitHub
3. Vérifier l'email (cliquer sur le lien reçu)

✅ **Compte créé !**

---

### 2️⃣ S'abonner à JSearch API

🔗 **Lien** : https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch

1. Sur la page JSearch, cliquer sur **"Subscribe to Test"** (bouton bleu)
2. Choisir le plan **"Basic"** (gratuit)
   - 100 requêtes/mois
   - Pas de carte bancaire requise
3. Cliquer sur **"Subscribe"**

✅ **Abonné au plan gratuit !**

---

### 3️⃣ Copier la clé API

Sur la même page (JSearch API) :

1. Chercher la section **"Header Parameters"** (à droite)
2. Vous verrez :
   ```
   X-RapidAPI-Key: abc123def456...
   X-RapidAPI-Host: jsearch.p.rapidapi.com
   ```
3. **Copier** la valeur de `X-RapidAPI-Key` (longue chaîne de caractères)

✅ **Clé copiée !**

---

### 4️⃣ Configurer Job Hunter AI

**Option A : Via Docker (Recommandé)**

Éditer `docker-compose.yml` :
```yaml
backend:
  environment:
    - RAPIDAPI_KEY=abc123def456...  # Coller votre clé ici
```

Puis redémarrer :
```bash
docker compose restart backend
```

---

**Option B : Directement dans le code**

Éditer `backend/app/services/scrapers/jsearch_scraper.py` :
```python
# Ligne 23
self.api_key = os.getenv("RAPIDAPI_KEY", "abc123def456...")  # Coller votre clé
```

Puis copier dans le container :
```bash
docker cp backend/app/services/scrapers/jsearch_scraper.py jobhunter_backend:/app/app/services/scrapers/
docker compose restart backend
```

---

### 5️⃣ Activer JSearch

Éditer `backend/app/platforms_config/platforms.py` :
```python
"jsearch": {"name": "JSearch", "base_url": "https://jsearch.p.rapidapi.com", "enabled": True},
```

Puis copier :
```bash
docker cp backend/app/platforms_config/platforms.py jobhunter_backend:/app/app/platforms_config/
docker compose restart backend
```

✅ **JSearch activé !**

---

## 🧪 Tester

### Test Backend

```bash
docker compose exec backend python -c "
import asyncio
from app.services.scrapers.jsearch_scraper import JSearchScraper

async def test():
    scraper = JSearchScraper()
    offers = await scraper.scrape(keywords='python developer', location='remote', max_results=5)
    print(f'✅ JSearch: {len(offers)} offres trouvées')
    if offers:
        print('Exemple:')
        offer = offers[0]
        print(f'  - {offer[\"title\"]}')
        print(f'  - {offer[\"company\"]}')
        print(f'  - Source: {offer.get(\"original_source\", \"N/A\")}')

asyncio.run(test())
"
```

**Résultat attendu** :
```
✅ JSearch: 5 offres trouvées
Exemple:
  - Senior Python Developer
  - Google
  - Source: LinkedIn
```

---

### Test Frontend

1. Aller sur http://localhost:3000/jobs
2. Rechercher :
   - Intitulé : **python developer**
   - Mode : **Télétravail / Remote**
   - Type : **Fulltime**
3. Attendre 30-45 secondes
4. Vérifier :
   - ✅ Badges **🔍 JSearch** visibles
   - ✅ 50-100+ offres (au lieu de 20)
   - ✅ Sources variées : LinkedIn, Indeed, Glassdoor

---

## ❓ FAQ

### Combien ça coûte ?
- **Gratuit** : 100 requêtes/mois (plan Basic)
- **Pro** : $10/mois pour 1000 requêtes
- Pas de carte bancaire requise pour le plan gratuit

### Combien de recherches ça fait ?
- 1 recherche frontend = 1 requête API
- 100 req/mois = ~3 recherches/jour
- Suffisant pour tester et développer

### Que se passe-t-il si je dépasse 100 ?
- L'API retourne une erreur 429 (Too Many Requests)
- Les autres scrapers (RemoteOK, The Muse) continuent de fonctionner
- Vous pouvez upgrader au plan Pro ($10/mois)

### Quelles sources sont incluses ?
JSearch agrège :
- ✅ **LinkedIn** (impossible à scraper autrement)
- ✅ **Indeed** (anti-bot très agressif)
- ✅ **Glassdoor** (API privée)
- ✅ **ZipRecruiter**
- ✅ **CareerBuilder**

### C'est légal ?
✅ **Oui**, JSearch est une API officielle et légale. Contrairement au scraping direct, vous passez par un service autorisé.

---

## 🚀 Résultats attendus

**Avant JSearch** : 40-70 offres par recherche  
**Après JSearch** : **100-500 offres** par recherche

**Sources actives** :
- RemoteOK (~20-50 offres remote)
- The Muse (~20-100 offres tech)
- **JSearch (~50-400 offres LinkedIn + Indeed + Glassdoor)**

**Total** : **~100-500 offres** au lieu de 40 🎉

---

## 📝 Liens utiles

- **RapidAPI** : https://rapidapi.com
- **JSearch API** : https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
- **Documentation** : https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch/details
- **Dashboard** (voir usage) : https://rapidapi.com/developer/dashboard

---

**🎯 Une fois configuré, vous aurez accès à LinkedIn sans risque de ban !**
