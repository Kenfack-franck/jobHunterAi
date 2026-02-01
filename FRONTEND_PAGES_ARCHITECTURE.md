# 🎨 ARCHITECTURE FRONTEND - JOB HUNTER AI

**Version** : Sprint 7 Complete + Pages Manquantes  
**Date** : 2026-01-31

---

## 📋 TABLE DES MATIÈRES

1. [Vue d'ensemble](#vue-densemble)
2. [Parcours Utilisateur](#parcours-utilisateur)
3. [Pages Publiques](#pages-publiques)
4. [Pages Authentifiées](#pages-authentifiées)
5. [Architecture Technique](#architecture-technique)
6. [État Actuel](#état-actuel)

---

## 🌐 VUE D'ENSEMBLE

L'application Job Hunter AI est structurée en **2 zones principales** :

### Zone Publique (Non authentifié)
- Landing Page
- Login
- Register
- Pages informatives (À créer)

### Zone Privée (Authentifié)
- Dashboard
- Profil
- Recherche d'offres
- Veille entreprise
- Documents générés
- Candidatures
- Paramètres

---

## 🚶 PARCOURS UTILISATEUR COMPLET

### 1️⃣ **PREMIÈRE VISITE (Non authentifié)**

```
┌─────────────────────────────────────────────────────────┐
│                    LANDING PAGE (/)                      │
│  - Hero section avec value proposition                   │
│  - Fonctionnalités clés (3-4 cards)                     │
│  - Call-to-action "Commencer gratuitement"              │
│  - Témoignages (optionnel)                              │
│  - Footer avec liens                                     │
│  - Navbar simple : Logo | Fonctionnalités | Tarifs |   │
│                     Se connecter | S'inscrire           │
└─────────────────────────────────────────────────────────┘
                            ↓
                    Clique "S'inscrire"
                            ↓
┌─────────────────────────────────────────────────────────┐
│              PAGE INSCRIPTION (/auth/register)           │
│  - Formulaire simple :                                   │
│    • Nom complet                                         │
│    • Email                                               │
│    • Mot de passe                                        │
│    • Confirmer mot de passe                              │
│  - Bouton "Créer mon compte"                            │
│  - Lien "Déjà inscrit ? Se connecter"                  │
└─────────────────────────────────────────────────────────┘
                            ↓
                  Inscription réussie
                            ↓
┌─────────────────────────────────────────────────────────┐
│            ONBOARDING WIZARD (À créer)                   │
│  Étape 1/4 : Bienvenue                                  │
│   - Message d'accueil personnalisé                      │
│   - Tour rapide des fonctionnalités                     │
│                                                          │
│  Étape 2/4 : Créer votre profil                        │
│   - Formulaire guidé simplifié                          │
│   - Ou upload CV PDF                                    │
│                                                          │
│  Étape 3/4 : Configurer votre recherche                │
│   - Postes visés                                        │
│   - Localisation préférée                               │
│   - Type de contrat                                     │
│                                                          │
│  Étape 4/4 : Prêt à commencer !                        │
│   - Résumé configuration                                │
│   - Bouton "Découvrir mon dashboard"                   │
└─────────────────────────────────────────────────────────┘
```

### 2️⃣ **CONNEXION (Utilisateur existant)**

```
┌─────────────────────────────────────────────────────────┐
│              PAGE LOGIN (/auth/login)                    │
│  - Formulaire :                                          │
│    • Email                                               │
│    • Mot de passe                                        │
│  - Bouton "Se connecter"                                │
│  - Lien "Pas encore inscrit ?"                          │
│  - (Optionnel) "Mot de passe oublié ?"                  │
└─────────────────────────────────────────────────────────┘
                            ↓
                    Login réussi
                            ↓
        Redirection vers Dashboard ou page précédente
```

### 3️⃣ **ZONE PRIVÉE (Après authentification)**

```
╔═══════════════════════════════════════════════════════════╗
║                  NAVBAR (Persistante)                      ║
║  Logo | Search bar | 🔔 Notifications | 👤 User Menu     ║
╠═══════════════════════════════════════════════════════════╣
║ SIDEBAR          │         CONTENU PRINCIPAL              ║
║ (Gauche)         │                                        ║
║                  │                                        ║
║ 🏠 Dashboard     │    [Contenu dynamique selon page]     ║
║ 🔍 Recherche     │                                        ║
║ 🏢 Veille        │                                        ║
║ 👤 Profil        │                                        ║
║ 📄 Documents     │                                        ║
║ 👁️ Candidatures  │                                        ║
║ ⚙️ Paramètres    │                                        ║
╠═══════════════════════════════════════════════════════════╣
║                      FOOTER                                ║
║  Liens | Support | Légal | © 2026 Job Hunter AI          ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 📄 PAGES PUBLIQUES (Non authentifié)

### 1. 🏠 **LANDING PAGE** (`/`)

**Objectif** : Convaincre et convertir les visiteurs

**Éléments clés** :
```
┌─────────────────────────────────────────┐
│ NAVBAR                                  │
│ Logo | Fonctionnalités | Tarifs | Login│
├─────────────────────────────────────────┤
│ HERO SECTION                            │
│ • Titre accrocheur (H1)                │
│ • Sous-titre value proposition          │
│ • CTA principal "Commencer gratuitement"│
│ • Image/illustration                    │
├─────────────────────────────────────────┤
│ FONCTIONNALITÉS (3-4 cards)           │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ │
│ │ CV IA│ │Veille│ │Analyse│ │Auto  │ │
│ │Généré│ │Entre.│ │Match │ │Apply │ │
│ └──────┘ └──────┘ └──────┘ └──────┘ │
├─────────────────────────────────────────┤
│ COMMENT ÇA MARCHE (3 étapes)          │
│ 1→ Upload CV  2→ Recherche  3→ Postuler│
├─────────────────────────────────────────┤
│ STATISTIQUES/SOCIAL PROOF               │
│ • 1000+ candidatures envoyées           │
│ • 85% taux de réponse                   │
│ • 200+ entreprises suivies              │
├─────────────────────────────────────────┤
│ TÉMOIGNAGES (optionnel)                │
│ "Grâce à Job Hunter AI, j'ai trouvé..." │
├─────────────────────────────────────────┤
│ CTA FINAL                               │
│ "Prêt à transformer votre recherche ?"  │
│ [Commencer maintenant]                  │
├─────────────────────────────────────────┤
│ FOOTER                                  │
│ Produit | Support | Légal | Social     │
└─────────────────────────────────────────┘
```

**État actuel** : ❌ Simple page avec login/register, manque tout le reste

**À faire** :
- [ ] Créer Hero section
- [ ] Cards fonctionnalités
- [ ] Section "Comment ça marche"
- [ ] Footer complet
- [ ] Navbar publique

---

### 2. 🔐 **PAGE LOGIN** (`/auth/login`)

**Objectif** : Permettre connexion rapide et sécurisée

**Éléments** :
- Formulaire centré (email, password)
- Validation temps réel
- Messages d'erreur clairs
- Lien "S'inscrire"
- (Optionnel) Social login (Google, LinkedIn)
- (Optionnel) "Mot de passe oublié"

**État actuel** : ✅ Existe mais problème de redirection

**Problèmes identifiés** :
1. ❌ Après login, pas de refresh du AuthContext → reload nécessaire
2. ❌ Cadre login reste visible après connexion
3. ❌ Pas de loading spinner visible
4. ❌ Pas de toast notification

**À corriger** :
- [ ] Appeler `refreshUser()` du AuthContext après login
- [ ] Ajouter toast de succès
- [ ] Améliorer feedback visuel

---

### 3. ✍️ **PAGE REGISTER** (`/auth/register`)

**Objectif** : Inscription simple et rapide

**Éléments** :
- Formulaire (nom, email, password, confirm password)
- Force du mot de passe (indicateur visuel)
- CGU checkbox
- Validation temps réel
- Lien "Déjà inscrit ?"

**État actuel** : ✅ Existe, même problème que login

**À corriger** :
- [ ] Refresh AuthContext après inscription
- [ ] Toast de succès
- [ ] Redirection vers onboarding (à créer)

---

## 🔒 PAGES AUTHENTIFIÉES

### 4. 🏠 **DASHBOARD** (`/dashboard`)

**Objectif** : Vue d'ensemble et point d'entrée principal

**Layout** :
```
┌─────────────────────────────────────────────────────┐
│ Bienvenue, John Doe ! 👋                            │
├─────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐  │
│ │   PROFIL    │ │  RECHERCHE  │ │  DOCUMENTS  │  │
│ │ Complétion  │ │  5 offres   │ │  3 générés  │  │
│ │    95%      │ │  trouvées   │ │  ce mois    │  │
│ │ [Compléter] │ │ [Rechercher]│ │   [Voir]    │  │
│ └─────────────┘ └─────────────┘ └─────────────┘  │
├─────────────────────────────────────────────────────┤
│ ACTIVITÉ RÉCENTE                                    │
│ • Nouvelle offre : Google - Senior Dev (il y a 2h) │
│ • CV généré pour Datadog (hier)                    │
│ • 3 nouvelles offres Stripe (3j)                   │
├─────────────────────────────────────────────────────┤
│ OFFRES RECOMMANDÉES (Top 3)                        │
│ ┌──────────────────────────────────────┐           │
│ │ Google France - Senior Full Stack    │           │
│ │ 🎯 85% match | 📍 Paris | 💰 70-90k  │           │
│ │ [Analyser] [Générer CV]              │           │
│ └──────────────────────────────────────┘           │
│ ... (2 autres offres)                              │
└─────────────────────────────────────────────────────┘
```

**État actuel** : ✅ Existe avec cards basiques

**À améliorer** :
- [ ] Ajouter section "Activité récente"
- [ ] Top 3 offres recommandées avec scores
- [ ] Statistiques visuelles (graphiques)
- [ ] Quick actions (boutons rapides)

---

### 5. 👤 **PROFIL** (`/profile`)

**Objectif** : Voir et gérer son profil professionnel

**Sections** :
```
┌─────────────────────────────────────────┐
│ INFORMATIONS GÉNÉRALES                  │
│ • Photo de profil (optionnel)          │
│ • Titre professionnel                   │
│ • Résumé                                │
│ • Contact (email, téléphone)           │
│ • Liens (LinkedIn, GitHub, Portfolio)  │
│ [Éditer]                                │
├─────────────────────────────────────────┤
│ EXPÉRIENCES PROFESSIONNELLES            │
│ ┌─────────────────────────────────┐    │
│ │ Senior Developer @ TechCorp     │    │
│ │ Mars 2021 - Présent             │    │
│ │ • Développement SaaS...         │    │
│ │ [Éditer] [Supprimer]            │    │
│ └─────────────────────────────────┘    │
│ [+ Ajouter expérience]                 │
├─────────────────────────────────────────┤
│ FORMATIONS                              │
│ • Master IA - Paris-Saclay (2016-2018) │
│ [+ Ajouter formation]                   │
├─────────────────────────────────────────┤
│ COMPÉTENCES TECHNIQUES                  │
│ [Python] [React] [FastAPI] [Docker]    │
│ (badges colorés selon niveau)          │
│ [+ Ajouter compétence]                 │
├─────────────────────────────────────────┤
│ VARIANTES PROFIL (Futur)               │
│ • Profil "Backend" (principal)         │
│ • Profil "Data Science" (secondaire)   │
│ [+ Créer variante]                      │
└─────────────────────────────────────────┘
```

**État actuel** : ✅ Existe et fonctionnel

**À améliorer** :
- [ ] Upload photo de profil
- [ ] Export CV PDF
- [ ] Variantes de profil (backend vs frontend, etc.)

---

### 6. 🔍 **RECHERCHE D'OFFRES** (`/jobs/search`)

**Objectif** : Trouver et sauvegarder des offres pertinentes

**Layout** :
```
┌─────────────────────────────────────────────────────┐
│ FILTRES (Sidebar gauche)                            │
│ ┌────────────────┐ ┌────────────────────────────┐  │
│ │ Type           │ │  RÉSULTATS (12 offres)     │  │
│ │ □ CDI          │ │  ┌────────────────────┐   │  │
│ │ □ CDD          │ │  │ Google - Senior FS │   │  │
│ │ □ Stage        │ │  │ 🎯 85% | Paris     │   │  │
│ │                │ │  │ [Détails] [Analyser]│  │  │
│ │ Mode           │ │  └────────────────────┘   │  │
│ │ □ Remote       │ │  ┌────────────────────┐   │  │
│ │ □ Hybrid       │ │  │ Datadog - Lead     │   │  │
│ │ □ Présentiel   │ │  │ 🎯 78% | Paris     │   │  │
│ │                │ │  │ [Détails] [Analyser]│  │  │
│ │ Localisation   │ │  └────────────────────┘   │  │
│ │ [Paris___]     │ │  ... (10 autres offres)   │  │
│ │                │ │                            │  │
│ │ Technologies   │ │  [Charger plus]            │  │
│ │ □ Python       │ │                            │  │
│ │ □ React        │ │                            │  │
│ │ □ Docker       │ │                            │  │
│ └────────────────┘ └────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

**État actuel** : ✅ Existe avec liste basique

**À améliorer** :
- [ ] Filtres avancés (salaire, date, entreprise)
- [ ] Tri (pertinence, date, salaire)
- [ ] Vue grille/liste toggle
- [ ] Sauvegarde de recherches

---

### 7. 📋 **DÉTAIL OFFRE** (`/jobs/[id]`)

**Objectif** : Voir détails complets et agir

**Sections** :
```
┌─────────────────────────────────────────────┐
│ ← Retour                                    │
├─────────────────────────────────────────────┤
│ GOOGLE FRANCE                               │
│ Senior Full Stack Developer                 │
│ 📍 Paris, France | 💰 70-90k | 🕒 CDI      │
├─────────────────────────────────────────────┤
│ DESCRIPTION                                 │
│ Rejoignez Google Cloud pour...             │
│ (Texte complet formaté)                    │
├─────────────────────────────────────────────┤
│ STACK TECHNIQUE                             │
│ [React] [TypeScript] [Go] [Kubernetes]     │
├─────────────────────────────────────────────┤
│ RESPONSABILITÉS                             │
│ • Développement features Cloud Console     │
│ • Architecture microservices                │
│ • Mentorat équipe                          │
├─────────────────────────────────────────────┤
│ ACTIONS                                     │
│ [🎯 Analyser compatibilité]                │
│ [📄 Générer CV + LM]                       │
│ [🗑️ Supprimer]                             │
├─────────────────────────────────────────────┤
│ SOURCE                                      │
│ 🔗 LinkedIn - Publié il y a 2 jours        │
│ [Voir l'offre originale]                   │
└─────────────────────────────────────────────┘
```

**État actuel** : ✅ Existe et fonctionnel

---

### 8. 🎯 **ANALYSE COMPATIBILITÉ** (`/jobs/[id]/analyze`)

**Objectif** : Évaluer le match avec le profil

**Layout** :
```
┌─────────────────────────────────────────────┐
│ SCORE DE COMPATIBILITÉ                      │
│        ┌───────┐                            │
│        │  85%  │ (Jauge circulaire colorée)│
│        └───────┘                            │
│        Excellent match !                    │
├─────────────────────────────────────────────┤
│ ✅ POINTS FORTS (Skills matchés)           │
│ • Python (expert) ✓                        │
│ • React (expert) ✓                         │
│ • Docker (advanced) ✓                      │
│ • 5 ans d'expérience ✓                     │
├─────────────────────────────────────────────┤
│ ⚠️ POINTS À AMÉLIORER                       │
│ • Go (requis) - Vous : débutant           │
│ • Kubernetes (avancé requis) - Vous : int.│
├─────────────────────────────────────────────┤
│ 💡 RECOMMANDATIONS IA                       │
│ • Mettez en avant vos 5 ans d'expérience   │
│ • Mentionnez vos projets Docker/K8s        │
│ • Insistez sur votre capacité d'apprentiss.│
├─────────────────────────────────────────────┤
│ ACTIONS                                     │
│ [📄 Générer CV optimisé]                   │
│ [✉️ Générer lettre de motivation]          │
└─────────────────────────────────────────────┘
```

**État actuel** : ⚠️ Existe mais problèmes de compilation

**À corriger** :
- [ ] Fix imports manquants
- [ ] Améliorer UI jauge
- [ ] Ajouter recommandations IA

---

### 9. 🏢 **VEILLE ENTREPRISE** (`/companies/watch`) ❌ 404

**Objectif** : Surveiller automatiquement les publications d'offres d'entreprises ciblées

**Pourquoi** :
- Recevoir des alertes dès qu'une entreprise que vous aimez publie
- Ne manquer aucune opportunité chez vos entreprises cibles
- Scraping automatique de leurs pages carrières

**Layout à créer** :
```
┌─────────────────────────────────────────────────────┐
│ MES ENTREPRISES SURVEILLÉES (3)                     │
│ [+ Ajouter entreprise]                              │
├─────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────┐        │
│ │ MICROSOFT                               │        │
│ │ 🌐 careers.microsoft.com                │        │
│ │ 📅 Dernière mise à jour : Il y a 2h     │        │
│ │ 📋 12 nouvelles offres trouvées          │        │
│ │ [Voir les offres] [Scraper maintenant]  │        │
│ │ [⚙️] [🗑️]                               │        │
│ └─────────────────────────────────────────┘        │
│ ┌─────────────────────────────────────────┐        │
│ │ META                                    │        │
│ │ 🌐 metacareers.com                      │        │
│ │ 📅 Dernière mise à jour : Il y a 4h     │        │
│ │ 📋 5 nouvelles offres                    │        │
│ │ [Voir les offres] [Scraper maintenant]  │        │
│ └─────────────────────────────────────────┘        │
│ ... (autres entreprises)                           │
├─────────────────────────────────────────────────────┤
│ STATISTIQUES                                        │
│ • 3 entreprises surveillées                        │
│ • 17 offres trouvées cette semaine                 │
│ • Prochain scraping automatique : dans 2h         │
└─────────────────────────────────────────────────────┘
```

**À créer** :
- [ ] Page liste entreprises
- [ ] Formulaire ajout entreprise (nom + URL)
- [ ] Bouton scraping manuel
- [ ] Indicateur dernière mise à jour
- [ ] Liste offres par entreprise

---

### 10. 📄 **DOCUMENTS GÉNÉRÉS** (`/documents`) ❌ 404

**Objectif** : Gérer tous les CV et lettres générés par l'IA

**Pourquoi** :
- Historique de tous vos documents générés
- Télécharger à nouveau un document
- Supprimer ou régénérer
- Voir pour quelle offre chaque document a été créé

**Layout à créer** :
```
┌─────────────────────────────────────────────────────┐
│ MES DOCUMENTS (15 générés)                          │
│ ┌──────┐ ┌──────┐                                  │
│ │ CV   │ │ LM   │ [Filtrer par type]              │
│ └──────┘ └──────┘                                  │
├─────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────┐        │
│ │ 📄 CV_Google_2026-01-30.pdf            │        │
│ │ Pour : Google - Senior Full Stack       │        │
│ │ Généré : Il y a 2 jours                 │        │
│ │ [📥 Télécharger] [👁️ Aperçu] [🔄 Régénérer]│      │
│ └─────────────────────────────────────────┘        │
│ ┌─────────────────────────────────────────┐        │
│ │ ✉️ LM_Datadog_2026-01-29.pdf           │        │
│ │ Pour : Datadog - Lead Python            │        │
│ │ Généré : Il y a 3 jours                 │        │
│ │ [📥 Télécharger] [👁️ Aperçu] [🗑️ Supprimer]│     │
│ └─────────────────────────────────────────┘        │
│ ... (13 autres documents)                          │
├─────────────────────────────────────────────────────┤
│ STATISTIQUES                                        │
│ • 10 CV générés ce mois                            │
│ • 5 lettres générées                                │
│ • Taux d'utilisation : 87%                         │
└─────────────────────────────────────────────────────┘
```

**À créer** :
- [ ] Page liste documents
- [ ] Filtres (type, date, entreprise)
- [ ] Preview modal
- [ ] Téléchargement multiple
- [ ] Statistiques d'utilisation

---

### 11. 👁️ **CANDIDATURES** (`/applications`) ❌ 404

**Objectif** : Journal de toutes vos candidatures envoyées

**Pourquoi** :
- Suivre vos candidatures
- Éviter de postuler 2 fois à la même offre
- Statistiques (taux de réponse)
- Relances (futur)

**Layout à créer** :
```
┌─────────────────────────────────────────────────────┐
│ JOURNAL DES CANDIDATURES (23 envoyées)              │
│ [Filtres] CDI | Remote | Paris | Cette semaine     │
├─────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────┐        │
│ │ Google France - Senior Full Stack       │        │
│ │ ✅ Envoyée le 30 Jan 2026 à 14:30      │        │
│ │ 📧 recrutement@google.com               │        │
│ │ 📄 CV + LM envoyés                      │        │
│ │ 📊 Statut : En attente                  │        │
│ │ [Voir détails] [Relancer (🔜)]         │        │
│ └─────────────────────────────────────────┘        │
│ ┌─────────────────────────────────────────┐        │
│ │ Datadog - Lead Python Developer         │        │
│ │ ✅ Envoyée le 28 Jan 2026 à 10:15      │        │
│ │ 📧 jobs@datadog.com                     │        │
│ │ 📄 CV + LM envoyés                      │        │
│ │ 📊 Statut : Réponse reçue ✅           │        │
│ │ [Voir détails] [Voir réponse]          │        │
│ └─────────────────────────────────────────┘        │
│ ... (21 autres candidatures)                       │
├─────────────────────────────────────────────────────┤
│ STATISTIQUES                                        │
│ • 23 candidatures envoyées                         │
│ • 8 réponses reçues (35%)                          │
│ • 3 entretiens planifiés (13%)                     │
│ • Temps moyen de réponse : 5 jours                │
└─────────────────────────────────────────────────────┘
```

**À créer** :
- [ ] Page liste candidatures
- [ ] Timeline par candidature
- [ ] Filtres & recherche
- [ ] Statistiques avancées
- [ ] (Futur) Système de relances

---

### 12. ⚙️ **PARAMÈTRES** (`/settings`) ❌ 404

**Objectif** : Gérer préférences et compte

**Sections à créer** :
```
┌─────────────────────────────────────────────────────┐
│ PARAMÈTRES                                          │
│ [Onglet : Compte] [Profil] [Notifications] [Confidentialité] │
├─────────────────────────────────────────────────────┤
│ ONGLET : COMPTE                                     │
│ ┌─────────────────────────────────────┐            │
│ │ Email                                │            │
│ │ john.doe@testmail.com                │            │
│ │ [Modifier]                           │            │
│ │                                      │            │
│ │ Mot de passe                         │            │
│ │ ••••••••                            │            │
│ │ [Changer mot de passe]              │            │
│ │                                      │            │
│ │ Langue                               │            │
│ │ [Français ▼] [English]              │            │
│ │                                      │            │
│ │ ZONE DANGER                          │            │
│ │ [🗑️ Supprimer mon compte]           │            │
│ └─────────────────────────────────────┘            │
├─────────────────────────────────────────────────────┤
│ ONGLET : NOTIFICATIONS                              │
│ ┌─────────────────────────────────────┐            │
│ │ □ Email quotidien (nouvelles offres)│            │
│ │ □ Alerte nouvelle offre entreprise  │            │
│ │ □ Document généré avec succès       │            │
│ │ □ Candidature envoyée               │            │
│ └─────────────────────────────────────┘            │
├─────────────────────────────────────────────────────┤
│ ONGLET : CONFIDENTIALITÉ                            │
│ ┌─────────────────────────────────────┐            │
│ │ □ Partager profil avec recruteurs   │            │
│ │ □ Stocker historique recherches     │            │
│ │ [Télécharger mes données] (RGPD)    │            │
│ └─────────────────────────────────────┘            │
└─────────────────────────────────────────────────────┘
```

**À créer** :
- [ ] Page settings avec onglets
- [ ] Formulaire changement email
- [ ] Formulaire changement mot de passe
- [ ] Préférences notifications
- [ ] Export données (RGPD)
- [ ] Suppression compte

---

## 🛠️ ARCHITECTURE TECHNIQUE

### Structure des dossiers

```
frontend/src/
├── app/
│   ├── (public)/              # Pages publiques
│   │   ├── page.tsx           # Landing page
│   │   └── about/
│   │       └── page.tsx       # À propos
│   ├── auth/
│   │   ├── login/
│   │   │   └── page.tsx       # ✅ Existe
│   │   └── register/
│   │       └── page.tsx       # ✅ Existe
│   ├── (protected)/           # Pages protégées
│   │   ├── dashboard/
│   │   │   └── page.tsx       # ✅ Existe
│   │   ├── profile/
│   │   │   ├── page.tsx       # ✅ Existe
│   │   │   └── create/
│   │   │       └── page.tsx   # ✅ Existe
│   │   ├── jobs/
│   │   │   ├── page.tsx       # ✅ Existe (liste)
│   │   │   ├── search/
│   │   │   │   └── page.tsx   # ✅ Existe
│   │   │   └── [id]/
│   │   │       ├── page.tsx   # ✅ Existe (détail)
│   │   │       └── analyze/
│   │   │           └── page.tsx # ⚠️ Compile error
│   │   ├── companies/
│   │   │   └── watch/
│   │   │       └── page.tsx   # ❌ À créer
│   │   ├── documents/
│   │   │   └── page.tsx       # ❌ À créer
│   │   ├── applications/
│   │   │   └── page.tsx       # ❌ À créer
│   │   └── settings/
│   │       └── page.tsx       # ❌ À créer
│   └── layout.tsx             # ✅ Root layout avec providers
├── components/
│   ├── layout/                # ✅ Créés (Sprint 7)
│   │   ├── Navbar.tsx
│   │   ├── Sidebar.tsx
│   │   ├── Footer.tsx
│   │   └── AppShell.tsx
│   ├── ui/                    # Composants shadcn/ui
│   └── features/              # Composants métier
├── contexts/                  # ✅ Créés (Sprint 7)
│   ├── AuthContext.tsx
│   └── ProfileContext.tsx
├── lib/
│   ├── api.ts                 # Client API
│   ├── auth.ts                # Service auth
│   └── profile.ts             # Service profile
└── types/
    └── index.ts               # Types TypeScript
```

---

## 📊 ÉTAT ACTUEL (Sprint 7)

### ✅ Implémenté (11 pages)

1. ✅ Landing page (basique)
2. ✅ Login
3. ✅ Register
4. ✅ Dashboard
5. ✅ Profile (view + create + edit)
6. ✅ Jobs search
7. ✅ Job detail
8. ✅ Job analyze (compile error)
9. ✅ Job add manual
10. ✅ Profile create
11. ✅ Profile edit

### ❌ Manquant (5 pages + amélioration landing)

1. ❌ Landing page professionnelle (Hero + Features + Footer)
2. ❌ Companies watch page
3. ❌ Documents page
4. ❌ Applications page
5. ❌ Settings page
6. ❌ Onboarding wizard (bonus)

---

## 🎯 PRIORITÉS DÉVELOPPEMENT

### Priorité 1 - Critique (Sprint 8)
1. **Fix login/register** - Refresh AuthContext après connexion
2. **Landing page** - Hero + Features + Footer professionnels
3. **Settings page** - Basique (email, password, langue)

### Priorité 2 - Important (Sprint 9)
4. **Companies watch** - Liste + Ajout + Scraping
5. **Documents page** - Liste + Filtres + Download
6. **Applications page** - Journal + Stats

### Priorité 3 - Nice to have (Sprint 10+)
7. **Onboarding wizard** - Guide 4 étapes au premier login
8. **Help page** - FAQ + Tutoriels
9. **About page** - Présentation produit

---

## 📝 NOTES TECHNIQUES

### Routing Next.js 14 (App Router)

- **Public routes** : Accessibles sans auth
- **Protected routes** : Wrappées avec `<ProtectedRoute>`
- **Dynamic routes** : `[id]` pour détails
- **Layouts imbriqués** : RootLayout → AuthProvider → ProfileProvider → AppShell

### State Management

- **AuthContext** : État authentification global
- **ProfileContext** : État profil utilisateur global
- **React Query** (futur) : Cache API calls

### Navigation

- **Navbar** : Persistante sur toutes pages auth
- **Sidebar** : Navigation principale (Desktop)
- **Footer** : Liens + informations légales
- **Breadcrumbs** (futur) : Fil d'Ariane

---

**Document créé le** : 2026-01-31  
**Version** : Sprint 7 Review + Pages Manquantes  
**Auteur** : GitHub Copilot + Kenfack
