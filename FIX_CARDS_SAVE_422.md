# Fix Sauvegarde + Affichage - 3 février 2026

## ❌ Problèmes résolus

1. **Erreur 422 sauvegarde** : Champ `job_title` manquant
2. **Badge "adzuna"** : Affichait source au lieu entreprise  
3. **"Invalid Date"** : Champ `created_at` manquant pour offres scrapées
4. **Déduplication cassée** : Cherchait `title`/`company`/`url` au lieu de champs normalisés

## ✅ Solutions

### Backend : 5 fichiers corrigés

**Fichier 1** : `backend/app/services/search_service.py` ligne 414
- Ajout `_normalize_offer_fields()` 
- Mapping : `title` → `job_title`, `company` → `company_name`, `url` → `source_url`

**Fichier 2** : `backend/app/api/routes/search.py` ligne 32-34 **← CRITIQUE**
- Fix : API retournait `o.get("title")` au lieu de `o.get("job_title")`
- Correction : `title=o.get("job_title")`, `company=o.get("company_name")`, `url=o.get("source_url")`

**Fichier 3** : `backend/app/services/search_service.py` ligne 492
- Fix vérification doublons DB : `JobOffer.title` → `JobOffer.job_title`

**Fichier 4** : `backend/app/services/search_service.py` ligne 348, 585
- Fix feed et conversion : `offer.title` → `offer.job_title`

**Fichier 5** : `backend/app/services/search_service.py` ligne 388-394 **← FIX DÉDUPLICATION**
- Fix déduplication : cherchait `"title"`/`"company"`/`"url"` au lieu de `"job_title"`/`"company_name"`/`"source_url"`
- **Impact énorme** : 250 → 1 offre AVANT, 250 → 163 offres APRÈS

### Frontend : Affichage
**Fichier** : `frontend/src/components/jobs/JobOfferCard.tsx`
- Badge : `source_platform` → `company_name`
- Dates : `posted_date || scraped_at || created_at`
- Type : Ajout champs optionnels `posted_date`, `scraped_at`

## 🎯 Résultats tests

### Avant corrections
- ❌ Erreur 422 sauvegarde
- ❌ 250 scrapées → 1 dédupliquée (0.4%)
- ❌ Badge "adzuna" au lieu entreprise
- ❌ "Invalid Date"

### Après corrections
- ✅ Sauvegarde fonctionne (201 Created)
- ✅ 250 scrapées → 163 dédupliquées (65%)
- ✅ Badge entreprise correct
- ✅ Dates valides
- ✅ Recherche "ingenieur" : 163 offres
- ✅ Recherche "stage ingénieur" + filtres : 87 stages

## 📝 Note critique

Le problème était **PARTOUT** dans le code :
1. Scrapers retournaient `title`/`company`/`url`
2. Search service normalisait EN MÉMOIRE mais...
3. API endpoint lisait les anciens champs
4. Déduplication cherchait les anciens champs
5. Sauvegarde DB vérifiait les anciens champs
6. Feed formatait avec les anciens champs

**Solution complète** : 
- Normaliser dans search_service.py
- Corriger TOUS les endroits lisant ces champs (5 fichiers, 8 emplacements)
