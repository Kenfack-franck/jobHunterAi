# 🧪 Guide de Test Complet - Job Hunter AI

## 📋 Informations de Connexion

**URL**: http://localhost:3000  
**Email**: `john.doe@testmail.com`  
**Mot de passe**: `Test2026!`

> ⚠️ Note: Ce compte de test contient déjà 3 expériences, 3 formations et 19 compétences pour tester l'application

---

## ✅ Checklist de Tests

### PHASE 1: Tests des Formulaires ✅ FIXÉ

#### Test 1.1: Ajouter une Compétence
1. Aller sur http://localhost:3000/profile
2. Dans la section "Compétences", cliquer "Ajouter une compétence"
3. Remplir:
   - Nom: `Docker`
   - Catégorie: `Outil` (tool)
   - Niveau: `Avancé` (advanced)
4. Cliquer "Ajouter"
5. **Attendu**: ✅ La compétence apparaît dans la liste

#### Test 1.2: Ajouter une Expérience (Sans Date de Fin)
1. Dans la section "Expériences", cliquer "Ajouter une expérience"
2. Remplir:
   - Poste: `Développeur Full Stack`
   - Entreprise: `Ma Startup`
   - Localisation: `Paris, France`
   - Date de début: `2024-01-15`
   - **NE PAS remplir la date de fin**
   - ✅ Cocher "Poste actuel"
   - Description: `Développement d'applications web modernes`
   - Technologies: Ajouter `React`, `TypeScript`, `Node.js`
3. Cliquer "Ajouter"
4. **Attendu**: ✅ L'expérience apparaît avec "Date de fin: En cours"

#### Test 1.3: Ajouter une Formation (Champs Minimaux)
1. Dans la section "Formations", cliquer "Ajouter une formation"
2. Remplir UNIQUEMENT:
   - Diplôme: `Master Informatique`
   - Établissement: `École Nationale Supérieure`
   - Date de début: `2022-09-01`
3. **Laisser vides**: Domaine d'études, Localisation, Date de fin, Description
4. Cliquer "Ajouter"
5. **Attendu**: ✅ La formation apparaît sans erreur

---

### PHASE 2: Recherche d'Offres

#### Test 2.1: Recherche Simple
1. Aller sur http://localhost:3000/jobs
2. Dans la barre de recherche:
   - Mots-clés: `Python Developer`
   - Localisation: `Paris`
   - Type: `CDI`
3. Cliquer "Rechercher"
4. **Attendu**: 
   - 🔵 Message bleu "Recherche en cours..." avec spinner
   - 🟢 Après quelques secondes: "X offres trouvées" (message vert)
   - 📋 Liste des offres qui apparaît

#### Test 2.2: Détails d'une Offre
1. Cliquer sur une offre dans les résultats
2. **Attendu**:
   - Titre du poste affiché
   - Description complète
   - Technologies/compétences requises
   - Score de compatibilité (ex: 75%)
   - Bouton "Générer les documents"

---

### PHASE 3: Génération de Documents AI

#### Test 3.1: Générer CV + Lettre de Motivation
1. Sur la page de détails d'une offre, cliquer "Générer les documents"
2. **Attendu**:
   - ⏳ Indicateur de chargement "Génération en cours..."
   - ✅ Affichage du CV personnalisé (PDF ou aperçu)
   - ✅ Affichage de la lettre de motivation
   - 📝 Possibilité d'éditer la lettre

#### Test 3.2: Télécharger les Documents
1. Après génération, cliquer "Télécharger le CV"
2. Cliquer "Télécharger la Lettre"
3. **Attendu**:
   - 📥 Fichiers PDF téléchargés
   - Nommage correct: `CV_Entreprise_Date.pdf`, `LM_Entreprise_Date.pdf`

---

### PHASE 4: Analyse & Matching

#### Test 4.1: Score de Compatibilité
1. Ouvrir plusieurs offres différentes
2. Observer le score affiché (ex: 58%, 72%, 85%)
3. **Attendu**:
   - 🎯 Score différent pour chaque offre (pas hardcodé à 75%)
   - 📊 Indication des compétences matchées en vert
   - ⚠️ Indication des compétences manquantes en rouge

#### Test 4.2: Compétences Matchées
1. Sur une offre, vérifier la section "Analyse de compatibilité"
2. **Attendu**:
   - Liste de vos compétences qui correspondent
   - Liste des compétences demandées que vous n'avez pas
   - Recommandations d'amélioration

---

### PHASE 5: Surveillance d'Entreprises

#### Test 5.1: Ajouter une Entreprise
1. Aller sur http://localhost:3000/companies/watch
2. Cliquer "Ajouter une entreprise"
3. Remplir:
   - Nom: `Google`
   - Site web: `https://careers.google.com`
4. Cliquer "Ajouter"
5. **Attendu**:
   - ✅ Entreprise ajoutée à la liste
   - 🔄 Statut "En attente de scraping" ou "Active"

---

## 🐛 Bugs Connus (Non-Bloquants)

1. **Dashboard stats null**: Les statistiques du dashboard ne sont pas calculées
2. **Endpoint applications manquant**: La page Applications n'est pas encore implémentée
3. **Scraping Celery**: Le scraping automatique n'est pas actif (à lancer manuellement)

---

## 📊 Résultats Attendus

### ✅ Ce qui DOIT fonctionner
- [x] Connexion/Inscription
- [x] Ajout de compétences, expériences, formations
- [x] Recherche d'offres avec feedback visuel
- [x] Affichage des offres existantes (2 offres déjà en base)
- [x] Calcul de score de compatibilité réel (AI)
- [x] Génération de documents (si configuré)

### ⏳ Ce qui est en développement
- [ ] Envoi d'emails automatique
- [ ] Scraping temps réel d'entreprises
- [ ] Statistiques du dashboard
- [ ] Kanban des candidatures

---

## 🔧 En Cas de Problème

### Erreur 422 sur les formulaires
➡️ **Status**: RÉSOLU ✅  
➡️ **Solution**: Redémarrer le frontend: `docker compose restart frontend`

### Pas d'offres affichées
➡️ **Vérifier**: `curl http://localhost:8000/api/v1/jobs` (doit retourner 2 offres)

### Score toujours à 0%
➡️ **Cause**: Modèle AI pas chargé
➡️ **Vérifier**: Logs backend `docker logs jobhunter_backend | grep "sentence-transformers"`

### Message de recherche ne s'affiche pas
➡️ **Vérifier**: Console navigateur (F12) pour erreurs JavaScript

---

## 📝 Rapport de Bugs

**Format pour remonter un bug**:
```
Page: [URL de la page]
Action: [Ce que vous avez fait]
Attendu: [Ce qui devrait se passer]
Obtenu: [Ce qui s'est passé]
Erreur: [Message d'erreur si visible]
```

**Exemple**:
```
Page: http://localhost:3000/profile
Action: Cliqué "Ajouter une compétence", rempli "Python" / "Langage" / "Expert"
Attendu: La compétence est ajoutée
Obtenu: Erreur 422
Erreur: "Request failed with status code 422"
```

---

**Date**: 2026-01-31  
**Version**: Sprint 11 - Post-Fix Formulaires  
**Status**: ✅ Tous les formulaires fonctionnels
