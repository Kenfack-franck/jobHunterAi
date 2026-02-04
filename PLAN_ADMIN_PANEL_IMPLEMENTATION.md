# 🔐 PLAN D'IMPLÉMENTATION - Admin Panel avec Limites

**Branche Git:** `feature/admin-panel-with-limits`

---

## 📋 OBJECTIFS

### Fonctionnalités à ajouter :
1. ✅ **Système de rôles** (user vs admin)
2. ✅ **Panel admin** pour gérer les utilisateurs
3. ✅ **Système de limites** pour le plan gratuit
4. ✅ **Notifications email** à l'admin
5. ✅ **Widgets d'utilisation** pour les utilisateurs

### Limites du Plan Gratuit :
- 🔍 **50 recherches/jour**
- 💾 **50 offres sauvegardées max**
- 👤 **3 profils max**
- 📝 **30 candidatures suivies**
- 📄 **5 CV parsés (upload)**
- 🏢 **5 entreprises en veille**
- ⭐ **4 CV personnalisés générés/jour** (NOUVEAU)

---

## 🗂️ STRUCTURE DU PLAN

### PHASE 1 : Base de Données (1h)
### PHASE 2 : Backend (3h)
### PHASE 3 : Frontend - Admin Panel (2h30)
### PHASE 4 : Frontend - Limites Utilisateur (2h)
### PHASE 5 : Tests et Déploiement (1h)

**TOTAL ESTIMÉ : ~9h30**

---

# 🔧 PHASE 1 : BASE DE DONNÉES (1h)

## 1.1 Migration Alembic - Ajouter colonne `role`

**Fichier à créer :**
`backend/alembic/versions/YYYY_MM_DD_HHMM-add_user_role.py`

**Objectif :** Ajouter une colonne `role` à la table `users`

**Actions :**
- Ajouter colonne `role VARCHAR(20) DEFAULT 'user'`
- Valeurs possibles : `'user'` ou `'admin'`
- Pas nullable, avec default

**Résultat attendu :**
```
Table users:
- id (existant)
- email (existant)
- ... (autres colonnes existantes)
- role (NOUVEAU) → 'user' par défaut
```

---

## 1.2 Migration Alembic - Table `user_limits`

**Fichier à créer :**
`backend/alembic/versions/YYYY_MM_DD_HHMM-create_user_limits_table.py`

**Objectif :** Créer une table pour suivre les limites d'utilisation

**Structure de la table :**

### Colonnes de base :
- `id` : UUID, primary key
- `user_id` : UUID, foreign key vers users(id) avec ON DELETE CASCADE
- `created_at` : timestamp
- `updated_at` : timestamp

### Compteurs actuels (ce que l'user a utilisé) :
- `saved_offers_count` : integer, default 0
- `searches_today_count` : integer, default 0
- `profiles_count` : integer, default 0
- `applications_count` : integer, default 0
- `cv_parsed_count` : integer, default 0
- `watched_companies_count` : integer, default 0
- `generated_cv_today_count` : integer, default 0 ⭐ NOUVEAU

### Limites personnalisées (NULL = utilise les limites par défaut) :
- `max_saved_offers` : integer, nullable
- `max_searches_per_day` : integer, nullable
- `max_profiles` : integer, nullable
- `max_applications` : integer, nullable
- `max_cv_parses` : integer, nullable
- `max_watched_companies` : integer, nullable
- `max_generated_cv_per_day` : integer, nullable ⭐ NOUVEAU

### Métadonnées :
- `last_search_date` : date (pour reset du compteur quotidien)
- `last_cv_generation_date` : date (pour reset du compteur quotidien) ⭐ NOUVEAU

**Index à créer :**
- Index unique sur `user_id`
- Index sur `last_search_date`

**Résultat attendu :**
- 1 ligne dans `user_limits` pour chaque utilisateur
- Créée automatiquement à l'inscription (trigger ou logique backend)

---

## 1.3 Script SQL - Mettre votre compte en admin

**Fichier à créer :**
`backend/scripts/set_admin.sql`

**Objectif :** Donner le rôle admin à votre compte

**Contenu du script :**
- UPDATE users SET role = 'admin' WHERE email = 'kenfackfranck08@gmail.com';
- Vérification avec SELECT

**Exécution :**
- Manuellement via `docker compose exec postgres psql...`
- Ou via script Python d'initialisation

---

# 🔧 PHASE 2 : BACKEND (3h)

## 2.1 Modèles SQLAlchemy (30 min)

**Fichier à modifier :**
`backend/app/models/user.py`

**Modifications :**
- Ajouter champ `role` au modèle User
- Type : String(20), default='user'
- Ajouter relation `limits` vers UserLimits

**Fichier à créer :**
`backend/app/models/user_limits.py`

**Contenu :**
- Classe `UserLimits` avec tous les champs définis en 1.2
- Relation vers User
- Méthodes helper : `get_limit()`, `get_current()`, etc.

---

## 2.2 Service de Gestion des Limites (1h)

**Fichier à créer :**
`backend/app/services/limit_service.py`

**Classe : `LimitService`**

### Constantes :
```
DEFAULT_LIMITS = {
    'max_saved_offers': 50,
    'max_searches_per_day': 50,
    'max_profiles': 3,
    'max_applications': 30,
    'max_cv_parses': 5,
    'max_watched_companies': 5,
    'max_generated_cv_per_day': 4  # NOUVEAU
}
```

### Méthodes principales :

#### `check_limit(user_id, limit_type) -> tuple[bool, int, int]`
**Objectif :** Vérifier si l'utilisateur peut encore faire l'action

**Logique :**
1. Récupérer `user_limits` de l'utilisateur
2. Si pas trouvé → créer automatiquement
3. Récupérer le compteur actuel (ex: `saved_offers_count`)
4. Récupérer la limite (custom ou default)
5. Comparer : `current < limit`
6. Retourner : (peut_continuer, actuel, limite)

**Cas spéciaux :**
- Pour limites quotidiennes (recherches, CV générés) :
  - Vérifier si `last_search_date` != aujourd'hui
  - Si différent → reset le compteur à 0
  - Puis vérifier la limite

---

#### `increment(user_id, limit_type) -> None`
**Objectif :** Incrémenter le compteur après une action réussie

**Logique :**
1. Récupérer `user_limits`
2. Incrémenter le compteur approprié
3. Mettre à jour `updated_at`
4. Si limite quotidienne → mettre à jour la date
5. Sauvegarder en base

---

#### `check_and_send_alerts(user_id, limit_type) -> None`
**Objectif :** Envoyer des emails d'alerte si nécessaire

**Logique :**
1. Calculer le pourcentage d'utilisation
2. Si >= 90% → Envoyer email à l'admin
3. Si == 100% → Envoyer email urgent à l'admin
4. Éviter les doublons (flag `alert_sent_at` ?)

**Email à envoyer :**
- Destinataire : admin (récupérer tous les users avec role='admin')
- Sujet : "⚠️ Utilisateur proche/à la limite"
- Corps : Détails de l'utilisateur + stats + lien admin panel

---

#### `get_user_usage_stats(user_id) -> dict`
**Objectif :** Récupérer toutes les stats d'utilisation pour affichage

**Retour :**
```python
{
    'saved_offers': {'current': 47, 'limit': 50, 'percentage': 94},
    'searches_today': {'current': 12, 'limit': 50, 'percentage': 24},
    'profiles': {'current': 2, 'limit': 3, 'percentage': 67},
    'applications': {'current': 15, 'limit': 30, 'percentage': 50},
    'cv_parsed': {'current': 3, 'limit': 5, 'percentage': 60},
    'watched_companies': {'current': 2, 'limit': 5, 'percentage': 40},
    'generated_cv_today': {'current': 2, 'limit': 4, 'percentage': 50}
}
```

---

## 2.3 Middleware de Vérification Admin (15 min)

**Fichier à créer :**
`backend/app/api/dependencies/admin.py`

**Fonction : `require_admin(current_user: User) -> User`**

**Logique :**
- Vérifier `current_user.role == 'admin'`
- Si non → lever HTTPException 403 Forbidden
- Si oui → retourner current_user

**Usage dans les routes :**
- Utiliser comme dépendance FastAPI
- Toutes les routes `/admin/*` l'utilisent

---

## 2.4 Endpoints Admin (1h)

**Fichier à créer :**
`backend/app/api/routes/admin.py`

### Route 1 : `GET /api/v1/admin/users`
**Objectif :** Lister tous les utilisateurs

**Query params :**
- `search` : string (recherche par email)
- `status` : 'active' | 'blocked' | 'all'
- `page` : int
- `per_page` : int (max 100)

**Réponse :**
```json
{
    "users": [
        {
            "id": "uuid",
            "email": "jean@test.fr",
            "full_name": "Jean Dupont",
            "role": "user",
            "is_active": true,
            "created_at": "2026-02-03T...",
            "usage": {
                "saved_offers": {"current": 47, "limit": 50},
                "searches_today": {"current": 12, "limit": 50}
                // ... autres stats
            }
        }
    ],
    "total": 247,
    "page": 1,
    "total_pages": 13
}
```

**Logique :**
1. Vérifier que l'utilisateur est admin (dependency)
2. Query la table users avec filtres
3. Pour chaque user → récupérer ses limits via `LimitService`
4. Paginer les résultats
5. Retourner

---

### Route 2 : `PUT /api/v1/admin/users/{user_id}/toggle-active`
**Objectif :** Bloquer/Débloquer un utilisateur

**Body :** Aucun (toggle automatique)

**Réponse :**
```json
{
    "user_id": "uuid",
    "email": "jean@test.fr",
    "is_active": false,
    "message": "Utilisateur bloqué avec succès"
}
```

**Logique :**
1. Récupérer l'utilisateur par ID
2. Inverser `is_active` : True → False ou False → True
3. Sauvegarder
4. Logger l'action (qui a fait quoi, quand)
5. Retourner le nouvel état

---

### Route 3 : `DELETE /api/v1/admin/users/{user_id}`
**Objectif :** Supprimer complètement un utilisateur

**Query params :**
- `confirm` : 'yes' (sécurité pour éviter suppression accidentelle)

**Réponse :**
```json
{
    "message": "Utilisateur et toutes ses données supprimés",
    "deleted": {
        "user": true,
        "profiles": 2,
        "job_offers": 34,
        "applications": 15
    }
}
```

**Logique :**
1. Vérifier `confirm == 'yes'` sinon erreur
2. Récupérer l'utilisateur
3. Supprimer (CASCADE via foreign keys supprime tout)
4. Compter ce qui a été supprimé pour le retour
5. Logger l'action
6. Retourner le résumé

---

### Route 4 : `PUT /api/v1/admin/users/{user_id}/limits`
**Objectif :** Modifier les limites personnalisées d'un utilisateur

**Body :**
```json
{
    "max_saved_offers": 100,
    "max_profiles": 5,
    "reason": "Client VIP - paiement hors ligne"
}
```

**Réponse :**
```json
{
    "user_id": "uuid",
    "updated_limits": {
        "max_saved_offers": 100,
        "max_profiles": 5
    },
    "reason": "Client VIP..."
}
```

**Logique :**
1. Récupérer `user_limits` de l'utilisateur
2. Mettre à jour les limites custom fournies
3. Sauvegarder avec la raison (log)
4. Retourner les nouvelles limites

---

### Route 5 : `GET /api/v1/admin/stats`
**Objectif :** Statistiques globales pour le dashboard admin

**Réponse :**
```json
{
    "total_users": 247,
    "active_users": 244,
    "blocked_users": 3,
    "new_users_this_week": 23,
    "new_users_today": 5,
    "users_near_limit": [
        {"email": "jean@test.fr", "usage": "94%"}
    ],
    "registrations_last_7_days": {
        "2026-02-03": 5,
        "2026-02-02": 8,
        // ... 7 jours
    }
}
```

**Logique :**
1. Compter les users par statut
2. Filtrer les nouvelles inscriptions (this week, today)
3. Identifier les users > 90% sur n'importe quelle limite
4. Agréger les inscriptions des 7 derniers jours (GROUP BY)
5. Retourner

---

## 2.5 Intégration avec Endpoints Existants (30 min)

**Fichiers à modifier :**

### `backend/app/api/routes/jobs.py`

**Dans : `POST /jobs/save` (ou équivalent)**

**Ajouter AVANT de sauvegarder :**
1. Vérifier limite : `can_save, current, max = limit_service.check_limit(user_id, 'saved_offers')`
2. Si `not can_save` → lever HTTPException 403 avec message
3. Après sauvegarde réussie → `limit_service.increment(user_id, 'saved_offers')`
4. Vérifier si alerte nécessaire → `limit_service.check_and_send_alerts(user_id, 'saved_offers')`

**Dans : `POST /jobs/search` (ou équivalent)**

**Ajouter :**
1. Check limite recherches quotidiennes
2. Incrémenter après recherche
3. Alertes si nécessaire

---

### `backend/app/api/routes/profiles.py`

**Dans : `POST /profiles`**

**Ajouter :**
1. Check limite profils
2. Incrémenter après création
3. Alertes

---

### `backend/app/api/routes/documents.py` (si existe)

**Dans : route de génération de CV personnalisé**

**Ajouter :**
1. Check limite `max_generated_cv_per_day` (4/jour)
2. Incrémenter après génération
3. Alertes

---

### `backend/app/api/routes/applications.py` (si existe)

**Dans : route de création de candidature**

**Ajouter :**
1. Check limite applications
2. Incrémenter
3. Alertes

---

## 2.6 Service d'Email (déjà existant, juste utiliser)

**Fichier existant :**
`backend/app/services/email_service.py`

**Ajouter une nouvelle fonction :**

### `send_admin_limit_alert(user, limit_type, percentage)`

**Objectif :** Envoyer email à tous les admins

**Logique :**
1. Récupérer tous les users avec `role='admin'`
2. Pour chaque admin → envoyer email
3. Template d'email avec :
   - Sujet approprié (90% vs 100%)
   - Détails de l'utilisateur
   - Stats d'utilisation
   - Lien vers admin panel : `/admin/users?email={user.email}`
   - Actions suggérées

---

# 🎨 PHASE 3 : FRONTEND - ADMIN PANEL (2h30)

## 3.1 Créer la structure des pages (15 min)

**Fichiers à créer :**

### `frontend/src/app/admin/layout.tsx`
**Objectif :** Layout commun pour toutes les pages admin

**Contenu :**
- Vérification que l'utilisateur est admin
- Si non admin → rediriger vers /dashboard avec message
- Sidebar navigation avec liens vers :
  - Dashboard
  - Utilisateurs
  - (Autres sections futures)

---

### `frontend/src/app/admin/page.tsx`
**Objectif :** Redirection vers /admin/dashboard

---

### `frontend/src/app/admin/dashboard/page.tsx`
**Objectif :** Dashboard admin avec statistiques

---

### `frontend/src/app/admin/users/page.tsx`
**Objectif :** Gestion des utilisateurs

---

## 3.2 Page Admin Dashboard (45 min)

**Fichier : `frontend/src/app/admin/dashboard/page.tsx`**

### Sections à afficher :

#### 1. Cartes de statistiques (grid 3 colonnes)
**Données à afficher :**
- Total utilisateurs (avec badge actifs/bloqués)
- Nouveaux cette semaine
- Utilisateurs proches de la limite (badge rouge si > 0)

**Design :**
- Cards avec gradients (bleu, vert, orange)
- Icônes Lucide (Users, TrendingUp, AlertTriangle)
- Nombre en gros + label en petit

---

#### 2. Graphique des inscriptions (7 derniers jours)
**Données :** API `/admin/stats` → `registrations_last_7_days`

**Affichage :**
- Graphique en barres simple (ou ligne)
- Utiliser une lib simple (recharts ou Chart.js)
- Axes : Jours (Lun, Mar, Mer...) / Nombre

**Alternative simple :**
- Si pas de lib graphique → tableau avec barres CSS
- Hauteur de la barre = proportionnelle au nombre

---

#### 3. Liste des derniers inscrits (5 derniers)
**Données :** API `/admin/users?per_page=5&sort=created_at`

**Affichage :**
- Liste simple avec :
  - Email
  - Date relative ("Il y a 2h", "Hier")
  - Badge statut (actif/bloqué)
  - Bouton "Voir" → vers page utilisateurs avec filtre

---

#### 4. Alertes utilisateurs proches limites
**Données :** API `/admin/stats` → `users_near_limit`

**Affichage :**
- Card avec bordure orange/rouge
- Liste des users à surveiller
- Pourcentage d'utilisation en badge
- Bouton "Action" → modal ou redirection

---

## 3.3 Page Gestion Utilisateurs (1h)

**Fichier : `frontend/src/app/admin/users/page.tsx`**

### Sections :

#### 1. Barre de contrôle (top)
**Composants :**
- Input de recherche (par email)
- Select filter par statut (Tous/Actifs/Bloqués)
- Bouton "Actualiser"
- Compteur : "247 utilisateurs trouvés"

---

#### 2. Tableau utilisateurs
**Colonnes :**
- Email (avec avatar/initiales)
- Nom complet
- Date d'inscription (format court)
- Statut (badge vert actif / rouge bloqué)
- Utilisation (barre de progression)
  - Afficher l'utilisation max parmi toutes les limites
  - Badge coloré : vert < 70%, orange 70-90%, rouge > 90%
- Actions (boutons dropdown)

**Actions disponibles :**
- 🔴 Bloquer / ✅ Activer (toggle)
- 📊 Voir détails (modal)
- ⚙️ Modifier limites (modal)
- 🗑️ Supprimer (modal confirmation)

---

#### 3. Pagination
**Composant :**
- Affichage : "Page 1 sur 13"
- Boutons Précédent/Suivant
- Optionnel : sélecteur page rapide

---

## 3.4 Composants Modaux (30 min)

**Fichiers à créer :**

### `frontend/src/components/admin/UserDetailsModal.tsx`
**Objectif :** Afficher tous les détails d'un utilisateur

**Contenu :**
- Infos perso (email, nom, date inscription)
- Toutes les statistiques d'utilisation avec barres
- Profils créés (liste)
- Offres sauvegardées (nombre)
- Dernière connexion
- Actions rapides (bloquer, modifier limites)

---

### `frontend/src/components/admin/EditLimitsModal.tsx`
**Objectif :** Modifier les limites d'un utilisateur

**Contenu :**
- Pour chaque limite :
  - Label + valeur actuelle
  - Input pour nouvelle valeur
  - Info : valeur par défaut
- Textarea "Raison" (optionnel)
- Boutons Annuler/Sauvegarder

**Validation :**
- Valeurs positives uniquement
- Min 1, Max 9999
- Afficher erreur si invalide

---

### `frontend/src/components/admin/ConfirmDeleteModal.tsx`
**Objectif :** Confirmer la suppression d'un user

**Contenu :**
- Titre en rouge : "⚠️ Supprimer l'utilisateur ?"
- Message : "Cette action est IRRÉVERSIBLE"
- Détails de ce qui sera supprimé :
  - Profils
  - Offres sauvegardées
  - Candidatures
  - Tous les documents
- Input de confirmation : "Tapez 'SUPPRIMER' pour confirmer"
- Boutons Annuler/Supprimer (rouge)

**Logique :**
- Désactiver bouton Supprimer tant que input != "SUPPRIMER"
- Après confirmation → appeler API DELETE
- Afficher toast succès
- Recharger la liste

---

# 🎨 PHASE 4 : FRONTEND - LIMITES UTILISATEUR (2h)

## 4.1 Service Frontend pour les Limites (15 min)

**Fichier à créer :**
`frontend/src/lib/limitsService.ts`

**Fonctions :**

### `getUserLimits() -> Promise<UsageStats>`
**Objectif :** Récupérer les stats d'utilisation de l'utilisateur courant

**Logique :**
- Appeler API (endpoint à créer) : `GET /api/v1/users/me/limits`
- Retourner les stats
- Mettre en cache (optionnel)

---

### `checkBeforeAction(limitType: string) -> Promise<boolean>`
**Objectif :** Vérifier si l'action est possible avant de l'exécuter

**Logique :**
- Appeler API : `GET /api/v1/users/me/limits/check?type={limitType}`
- Retourner true/false
- Si false → afficher modal d'erreur

---

## 4.2 Widget d'Utilisation Dashboard (30 min)

**Fichier à créer :**
`frontend/src/components/usage/UsageWidget.tsx`

**Emplacement :** Dashboard utilisateur (`/dashboard`)

**Design :**
- Card moderne avec gradient subtil
- Titre : "📊 Votre Utilisation (Plan Gratuit)"
- Liste des limites avec barres de progression
- Chaque limite :
  - Icône + Label
  - Barre de progression colorée (vert → orange → rouge)
  - Texte : "42/50"
  - Pourcentage
- Footer :
  - Lien "Besoin de plus ?" → Contact admin
  - Email : admin@jobhunter.com

**Barres de progression :**
- < 70% : vert
- 70-89% : orange
- 90-99% : rouge clignotant
- 100% : rouge + badge "LIMITE ATTEINTE"

---

## 4.3 Modals d'Avertissement (45 min)

**Fichiers à créer :**

### `frontend/src/components/usage/LimitWarningModal.tsx`
**Objectif :** Avertir l'utilisateur qu'il approche de la limite

**Quand afficher ?**
- Automatiquement quand utilisation atteint 90%
- Une seule fois par session (localStorage flag)

**Contenu :**
- Icône ⚠️ orange
- Titre : "Limite presque atteinte"
- Message : "Vous avez utilisé 47/50 offres sauvegardées"
- Info : Ce qui se passe à 100%
- Boutons :
  - "Compris" (ferme)
  - "Contacter l'admin" (ouvre email)

---

### `frontend/src/components/usage/LimitReachedModal.tsx`
**Objectif :** Bloquer l'action si limite atteinte

**Quand afficher ?**
- Quand l'utilisateur tente une action bloquée
- Ex : sauvegarder 51ème offre

**Contenu :**
- Icône 🛑 rouge
- Titre : "Limite Atteinte"
- Message : "Vous ne pouvez plus sauvegarder d'offres (50/50)"
- Solutions :
  - Supprimer des offres anciennes
  - Contacter l'admin pour augmenter
- Email admin : lien mailto
- Boutons :
  - "Voir mes offres" (→ /jobs?filter=saved)
  - "Contacter l'admin" (mailto)
  - "Fermer"

**Important :**
- Modal non fermable avec X (forcer à choisir action)
- Overlay sombre pour emphase

---

## 4.4 Intégration dans les Actions Utilisateur (30 min)

**Fichiers à modifier :**

### `frontend/src/app/jobs/page.tsx`
**Modifier : Action "Sauvegarder une offre"**

**Logique à ajouter AVANT l'API call :**
```typescript
// Pseudo-code
const handleSaveJob = async () => {
  // 1. Vérifier la limite
  const canSave = await limitsService.checkBeforeAction('saved_offers');
  
  // 2. Si non → afficher modal limite atteinte
  if (!canSave) {
    setShowLimitModal(true);
    return;
  }
  
  // 3. Si oui → continuer normalement
  await saveJob();
  
  // 4. Recharger les stats d'utilisation
  await refreshUsageStats();
  
  // 5. Si maintenant à 90% → afficher warning
  if (newUsage >= 90) {
    setShowWarningModal(true);
  }
}
```

---

### `frontend/src/app/profile/create/page.tsx`
**Modifier : Bouton "Créer un profil"**

**Ajouter :**
- Check limite avant création
- Modal si limite atteinte (3/3)
- Message : "Supprimez un profil existant ou contactez l'admin"

---

### `frontend/src/app/documents/page.tsx` (si page génération CV existe)
**Modifier : Bouton "Générer CV personnalisé"**

**Ajouter :**
- Check limite quotidienne (4/jour)
- Modal spécifique : "Vous avez généré 4 CV aujourd'hui. Réessayez demain."

---

## 4.5 Indicateurs Visuels (15 min)

**Fichier à créer :**
`frontend/src/components/usage/UsageBadge.tsx`

**Objectif :** Badge compact à afficher dans header/menu

**Design :**
- Petit badge coloré
- Affiche la pire utilisation (max %)
- Couleurs : vert/orange/rouge
- Tooltip au hover : détails complets
- Cliquable → ouvre UsageWidget ou redirige vers /dashboard

**Emplacement :**
- Dans le header à côté de l'avatar
- Ou dans le menu utilisateur (dropdown)

---

# 🧪 PHASE 5 : TESTS & DÉPLOIEMENT (1h)

## 5.1 Tests Backend (30 min)

**Fichier à créer :**
`backend/tests/test_admin_routes.py`

**Tests à écrire :**

### Test 1 : Accès admin requis
- User normal essaie d'accéder à `/admin/users`
- Doit recevoir 403 Forbidden

### Test 2 : Lister utilisateurs
- Admin appelle GET `/admin/users`
- Doit retourner liste avec pagination

### Test 3 : Bloquer utilisateur
- Admin bloque un user
- Vérifier `is_active = False`
- User bloqué essaie de se connecter → refusé

### Test 4 : Vérifier limites
- User sauvegarde 50 offres
- 51ème tentative → erreur 403

### Test 5 : Reset quotidien
- User fait 50 recherches aujourd'hui
- Changer la date (mock)
- Vérifier compteur reset à 0

---

## 5.2 Tests Frontend Manuels (15 min)

**Checklist :**

### Tests Admin
- [ ] Se connecter en tant qu'admin
- [ ] Accéder à `/admin/dashboard` → affiche stats
- [ ] Voir la liste des users
- [ ] Bloquer un user → vérifier qu'il ne peut plus se connecter
- [ ] Débloquer le user → vérifier qu'il peut se reconnecter
- [ ] Modifier les limites d'un user → vérifier application
- [ ] Supprimer un user test → vérifier suppression complète

### Tests Utilisateur
- [ ] Widget utilisation visible dans dashboard
- [ ] Sauvegarder 48 offres → pas d'alerte
- [ ] Sauvegarder 49ème → warning 90%
- [ ] Sauvegarder 50ème → message limite proche
- [ ] Tenter 51ème → modal bloquant affiché
- [ ] Générer 4 CV dans la journée
- [ ] Tenter 5ème CV → modal "Limite quotidienne atteinte"

---

## 5.3 Migration Base de Données Production (15 min)

**Étapes :**

### 1. Tester migrations localement
```bash
cd backend
alembic upgrade head
```

### 2. Créer backup DB production
```bash
docker compose -f docker-compose.prod.yml exec postgres pg_dump...
```

### 3. Appliquer migrations en production
```bash
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### 4. Vérifier tables créées
```sql
\d user_limits
SELECT * FROM users WHERE role='admin';
```

### 5. Définir votre compte en admin
```sql
UPDATE users SET role='admin' WHERE email='kenfackfranck08@gmail.com';
```

---

## 5.4 Déploiement GitLab CI/CD (optionnel)

**Si GitLab CI/CD configuré :**
- Merge de la branche `feature/admin-panel-with-limits` vers `main`
- Pipeline se déclenche automatiquement
- Rebuild backend + frontend
- Redémarrage des containers

**Si déploiement manuel :**
- SSH vers le VPS
- `git pull origin main`
- `docker compose -f docker-compose.prod.yml up -d --build`
- Vérifier logs : `docker compose logs -f`

---

# 📝 CHECKLIST FINALE

## Base de Données
- [ ] Migration `role` créée et appliquée
- [ ] Migration `user_limits` créée et appliquée
- [ ] Votre compte défini comme admin
- [ ] Backup DB créé avant migration prod

## Backend
- [ ] Modèle User mis à jour avec `role`
- [ ] Modèle UserLimits créé
- [ ] LimitService implémenté et testé
- [ ] Middleware admin fonctionnel
- [ ] 5 routes admin créées
- [ ] Intégration limites dans routes existantes
- [ ] Service email d'alerte configuré
- [ ] Tests unitaires passent

## Frontend - Admin
- [ ] Layout admin créé avec vérification rôle
- [ ] Dashboard admin avec stats
- [ ] Page gestion utilisateurs
- [ ] Modals : détails, édition limites, suppression
- [ ] Design moderne cohérent

## Frontend - Utilisateur
- [ ] Widget utilisation dans dashboard
- [ ] Modals warning et limite atteinte
- [ ] Intégration checks dans actions
- [ ] Badge utilisation dans header
- [ ] Tests manuels passés

## Déploiement
- [ ] Migrations appliquées en prod
- [ ] Backend redéployé
- [ ] Frontend redéployé
- [ ] Smoke tests en production
- [ ] Email test d'alerte admin reçu

---

# 🎯 RÉSULTAT ATTENDU

## Pour l'Admin (Vous)
1. Page `/admin/dashboard` avec statistiques en temps réel
2. Page `/admin/users` pour gérer tous les utilisateurs
3. Emails automatiques quand un user approche/atteint une limite
4. Pouvoir bloquer/débloquer/supprimer des users
5. Pouvoir augmenter les limites au cas par cas

## Pour les Utilisateurs
1. Widget visible montrant leur utilisation
2. Avertissement progressif avant d'atteindre les limites
3. Blocage clair avec message explicatif
4. Contact facile avec l'admin (email)
5. Expérience non intrusive pour utilisation normale

## Limites Appliquées
- ✅ 50 recherches/jour
- ✅ 50 offres sauvegardées
- ✅ 3 profils max
- ✅ 30 candidatures
- ✅ 5 CV parsés
- ✅ 5 entreprises en veille
- ✅ 4 CV générés/jour

---

# 📅 ESTIMATION TEMPORELLE

## Jour 1 (4h)
- Phase 1 : Base de données (1h)
- Phase 2 : Backend partie 1 (3h)

## Jour 2 (4h)
- Phase 3 : Frontend Admin (2h30)
- Phase 4 : Frontend Utilisateur partie 1 (1h30)

## Jour 3 (1h30)
- Phase 4 : Frontend Utilisateur partie 2 (30 min)
- Phase 5 : Tests et déploiement (1h)

**TOTAL : ~9h30 réparties sur 3 jours**

---

# ✅ PRÊT À COMMENCER

La branche `feature/admin-panel-with-limits` est créée.
Le .gitignore est mis à jour pour exclure les docs.

**Prochaine étape :** Commencer l'implémentation de la Phase 1 (Base de données).

Dites-moi quand vous êtes prêt ! 🚀
