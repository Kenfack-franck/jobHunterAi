# Fix Page Recherche - Adaptation au Système Multi-Sources Adzuna

**Date**: 2026-02-03  
**Problème**: Page de recherche retourne 0 offres

---

## 🐛 Problème: Confusion location / work_mode

Le formulaire envoyait `location="onsite"` au lieu d'une vraie ville, ce qu'Adzuna ne comprend pas.

---

## ✅ Solution

### Fichier : `frontend/src/components/jobs/SearchBar.tsx`

**Avant** :
```typescript
// ❌ Work mode dans location
let location = workMode || city;  // Confus !
```

**Après** :
```typescript
// ✅ Séparation propre
const location = city || undefined;      // "Paris", "France"
const work_mode = workMode || undefined; // "remote", "onsite"
```

---

## 🧪 Comment tester

### Test rapide
1. http://localhost:3000/jobs
2. Intitulé : **"Développeur"** ou **"Cloud"**
3. Ville : Laisser vide
4. Cliquer "Rechercher"

**Résultat attendu** : 10-20 offres par source

### Meilleurs mots-clés
- **Développeur** → 7-17 offres/entreprise
- **Cloud** → 20 offres Capgemini, 19 Sopra, 8 Dassault
- **Data** → 18 Capgemini, 20 Sopra
- **Ingénieur** → 19 Capgemini, 7 L'Oréal

---

## 💡 Recommandations

### Localisation
- **Laisser vide** = Tous les résultats (meilleur)
- **Paris, France** = Résultats filtrés
- **❌ PAS "Présentiel" ou "Remote"** = Ce sont des modes de travail

### Mode de travail
- **Télétravail** = Plus de résultats
- Filtré après le scraping, pas envoyé à Adzuna

---

**Status** : ✅ Corrigé et redémarré  
**Action** : Recharger http://localhost:3000/jobs et tester avec "Développeur"
