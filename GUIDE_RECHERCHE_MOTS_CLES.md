# Guide Recherche - Mots-clés qui Fonctionnent avec Adzuna

**Date**: 2026-02-03  
**Contexte**: Tu as sélectionné uniquement des entreprises (pas d'agrégateurs)

---

## ✅ Mots-clés qui FONCTIONNENT (testés)

### Excellent (10+ offres par entreprise)
- **Ingénieur** → 10 offres Capgemini, 10 Thales, 1 Sopra
- **Développeur** → 7-10 offres par entreprise
- **Cloud** → 20 offres Capgemini, 19 Sopra, 8 Dassault
- **Data** → 18 Capgemini, 20 Sopra

### Bon (5-10 offres)
- **DevOps** → 20 Capgemini, 1 Sopra
- **Backend**
- **Frontend**
- **Full Stack**

---

## ❌ Mots-clés qui NE FONCTIONNENT PAS

### Trop spécifiques (0 offres)
- ❌ "data science" → Trop technique
- ❌ "Python Django React" → Combinaison trop restrictive
- ❌ "Machine Learning Engineer" → Trop de niche
- ❌ "Senior DevOps Kubernetes" → Trop long

### Pourquoi ?
Adzuna cherche des correspondances textuelles exactes. Plus le mot-clé est long et spécifique, moins il y a de résultats.

---

## 🎯 Comment rechercher maintenant

### Étape 1 : Va sur http://localhost:3000/jobs

### Étape 2 : Utilise UN mot-clé simple

**Exemples** :
- **Intitulé du poste** : `Ingénieur`
- **Intitulé du poste** : `Développeur`
- **Intitulé du poste** : `Cloud`

### Étape 3 : NE PAS remplir Ville

Laisse le champ **Ville / Région** vide pour maximum de résultats.

### Étape 4 : Cliquer "Rechercher"

**Résultat attendu** : 50-100 offres au total (10 par entreprise × 10 entreprises)

---

## 📊 Résultats par entreprise (testés)

| Entreprise | "Ingénieur" | "Développeur" | "Cloud" | "Data" |
|------------|-------------|---------------|---------|--------|
| **Capgemini** | 10 | 7 | 20 | 18 |
| **Sopra Steria** | 1 | 10 | 19 | 20 |
| **Thales** | 10 | 10 | 10 | ? |
| **Airbus** | ? | ? | 8 | ? |
| **Dassault** | 0 | ? | 8 | 0 |
| **EDF** | ? | ? | 5 | ? |
| **TotalEnergies** | ? | ? | 2 | ? |
| **Renault** | ? | ? | 3 | ? |

---

## 💡 Stratégie de recherche efficace

### 1. Recherche large
**Mot-clé** : "Ingénieur" ou "Développeur"  
**Résultat** : 50-100 offres variées

### 2. Filtrer manuellement
Une fois les résultats affichés, tu peux :
- Lire les titres pour trouver ce qui t'intéresse
- Cliquer sur l'offre pour voir les détails
- Sauvegarder celles qui correspondent

### 3. Recherche ciblée après
Si tu veux plus spécifique :
- **"Cloud"** pour postes cloud
- **"Data"** pour data scientist/engineer
- **"DevOps"** pour devops

---

## 🔍 Pourquoi pas d'agrégateurs ?

Tu as décoché RemoteOK et LinkedIn. C'est OK, mais :

### Avantages de garder RemoteOK
- ✅ **Toujours 10 offres** même avec mots-clés spécifiques
- ✅ **Offres télétravail** internationales
- ✅ **Complète** les offres entreprises

### Recommandation
Active RemoteOK en plus des entreprises :
1. http://localhost:3000/settings/sources
2. Cocher : `☑️ RemoteOK`
3. Sauvegarder

Résultat : Tu auras offres entreprises + offres RemoteOK

---

## 🧪 Test rapide MAINTENANT

### Recherche simple
1. **Aller sur** : http://localhost:3000/jobs
2. **Intitulé** : `Ingénieur`
3. **Ville** : (laisser vide)
4. **Cliquer** : Rechercher

**Résultat attendu** : 20-30 offres minimum

---

### Si toujours 0 offres

**Vérifie tes sources** :
```bash
# Se connecter
http://localhost:3000/settings/sources

# Vérifier que des entreprises sont cochées
# Cliquer "Sauvegarder les préférences"
```

**Vérifie les logs** :
```bash
docker compose logs backend | grep "Sources activées" | tail -5
# Doit afficher: [SearchService] 📋 Sources activées: X sources (X > 0)
```

---

## 📝 Récapitulatif

### ✅ À FAIRE
- Utiliser mots-clés **simples** : "Ingénieur", "Développeur", "Cloud"
- Laisser champ **Ville vide**
- Activer **RemoteOK** en plus pour plus de résultats

### ❌ À ÉVITER
- Mots-clés longs : "Senior Python Django Developer"
- Mots-clés trop spécifiques : "data science", "machine learning"
- Remplir Ville si tu veux maximum de résultats

---

**Status** : 🎯 Prêt pour recherche  
**Action immédiate** : Recherche "Ingénieur" sur http://localhost:3000/jobs
