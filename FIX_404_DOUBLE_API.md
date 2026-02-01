# 🔧 Fix: Erreur 404 Double /api/v1

## 🐛 Problème

**Symptôme**: Erreur 404 lors de la recherche d'offres  
**URL incorrecte**: `http://localhost:8000/api/v1/api/v1/jobs/search`  
**URL correcte**: `http://localhost:8000/api/v1/jobs/search`

### Cause Root

Double préfixe `/api/v1` dans les URLs:
- Variable d'environnement: `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1`
- Code: `${API_URL}/api/v1/jobs/search`
- Résultat: `/api/v1/api/v1/jobs/search` ❌

---

## ✅ Solution Appliquée

### Principe
Utiliser `NEXT_PUBLIC_API_URL` comme base **avec** `/api/v1`, et supprimer `/api/v1` de tous les appels.

### Avant
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
// ...
const response = await axios.get(`${API_URL}/api/v1/jobs/search`);
// → http://localhost:8000/api/v1/api/v1/jobs/search ❌
```

### Après
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
// ...
const response = await axios.get(`${API_URL}/jobs/search`);
// → http://localhost:8000/api/v1/jobs/search ✅
```

---

## 📁 Fichiers Modifiés

### 1. `/frontend/src/lib/jobOffer.ts`
**Changements**:
- ✅ `API_URL` par défaut: `http://localhost:8000/api/v1`
- ✅ Tous les endpoints: `/jobs` au lieu de `/api/v1/jobs`

**Endpoints corrigés**:
- `GET /jobs` (liste)
- `GET /jobs/search` (recherche)
- `GET /jobs/:id` (détails)
- `POST /jobs` (création)
- `PUT /jobs/:id` (mise à jour)
- `DELETE /jobs/:id` (suppression)
- `GET /jobs/stats/count` (statistiques)
- `POST /jobs/search/async` (recherche async)
- `GET /jobs/search/status/:id` (statut async)

### 2. `/frontend/src/lib/documents.ts`
**Changements**:
- ✅ `API_URL` par défaut: `http://localhost:8000/api/v1`
- ✅ Endpoints: `/documents/*` au lieu de `/api/v1/documents/*`

### 3. `/frontend/src/lib/analysis.ts`
**Changements**:
- ✅ `API_URL` par défaut: `http://localhost:8000/api/v1`
- ✅ Endpoints: `/analysis/*` au lieu de `/api/v1/analysis/*`

### 4. `/frontend/src/lib/api.ts`
**Status**: ✅ Déjà correct (utilisait déjà le bon pattern)

---

## 🧪 Tests Effectués

### Test 1: Recherche d'offres
```bash
GET /api/v1/jobs/search?keyword=Python&location=Paris
✅ Résultat: 2 offres trouvées
```

### Test 2: Vérification des URLs
```bash
# Avant le fix
❌ /api/v1/api/v1/jobs/search → 404 Not Found

# Après le fix
✅ /api/v1/jobs/search → 200 OK
```

---

## 🎯 Résultat

**La recherche d'offres fonctionne maintenant!**

### Testez Maintenant
1. Allez sur http://localhost:3000/jobs
2. Entrez: `Python` + `Paris`
3. Cliquez "Rechercher"
4. **Attendu**: 
   - 🔵 Spinner "Recherche en cours..."
   - ✅ "2 offres trouvées"
   - Liste des 2 offres affichée

---

## 📝 Leçons Apprises

### ❌ Pattern Incorrect
```typescript
// Variable d'env avec /api/v1
const API_URL = 'http://localhost:8000/api/v1';
// Code qui ajoute aussi /api/v1
fetch(`${API_URL}/api/v1/jobs`);
// → Double préfixe!
```

### ✅ Pattern Correct
```typescript
// Variable d'env avec /api/v1
const API_URL = 'http://localhost:8000/api/v1';
// Code sans /api/v1
fetch(`${API_URL}/jobs`);
// → URL correcte!
```

### Règle d'Or
**Choisir UN seul endroit pour le préfixe `/api/v1`**:
- ✅ Option A: Dans la variable d'environnement (choisi)
- ✅ Option B: Dans chaque appel API
- ❌ Jamais les deux en même temps!

---

## 🔍 Comment Détecter ce Bug

### Signes
- Erreur 404 sur les appels API
- URL dans les logs avec double préfixe
- Pattern `/api/v1/api/v1/` visible

### Debug
```bash
# Voir les URLs appelées dans le navigateur
F12 → Network → Filter: XHR → Observer les URLs
```

---

**Date**: 2026-01-31 19:09  
**Status**: ✅ Corrigé et testé  
**Impact**: Critique → La recherche ne fonctionnait pas
