# 🧪 INSTRUCTIONS DE TEST - Job Hunter AI

## 🚀 Lancement Rapide

### 1. Créer le profil de test automatiquement
```bash
cd /home/kenfack/Documents/Personnal-Work/hackaton
./create_test_profile.sh
```

**Identifiants créés:**
- Email: `kenfackfranck08@gmail.com`
- Mot de passe: `TestJobHunter2026!`
- 2 profils: "Backend Python Senior" + "Full-Stack Python/React"

---

## 📋 Parcours de Test Simplifié

### ÉTAPE 1 : Connexion ✅
1. Ouvrir http://localhost:3000
2. Se connecter avec les identifiants ci-dessus
3. **Attendu**: Dashboard s'affiche

### ÉTAPE 2 : Recherche d'Offres 🔍
1. Menu → **"Recherche d'emplois"**
2. Entrer dans la barre de recherche:
   - Mots-clés: `Python Developer`
   - Localisation: `Paris`
3. Cliquer **"Rechercher"**
4. **Attendu**: 
   - Message "Scraping en cours..." (~15-30s)
   - Liste d'offres s'affiche (Indeed, LinkedIn)
   - Chaque offre a un bouton **"Analyser"**

### ÉTAPE 3 : Analyser une Offre 🎯
1. Sur n'importe quelle offre, cliquer **"Analyser"**
2. **Attendu**:
   - Modal s'ouvre
   - **Score de compatibilité calculé par l'IA** (ex: 65%)
   - Spinner pendant ~5-10s (première fois)
   - Score dynamique (PAS toujours 78%)
   - Badge: "Excellent/Bon/Moyen/Faible match"

### ÉTAPE 4 : Générer les Documents 📄
1. Dans le modal, sélectionner le profil: **"Backend Python Senior"**
2. Cliquer **"Générer les documents"**
3. **Attendu**:
   - Loading pendant ~15-20s (appel Gemini AI)
   - Message: "Documents générés avec succès!"
   - 2 cards: CV + Lettre de Motivation
   - Boutons "Télécharger" sur chaque card

### ÉTAPE 5 : Télécharger les PDFs ⬇️
1. Cliquer **"Télécharger le CV"**
2. Cliquer **"Télécharger la LM"**
3. **Attendu**:
   - 2 fichiers PDF téléchargés
   - `CV_[Entreprise]_[Date].pdf` (~18 KB)
   - `LM_[Entreprise]_[Date].pdf` (~12 KB)
   - Contenu professionnel et personnalisé

### ÉTAPE 6 : Vérifier la Qualité 🔍
Ouvrir les PDFs et vérifier:
- ✅ CV: Mise en page propre, compétences mises en avant
- ✅ LM: Personnalisée pour l'offre, ton professionnel
- ✅ Pas de fautes de formatage
- ✅ Informations correctes (nom, email, téléphone)

---

## 🐛 Que Tester et Rapporter

### À vérifier sur chaque étape:

**ÉTAPE 2 - Recherche**:
- [ ] Le scraping retourne de vraies offres d'internet
- [ ] Les offres ont: titre, entreprise, localisation, description
- [ ] Pas d'erreur 404 ou 500
- [ ] Bouton "Analyser" présent sur chaque offre

**ÉTAPE 3 - Analyse**:
- [ ] Le score change selon le profil sélectionné
- [ ] Le score n'est PAS toujours 78% (c'était hardcodé avant)
- [ ] Loading state visible pendant calcul
- [ ] Badge de couleur correspond au score
- [ ] Pas d'erreur dans la console (F12)

**ÉTAPE 4 - Génération**:
- [ ] Les 2 documents sont générés (CV + LM)
- [ ] Temps de génération: 10-20s (normal)
- [ ] Message de succès affiché
- [ ] Pas d'erreur "Generation failed"

**ÉTAPE 5 - Téléchargement**:
- [ ] Les 2 PDFs se téléchargent immédiatement
- [ ] Taille correcte (10-25 KB)
- [ ] Nom de fichier pertinent
- [ ] Pas de "Blob error"

**ÉTAPE 6 - Qualité**:
- [ ] CV personnalisé pour l'offre (pas générique)
- [ ] LM mentionne l'entreprise et le poste spécifique
- [ ] Mise en forme professionnelle
- [ ] Pas de texte coupé ou manquant

---

## 📝 Format de Rapport de Bug

Si quelque chose ne fonctionne pas:

```
❌ PROBLÈME : [Description courte]

Étape: [Numéro de l'étape où ça plante]
Attendu: [Ce qui devrait se passer]
Observé: [Ce qui se passe vraiment]

Erreur console (F12):
[Copier-coller l'erreur si présente]

Screenshot: [Si possible]
```

**Exemples:**
```
❌ PROBLÈME : Le score reste bloqué à 78%

Étape: 3 (Analyse)
Attendu: Score calculé avec l'IA (devrait varier)
Observé: Toujours 78% peu importe l'offre
Erreur console: Aucune
```

```
❌ PROBLÈME : Téléchargement PDF échoue

Étape: 5 (Téléchargement CV)
Attendu: Fichier PDF se télécharge
Observé: Erreur "Failed to download document"
Erreur console: 
  TypeError: Cannot read property 'data' of undefined
  at documentsService.ts:45
```

---

## 🔧 En Cas de Problème

### Redémarrer les services
```bash
cd /home/kenfack/Documents/Personnal-Work/hackaton
docker compose restart
```

### Voir les logs
```bash
# Backend
docker logs jobhunter_backend --tail 50

# Frontend
docker logs jobhunter_frontend --tail 50
```

### Vérifier que tout tourne
```bash
docker ps
# Devrait afficher: backend, frontend, postgres, redis
```

---

## 📚 Documentation Complète

Guide détaillé avec toutes les étapes:
```bash
cat ~/.copilot/session-state/*/files/TEST_GUIDE_COMPLET.md
```

---

## ✅ Checklist Finale

- [ ] Connexion fonctionne
- [ ] Recherche retourne des offres réelles
- [ ] Scraping d'Indeed/LinkedIn marche
- [ ] Analyse calcule un score dynamique (pas hardcodé)
- [ ] Score change selon le profil
- [ ] Génération CV + LM réussit
- [ ] PDFs téléchargeables
- [ ] Contenu personnalisé et professionnel
- [ ] Pas d'erreur 404 sur les pages
- [ ] Navigation fluide

---

**Prêt à tester ?** 🚀

1. `./create_test_profile.sh`
2. Ouvrir http://localhost:3000
3. Suivre les 6 étapes ci-dessus
4. Rapporter ce qui ne fonctionne pas
