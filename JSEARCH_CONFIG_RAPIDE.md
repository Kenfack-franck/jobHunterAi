# 🚀 PRÊT À TESTER - Configuration JSearch

## ✅ Ce qui fonctionne maintenant

1. **JSearch est activé** dans le système
2. **15 entreprises mappées** vers JSearch API
3. **Limité à 3 offres** par entreprise (pour les tests)
4. **Le code appelle correctement** JSearch avec filtre company

## ⚠️ Ce qu'il manque : LA CLÉ API

Le système affiche :
```
[JSearch] ⚠️ Clé API non configurée. Voir SCRAPERS_CONFIG.md
```

---

## 🎯 ÉTAPES RAPIDES (10 minutes)

### 1. Obtenir la clé API (5 min)

1. **Aller sur** : https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
2. **Se connecter** ou créer un compte (gratuit)
3. **Cliquer** sur "Subscribe to Test"
4. **Choisir** le plan **"Basic" - FREE** (100 requêtes/mois)
5. **Copier** votre clé : `X-RapidAPI-Key: 1234567890abcdef...`

### 2. Configurer la clé (2 min)

**Créer ou éditer** `.env` à la racine du projet :

```bash
# .env
RAPIDAPI_KEY=votre_cle_copiee_ici_1234567890
```

**OU modifier** `docker-compose.yml` (ligne 46, section backend) :

```yaml
backend:
  environment:
    RAPIDAPI_KEY: "votre_cle_copiee_ici_1234567890"
    DATABASE_URL: postgresql+asyncpg://...
    ...
```

### 3. Redémarrer le backend (1 min)

```bash
docker compose restart backend
```

### 4. Tester (2 min)

```bash
# Tester Capgemini
docker compose exec backend python /app/test_sources.py capgemini Python

# Tester vos 4 entreprises sélectionnées
docker compose exec backend python /app/test_sources.py user
```

**Résultat attendu** :
```
[JSearch] 🔍 Début scraping: keywords=Python, company=Capgemini
[JSearch] 📡 API: 3 offres récupérées
✅ capgemini: 3 offres

📦 Exemples d'offres:
  1. Python Developer - Capgemini
     📍 Paris
  2. Backend Engineer - Capgemini
     📍 Lyon
```

---

## 📊 Test depuis l'interface web

### Se connecter
- **Email**: `kenfackfranck08@gmail.com`
- **Password**: `noumedem`

### Tester la recherche
1. **Aller sur** : http://localhost:3000/jobs
2. **Rechercher** : "Python" ou "Développeur"
3. **Voir les résultats** :
   - Capgemini (3 offres)
   - Sopra Steria (3 offres)
   - Dassault Systèmes (3 offres)
   - L'Oréal (3 offres)

---

## 📝 Rappel de vos préférences actuelles

Vous avez déjà sélectionné (sauvegardé en BDD) :
- ☑️ Capgemini
- ☑️ Sopra Steria
- ☑️ Dassault Systèmes
- ☑️ L'Oréal

**Ces 4 sources seront automatiquement utilisées** lors de votre recherche.

---

## 🐛 Vérifications si problème

### La clé est-elle bien configurée ?

```bash
# Vérifier la variable d'environnement
docker compose exec backend printenv | grep RAPID

# Devrait afficher:
# RAPIDAPI_KEY=1234567890abcdef...
```

### Tester une requête API directement

```bash
docker compose exec backend python -c "
from app.services.scrapers.jsearch_scraper import JSearchScraper
import asyncio
scraper = JSearchScraper()
result = asyncio.run(scraper.scrape('Python', company='Capgemini', max_results=3))
print(f'Résultats: {len(result)} offres')
"
```

---

## 🎉 Si ça fonctionne

### Augmenter la limite

Une fois les tests OK, vous pouvez augmenter :

```python
# backend/app/services/scrapers/jsearch_scraper.py
# Ligne 33
self.max_offers = 10  # Au lieu de 3
```

### Monitorer l'usage API

- Dashboard RapidAPI : https://rapidapi.com/developer/dashboard
- Section "Usage" pour voir les requêtes consommées

---

## 💡 Limites du plan gratuit

- **100 requêtes/mois** gratuites
- **1 recherche = 4 requêtes** (1 par entreprise sélectionnée)
- **Avec cache 24h** : ~25 recherches différentes/mois

Si besoin de plus :
- **$10/mois** = 1000 requêtes
- **$25/mois** = 5000 requêtes

---

## 📖 Guide complet

Consultez **GUIDE_JSEARCH_RAPIDAPI.md** pour plus de détails.

---

## ✅ Checklist rapide

- [ ] Clé API obtenue sur RapidAPI.com
- [ ] `RAPIDAPI_KEY` ajouté dans `.env` ou `docker-compose.yml`
- [ ] Backend redémarré
- [ ] Test script : `python /app/test_sources.py user`
- [ ] Test interface web : http://localhost:3000/jobs
- [ ] Résultats affichés (3 offres par entreprise)

**Temps estimé : 10 minutes** ⏱️
