# Configuration JSearch pour Sources Multi-Entreprises

**Date**: 2026-02-03  
**Objectif**: Implémenter temporairement JSearch API pour les 15 entreprises non fonctionnelles

---

## 📊 Contexte

### Problème initial
- **17 sources sur 18** ne retournaient AUCUN résultat
- Utilisateur sélectionnait Capgemini, Sopra, Dassault, L'Oréal → 0 offres
- Seul RemoteOK fonctionnait

### Cause
- Les 15 entreprises mappées vers `None` dans le code
- Pas de scrapers implémentés pour les sites carrières

### Solution temporaire
- **JSearch API** (agrégateur LinkedIn, Indeed, Glassdoor)
- Filtre par nom d'entreprise : `company="Capgemini"`
- 100 requêtes/mois gratuites, limite à 3 offres pour tests

---

## ✅ Modifications effectuées

### 1. Mapping sources → JSearch

**Fichier**: `backend/app/services/scraping_service.py`

**Lignes 401-436** : Mapping mis à jour
```python
mapping = {
    # Agrégateurs (scrapers existants)
    "remoteok": "remoteok",           # ✅ Scraping direct
    "wttj": "welcometothejungle",     # À implémenter
    "linkedin": "jsearch",            # Via JSearch
    
    # 15 entreprises → JSearch
    "capgemini": "jsearch",
    "sopra_steria": "jsearch",
    "dassault_systemes": "jsearch",
    "airbus": "jsearch",
    "thales": "jsearch",
    "dassault_aviation": "jsearch",
    "safran": "jsearch",
    "totalenergies": "jsearch",
    "edf": "jsearch",
    "renault": "jsearch",
    "stellantis": "jsearch",
    "lvmh": "jsearch",
    "loreal": "jsearch",
    "bnp_paribas": "jsearch",
    "societe_generale": "jsearch",
    "orange": "jsearch",
}
```

---

### 2. Méthode de mapping nom entreprise

**Fichier**: `backend/app/services/scraping_service.py`

**Lignes 346-388** : Nouvelle méthode `_get_company_name()`
```python
def _get_company_name(self, source_id: str) -> Optional[str]:
    """
    Convertir source_id → nom entreprise pour JSearch
    Ex: "sopra_steria" → "Sopra Steria"
    """
    company_mapping = {
        "capgemini": "Capgemini",
        "sopra_steria": "Sopra Steria",
        "dassault_systemes": "Dassault Systemes",
        "airbus": "Airbus",
        "thales": "Thales",
        ...
    }
    return company_mapping.get(source_id)
```

---

### 3. Paramètre company dans scrape_platform

**Fichier**: `backend/app/services/scraping_service.py`

**Lignes 195-242** : Ajout du paramètre `company`
```python
async def scrape_platform(
    self,
    platform: str,
    keywords: str,
    location: str = "",
    limit: int = 100,
    company: Optional[str] = None  # ← NOUVEAU
) -> List[Dict]:
    # ...
    if platform == "jsearch" and company:
        print(f"[ScrapingService] 🏢 JSearch avec filtre company='{company}'")
        offers = await scraper.scrape(
            keywords=keywords,
            location=location if location else None,
            company=company,  # ← Passé à JSearch
            max_results=limit
        )
```

---

### 4. Utilisation dans scrape_priority_sources

**Fichier**: `backend/app/services/scraping_service.py`

**Lignes 276-342** : Extraction et passage du nom entreprise
```python
async def scrape_priority_sources(
    self,
    sources: List[Dict],
    keywords: str,
    location: str = ""
) -> Dict[str, List[Dict]]:
    results = {}
    
    for source in sources:
        source_id = source.get("id")
        platform = self._map_source_to_platform(source_id)
        
        if platform:
            # Extraire le nom de l'entreprise pour JSearch
            company = self._get_company_name(source_id)  # ← NOUVEAU
            
            offers = await self.scrape_platform(
                platform=platform,
                keywords=keywords,
                location=location,
                company=company  # ← Passé au scraper
            )
```

---

### 5. Limite d'offres pour tests

**Fichier**: `backend/app/services/scrapers/jsearch_scraper.py`

**Ligne 33** : Limite réduite à 3
```python
self.max_offers = 3  # LIMITE À 3 pour les tests (changeable ensuite)
```

**Avant** : `self.max_offers = 100`

---

### 6. Activation de JSearch dans platformes

**Fichier**: `backend/app/platforms_config/platforms.py`

**Ligne 9** : Activation du scraper
```python
"jsearch": {
    "name": "JSearch",
    "base_url": "https://jsearch.p.rapidapi.com",
    "enabled": True  # ← Changé de False à True
}
```

---

## 🧪 Tests effectués

### Test avec script diagnostic

```bash
docker compose exec backend python /app/test_sources.py capgemini Python
```

**Résultat** :
```
[ScrapingService] 🏢 JSearch avec filtre company='Capgemini'
[JSearch] ⚠️ Clé API non configurée. Voir SCRAPERS_CONFIG.md
✅ capgemini: 0 offres
```

**Conclusion** : 
- ✅ Mapping fonctionne (appelle JSearch)
- ✅ Filtre company passé correctement
- ⚠️ Besoin de la clé API RapidAPI pour obtenir des résultats

---

## 📋 État actuel

### Fonctionnel
- ✅ Mapping des 15 entreprises vers JSearch
- ✅ Extraction du nom d'entreprise depuis source_id
- ✅ Paramètre company passé au scraper
- ✅ Limite à 3 offres pour tests
- ✅ JSearch activé dans platformes

### En attente
- ⚠️ Configuration de `RAPIDAPI_KEY`
- ⚠️ Test avec vraie clé API
- ⚠️ Validation que JSearch retourne des offres pour entreprises françaises

---

## 📝 Prochaines étapes pour l'utilisateur

### 1. Obtenir la clé API (5 min)
1. Aller sur : https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
2. S'inscrire (gratuit)
3. S'abonner au plan "Basic" (100 req/mois gratuit)
4. Copier la clé : `X-RapidAPI-Key: ...`

### 2. Configurer (2 min)
Ajouter dans `.env` :
```bash
RAPIDAPI_KEY=votre_cle_ici
```

OU dans `docker-compose.yml` (ligne 46) :
```yaml
backend:
  environment:
    RAPIDAPI_KEY: "votre_cle_ici"
```

### 3. Redémarrer (1 min)
```bash
docker compose restart backend
```

### 4. Tester (2 min)
```bash
# Test automatique avec les 4 entreprises sélectionnées
docker compose exec backend python /app/test_sources.py user

# Test d'une entreprise spécifique
docker compose exec backend python /app/test_sources.py capgemini Python
```

**Résultat attendu** :
```
✅ capgemini: 3 offres
✅ sopra_steria: 3 offres
✅ dassault_systemes: 3 offres
✅ loreal: 3 offres
```

---

## 🎯 Architecture finale

```
User sélectionne:           Backend scraping:
┌─────────────────┐         ┌─────────────────────────┐
│ ☑️ Capgemini    │────────>│ JSearch(company="Cap") │
│ ☑️ Sopra Steria │────────>│ JSearch(company="Sop") │
│ ☑️ Dassault     │────────>│ JSearch(company="Das") │
│ ☑️ L'Oréal      │────────>│ JSearch(company="Lor") │
└─────────────────┘         └─────────────────────────┘
                                       │
                                       ▼
                            ┌──────────────────────────┐
                            │ JSearch API (RapidAPI)   │
                            │ Agrège: LinkedIn, Indeed,│
                            │ Glassdoor, ZipRecruiter  │
                            └──────────────────────────┘
                                       │
                                       ▼
                            ┌──────────────────────────┐
                            │  3 offres par entreprise │
                            │  Total: 12 offres        │
                            └──────────────────────────┘
```

---

## 💡 Limites connues

### Plan gratuit RapidAPI
- **100 requêtes/mois** gratuites
- **1 recherche = 4 requêtes** (4 entreprises sélectionnées)
- **Maximum : ~25 recherches/mois**

### Cache Redis (optimisation)
- **TTL 24h** sur les résultats
- Même recherche dans les 24h = **0 requête API** (cache)
- Économise les requêtes API

### JSearch vs Scraping direct
- ✅ **Avantage** : Résultats instantanés, pas de maintenance scrapers
- ⚠️ **Inconvénient** : Pas d'accès direct aux sites carrières
- ⚠️ **Limitation** : Dépend de LinkedIn/Indeed/Glassdoor
- 🔮 **Future** : Implémenter scrapers directs en Phase 2

---

## 📖 Documentation créée

1. **GUIDE_JSEARCH_RAPIDAPI.md** - Guide complet détaillé
2. **JSEARCH_CONFIG_RAPIDE.md** - Instructions rapides (10 min)
3. **JSEARCH_IMPLEMENTATION_STATUS.md** - Ce document (status technique)

---

## ✅ Checklist de validation

- [x] Mapping sources → jsearch implémenté
- [x] Méthode `_get_company_name()` créée
- [x] Paramètre `company` ajouté à `scrape_platform()`
- [x] Passage du company dans `scrape_priority_sources()`
- [x] Limite à 3 offres configurée
- [x] JSearch activé dans platformes
- [x] Test avec script diagnostic OK (appelle JSearch)
- [ ] **EN ATTENTE** : Clé API RapidAPI
- [ ] **EN ATTENTE** : Test avec vraies offres
- [ ] **EN ATTENTE** : Validation interface web

---

## 🚀 Prêt pour tests

**Le code est prêt**. Il suffit maintenant de :
1. Obtenir la clé API (5 min)
2. Configurer la variable d'environnement (2 min)
3. Redémarrer le backend (1 min)
4. Tester (2 min)

**Temps total : 10 minutes** ⏱️

Voir **JSEARCH_CONFIG_RAPIDE.md** pour les instructions.
