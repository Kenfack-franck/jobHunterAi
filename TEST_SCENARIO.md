# 🧪 SCÉNARIO DE TEST COMPLET - JOB HUNTER AI

**Date**: 2026-01-30  
**Version**: Sprint 7 Complete  
**Durée estimée**: 30-40 minutes

---

## 📋 TABLE DES MATIÈRES

1. [Préparation](#préparation)
2. [Phase 1 : Inscription & Authentification](#phase-1--inscription--authentification)
3. [Phase 2 : Découverte Interface](#phase-2--découverte-interface)
4. [Phase 3 : Profil Utilisateur](#phase-3--profil-utilisateur)
5. [Phase 4 : Recherche d'Offres](#phase-4--recherche-doffres)
6. [Phase 5 : Veille Entreprise](#phase-5--veille-entreprise)
7. [Phase 6 : Analyse & Génération](#phase-6--analyse--génération)
8. [Phase 7 : Custom Sources](#phase-7--custom-sources)
9. [Checklist Validation](#checklist-validation)

---

## 🎯 PRÉPARATION

### Option A : Utiliser le compte pré-créé (Recommandé)

```bash
cd /home/kenfack/Documents/Personnal-Work/hackaton
docker compose exec backend python create_test_user.py
```

**Identifiants du compte de test** :
```
📧 Email    : john.doe@testmail.com
🔑 Password : Test2026!
👤 Nom      : John Doe
```

**Données incluses** :
- ✅ Profil complet (Senior Full Stack Developer)
- ✅ 3 expériences professionnelles
- ✅ 2 formations universitaires
- ✅ 19 compétences techniques
- ✅ 5 offres d'emploi (Google, Datadog, Stripe, OVHcloud, Hugging Face)
- ✅ 3 entreprises en veille (Microsoft, Meta, Amazon)
- ✅ 2 sources personnalisées

### Option B : Créer un nouveau compte manuellement

Si vous préférez tester le flow complet d'inscription, suivez le scénario depuis Phase 1.

---

## 🔐 PHASE 1 : INSCRIPTION & AUTHENTIFICATION

### Test 1.1 : Accès Landing Page

**Actions** :
1. Ouvrir `http://localhost:3000`
2. Observer la page d'accueil

**Résultats attendus** :
- ✅ Page d'accueil sans navbar/sidebar (utilisateur non authentifié)
- ✅ Boutons "Connexion" et "Inscription" visibles
- ✅ Design responsive

---

### Test 1.2 : Inscription Nouveau Compte

**Actions** :
1. Cliquer "Inscription"
2. Remplir le formulaire :
   ```
   Nom complet : Jane Smith
   Email       : jane.smith@example.com
   Mot de passe: Password2026!
   ```
3. Soumettre

**Résultats attendus** :
- ✅ Toast notification "Inscription réussie"
- ✅ Redirection automatique vers Dashboard
- ✅ Navbar + Sidebar apparaissent

**Capture** : Screenshot après inscription

---

### Test 1.3 : Connexion Compte Existant

**Actions** :
1. Se déconnecter (Dropdown user → Déconnexion)
2. Cliquer "Connexion"
3. Entrer identifiants :
   ```
   Email    : john.doe@testmail.com
   Password : Test2026!
   ```
4. Se connecter

**Résultats attendus** :
- ✅ Toast "Connexion réussie"
- ✅ Redirection Dashboard
- ✅ Navbar affiche "John Doe"
- ✅ Badge "Profil 95%" visible (profil pré-rempli)

---

## 🎨 PHASE 2 : DÉCOUVERTE INTERFACE

### Test 2.1 : Navigation Navbar

**Actions** :
1. Observer la Navbar en haut
2. Cliquer sur chaque élément :
   - Logo → Retour Dashboard
   - Search bar → (Non fonctionnelle pour l'instant)
   - Bell icon → Notifications
   - Help icon → Page Help (si existe)
   - User dropdown → Menu

**Résultats attendus** :
- ✅ Logo ramène au Dashboard
- ✅ User dropdown affiche :
  - Email/Nom utilisateur
  - Badge "Profil X%"
  - "Mon profil" → `/profile`
  - "Paramètres" → `/settings`
  - "Déconnexion" → logout + redirect `/`

**Capture** : Screenshot dropdown ouvert

---

### Test 2.2 : Navigation Sidebar

**Actions** :
1. Observer Sidebar gauche (Desktop uniquement)
2. Cliquer sur chaque item :
   - 🏠 Accueil → `/dashboard`
   - 🔍 Recherche → `/jobs/search`
   - 🏢 Veille Entreprise → `/companies/watch`
   - 💼 Mon Profil → `/profile`
   - 📄 Documents → `/documents`
   - 👁️ Candidatures → `/applications`
   - ⚙️ Paramètres → `/settings`

**Résultats attendus** :
- ✅ Item actif surligné en bleu
- ✅ Hover effect sur items
- ✅ Navigation fluide sans reload complet

---

### Test 2.3 : Sidebar Collapse

**Actions** :
1. Cliquer bouton toggle en bas du Sidebar
2. Observer le collapse
3. Re-cliquer pour expand

**Résultats attendus** :
- ✅ Sidebar se réduit (icons seulement)
- ✅ Tooltip apparaît au hover (quand collapsed)
- ✅ Expand restaure labels

---

### Test 2.4 : Footer

**Actions** :
1. Scroller en bas de page
2. Observer Footer
3. Cliquer sur liens

**Résultats attendus** :
- ✅ Footer 4 colonnes visible
- ✅ Liens fonctionnels (ou pages 404 si pas encore créées)
- ✅ Copyright avec année dynamique

---

## 👤 PHASE 3 : PROFIL UTILISATEUR

### Test 3.1 : Voir Profil Complet

**Actions** :
1. Navbar → User dropdown → "Mon profil"
2. Observer les sections :
   - Informations générales
   - Expériences
   - Formations
   - Compétences

**Résultats attendus (compte john.doe)** :
- ✅ Titre : "Senior Full Stack Developer"
- ✅ 3 expériences affichées :
  - TechCorp France (actuel)
  - StartupLab (2019-2021)
  - WebAgency Pro (2018-2019)
- ✅ 2 formations :
  - Master IA - Paris-Saclay
  - Licence Info - Lyon 1
- ✅ 19 compétences avec niveaux (expert, advanced, intermediate)

**Capture** : Screenshot profil complet

---

### Test 3.2 : Calcul Complétion Profil

**Actions** :
1. Observer badge "Profil X%" dans Navbar
2. Comparer avec Dashboard card

**Résultats attendus** :
- ✅ Pourcentage identique (Navbar = Dashboard)
- ✅ Pour john.doe : ~95% (profil quasi complet)
- ✅ Pour nouveau compte : ~20% (juste email/nom)

---

### Test 3.3 : Éditer Profil

**Actions** :
1. Sur page profil, cliquer "Éditer"
2. Modifier un champ (ex: titre)
3. Sauvegarder

**Résultats attendus** :
- ✅ Toast "Profil mis à jour avec succès"
- ✅ Changement visible immédiatement
- ✅ Badge % recalculé si pertinent

---

### Test 3.4 : Ajouter Expérience

**Actions** :
1. Section Expériences → "Ajouter"
2. Remplir formulaire :
   ```
   Poste     : Lead Developer
   Entreprise: MyCompany
   Début     : 2023-01-01
   Actuel    : Oui
   ```
3. Sauvegarder

**Résultats attendus** :
- ✅ Toast "Expérience ajoutée"
- ✅ Nouvelle expérience dans la liste
- ✅ Badge "Actuel" si coché

---

### Test 3.5 : Ajouter Compétence

**Actions** :
1. Section Compétences → "Ajouter"
2. Remplir :
   ```
   Nom      : Vue.js
   Niveau   : Advanced
   Catégorie: Frontend
   ```
3. Sauvegarder

**Résultats attendus** :
- ✅ Toast "Compétence ajoutée"
- ✅ Badge coloré selon niveau
- ✅ Complétion % augmente

---

## 🔍 PHASE 4 : RECHERCHE D'OFFRES

### Test 4.1 : Liste des Offres

**Actions** :
1. Sidebar → "Recherche" (`/jobs/search`)
2. Observer liste des offres

**Résultats attendus (compte john.doe)** :
- ✅ 5 offres affichées :
  - Google France - Senior Full Stack
  - Datadog - Lead Python
  - Stripe - Full Stack Remote
  - OVHcloud - Senior Backend
  - Hugging Face - AI/ML Engineer
- ✅ Cards avec :
  - Titre poste
  - Entreprise
  - Localisation
  - Type (CDI)
  - Mode (Remote/Hybrid)
  - Date publication
- ✅ Bouton "Voir détails" sur chaque card

**Capture** : Screenshot liste offres

---

### Test 4.2 : Détail d'une Offre

**Actions** :
1. Cliquer "Voir détails" sur offre Google
2. Observer page détail

**Résultats attendus** :
- ✅ Titre : "Senior Full Stack Developer"
- ✅ Entreprise : Google France
- ✅ Description complète affichée
- ✅ Stack technique : React, TypeScript, Go, Kubernetes
- ✅ Salaire : 70k-90k EUR
- ✅ Lien source cliquable
- ✅ Boutons actions :
  - "Analyser la compatibilité"
  - "Générer documents"
  - "Supprimer"

**Capture** : Screenshot détail offre

---

### Test 4.3 : Filtres Recherche

**Actions** :
1. Page `/jobs/search`
2. Utiliser filtres :
   - Type : CDI
   - Mode : Remote
   - Localisation : Paris

**Résultats attendus** :
- ✅ Résultats filtrés en temps réel
- ✅ Count "X offres trouvées"
- ✅ Possibilité reset filtres

---

### Test 4.4 : Ajouter Offre Manuelle

**Actions** :
1. Page `/jobs` → "Ajouter offre"
2. Remplir formulaire :
   ```
   Titre      : Backend Engineer
   Entreprise : MyStartup
   Lieu       : Remote
   Type       : CDI
   URL source : https://example.com/job
   Description: Poste backend avec Python
   ```
3. Sauvegarder

**Résultats attendus** :
- ✅ Toast "Offre ajoutée"
- ✅ Offre apparaît dans liste
- ✅ Redirection vers détail

---

## 👀 PHASE 5 : VEILLE ENTREPRISE

### Test 5.1 : Liste Entreprises Surveillées

**Actions** :
1. Sidebar → "Veille Entreprise" (`/companies/watch`)
2. Observer liste

**Résultats attendus (compte john.doe)** :
- ✅ 3 entreprises affichées :
  - Microsoft
  - Meta
  - Amazon
- ✅ Cards avec :
  - Logo/nom entreprise
  - URL careers page
  - Statut actif/inactif
  - Date dernier scraping
  - Nombre offres trouvées

**Capture** : Screenshot veille entreprises

---

### Test 5.2 : Ajouter Entreprise en Veille

**Actions** :
1. Page veille → "Ajouter entreprise"
2. Remplir :
   ```
   Nom : GitLab
   URL : https://about.gitlab.com/jobs/
   ```
3. Sauvegarder

**Résultats attendus** :
- ✅ Toast "Entreprise ajoutée à la veille"
- ✅ Card apparaît dans liste
- ✅ Badge "Scraping en attente"

---

### Test 5.3 : Déclencher Scraping Manuel

**Actions** :
1. Sur card Microsoft → bouton "Scraper maintenant"
2. Attendre résultat

**Résultats attendus** :
- ✅ Toast "Scraping lancé"
- ✅ Spinner/loader pendant traitement
- ✅ Toast "X offres trouvées" après scraping
- ✅ Date "Dernière mise à jour" rafraîchie

**Note** : Le scraping peut échouer si site bloque (anti-bot). C'est normal.

---

### Test 5.4 : Voir Offres d'une Entreprise

**Actions** :
1. Card Microsoft → "Voir les offres"
2. Observer liste filtrée

**Résultats attendus** :
- ✅ Page `/jobs/search?company=Microsoft`
- ✅ Uniquement offres Microsoft
- ✅ Filtres pré-appliqués

---

## 🤖 PHASE 6 : ANALYSE & GÉNÉRATION

### Test 6.1 : Analyser Compatibilité Offre

**Actions** :
1. Aller sur détail offre Google
2. Cliquer "Analyser la compatibilité"
3. Observer résultat

**Résultats attendus** :
- ✅ Page `/jobs/[id]/analyze`
- ✅ Score compatibilité affiché (ex: 85%)
- ✅ Jauge circulaire colorée
- ✅ Sections :
  - ✅ Points forts (skills matchés)
  - ⚠️ Points manquants (skills requis absents)
  - 💡 Recommandations
- ✅ Bouton "Générer documents"

**Capture** : Screenshot analyse compatibilité

---

### Test 6.2 : Générer CV Personnalisé

**Actions** :
1. Page analyse → "Générer documents"
2. Sélectionner options :
   - Type : CV
   - Profil source : John Doe (Senior Full Stack)
   - Template : Modern
3. Cliquer "Générer"

**Résultats attendus** :
- ✅ Toast "Génération en cours..."
- ✅ Loader/spinner
- ✅ Toast "CV généré avec succès"
- ✅ Preview PDF s'affiche
- ✅ Bouton "Télécharger PDF"

**Capture** : Screenshot CV généré

---

### Test 6.3 : Générer Lettre Motivation

**Actions** :
1. Même page → "Générer lettre"
2. Options :
   - Langue : Français
   - Ton : Professionnel
   - Longueur : Standard
3. Générer

**Résultats attendus** :
- ✅ Toast "Génération en cours..."
- ✅ Texte lettre généré s'affiche
- ✅ Éditeur texte riche (modifiable)
- ✅ Bouton "Régénérer avec autre ton"
- ✅ Bouton "Télécharger PDF"

---

### Test 6.4 : Éditer Lettre Avant Download

**Actions** :
1. Dans éditeur lettre, modifier un paragraphe
2. Cliquer "Sauvegarder modifications"
3. Télécharger PDF

**Résultats attendus** :
- ✅ Modifications sauvegardées
- ✅ PDF téléchargé avec modifications
- ✅ Nom fichier : `LM_Google_2026-01-30.pdf`

---

## 🌐 PHASE 7 : CUSTOM SOURCES

### Test 7.1 : Liste Sources Personnalisées

**Actions** :
1. Page `/jobs` → Onglet "Sources personnalisées"
2. Observer liste

**Résultats attendus (compte john.doe)** :
- ✅ 2 sources :
  - RemoteOK - Python Jobs
  - AngelList - Startups France
- ✅ Cards avec :
  - Nom source
  - URL
  - Type (job_board)
  - Statut actif
  - Dernière mise à jour

---

### Test 7.2 : Ajouter Source Personnalisée

**Actions** :
1. Bouton "Ajouter source"
2. Remplir :
   ```
   Nom : We Love Remote
   URL : https://weworkremotely.com/categories/remote-programming-jobs
   Type: Job Board
   ```
3. Sauvegarder

**Résultats attendus** :
- ✅ Toast "Source ajoutée"
- ✅ Source dans liste
- ✅ Badge "Scraping en attente"

---

### Test 7.3 : Scraper Source Personnalisée

**Actions** :
1. Card "RemoteOK" → "Scraper maintenant"
2. Attendre résultat

**Résultats attendus** :
- ✅ Toast "Scraping lancé"
- ✅ Spinner pendant traitement
- ✅ Toast "X offres extraites"
- ✅ Offres apparaissent dans `/jobs/search`

**Note** : RemoteOK devrait fonctionner (testé dans Sprint 4-6).

---

### Test 7.4 : Analyser URL Offre Externe

**Actions** :
1. Page `/jobs/add` → Onglet "Par URL"
2. Coller URL :
   ```
   https://remoteok.com/remote-jobs/123456-senior-python-developer
   ```
3. Cliquer "Analyser"

**Résultats attendus** :
- ✅ Scraping de la page
- ✅ Extraction automatique :
  - Titre
  - Entreprise
  - Description
  - Stack
- ✅ Formulaire pré-rempli
- ✅ Possibilité éditer avant sauvegarder

---

## 📊 PHASE 8 : FEED PERSONNALISÉ

### Test 8.1 : Voir Feed Offres Recommandées

**Actions** :
1. Dashboard → Card "Offres recommandées"
2. Cliquer "Voir le feed"

**Résultats attendus** :
- ✅ Page `/jobs/feed`
- ✅ Offres triées par pertinence
- ✅ Score compatibilité sur chaque card
- ✅ Badge "Nouvelle" si < 7 jours
- ✅ Filtres rapides :
  - Toutes
  - >80% match
  - Remote uniquement

---

### Test 8.2 : Cache Feed Performance

**Actions** :
1. Aller sur `/jobs/feed`
2. Noter temps chargement
3. Rafraîchir page (F5)
4. Noter temps chargement

**Résultats attendus** :
- ✅ 1er chargement : ~2-3s (calcul scores)
- ✅ 2ème chargement : <500ms (cache hit)
- ✅ Pas de re-calcul si cache valide (<1h)

---

## ✅ CHECKLIST VALIDATION FINALE

### Authentification & Sécurité
- [ ] Inscription fonctionne
- [ ] Login fonctionne
- [ ] Logout fonctionne
- [ ] Redirection si non authentifié
- [ ] JWT token stocké correctement

### Interface & Navigation
- [ ] Navbar persiste sur toutes pages auth
- [ ] Sidebar collapsible fonctionne
- [ ] Footer visible en bas
- [ ] Navigation items highlight actifs
- [ ] Responsive mobile/desktop

### Profil Utilisateur
- [ ] Voir profil complet
- [ ] Éditer informations
- [ ] Ajouter expérience
- [ ] Ajouter formation
- [ ] Ajouter compétence
- [ ] Calcul complétion correct
- [ ] Badge % dans Navbar sync

### Gestion Offres
- [ ] Liste offres affichée
- [ ] Détail offre complet
- [ ] Ajouter offre manuelle
- [ ] Filtres recherche fonctionnent
- [ ] Supprimer offre

### Veille Entreprise
- [ ] Liste entreprises surveillées
- [ ] Ajouter entreprise
- [ ] Scraping manuel déclenché
- [ ] Offres récupérées affichées
- [ ] Date dernière mise à jour

### Analyse & IA
- [ ] Score compatibilité calculé
- [ ] Points forts/manquants listés
- [ ] Génération CV fonctionne
- [ ] Génération lettre fonctionne
- [ ] Édition documents avant download

### Sources Personnalisées
- [ ] Liste sources affichée
- [ ] Ajouter source
- [ ] Scraping source custom
- [ ] Analyser URL externe

### Feed & Recommandations
- [ ] Feed personnalisé affiché
- [ ] Tri par pertinence
- [ ] Cache fonctionne (perf)
- [ ] Filtres rapides fonctionnent

### Feedback Utilisateur
- [ ] Toasts s'affichent (success, error)
- [ ] Loading spinners pendant async
- [ ] Messages erreur clairs
- [ ] Confirmations avant suppression

---

## 🐛 BUGS CONNUS À IGNORER

1. **Warning Next.js config** - `experimental.serverActions` deprecated
   - **Impact** : Aucun
   - **Fix prévu** : Sprint 8

2. **Page `/analyze` build error** - Import manquant
   - **Impact** : Page ne compile pas en production
   - **Workaround** : Tester en dev mode uniquement
   - **Fix prévu** : Sprint 9

3. **Scraping Indeed échoue** - Anti-bot protection
   - **Impact** : Scraping Indeed retourne 403
   - **Workaround** : Utiliser RemoteOK qui fonctionne
   - **Fix prévu** : Proxy rotation (Sprint 12+)

4. **Search bar Navbar non fonctionnelle**
   - **Impact** : Pas de recherche depuis Navbar
   - **Workaround** : Utiliser page `/jobs/search`
   - **Fix prévu** : Sprint 10

---

## 📸 CAPTURES D'ÉCRAN À FAIRE

Pour documenter les tests, capturez :

1. **Landing page** (non auth)
2. **Dashboard** avec Navbar + Sidebar
3. **User dropdown menu** ouvert
4. **Profil complet** avec expériences
5. **Liste offres** avec 5 cards
6. **Détail offre** Google
7. **Analyse compatibilité** avec score
8. **CV généré** preview PDF
9. **Veille entreprises** liste
10. **Feed personnalisé** avec scores

---

## 📝 RAPPORT DE TEST

Après avoir terminé tous les tests, remplissez :

**Testeur** : _________________  
**Date** : _________________  
**Durée totale** : _________________  

**Résumé** :
- Tests réussis : ____ / 50
- Bugs critiques trouvés : ____
- Bugs mineurs : ____
- Suggestions d'amélioration : ____

**Commentaires généraux** :
```
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________
```

---

**Document créé le** : 2026-01-30  
**Version** : 1.0 - Sprint 7 Complete  
**Auteur** : GitHub Copilot + Kenfack
