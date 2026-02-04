# 🔐 Plan Admin Panel - Simple & Efficace

## 🎯 Objectif
Créer une interface admin pour contrôler l'accès au site et gérer les utilisateurs.

---

## 📋 Fonctionnalités Nécessaires

### ✅ Ce que l'admin peut faire :
1. **Voir la liste de tous les utilisateurs**
   - Email, nom, date d'inscription, statut
2. **Bloquer/Débloquer un utilisateur**
   - Utilisateur bloqué = ne peut plus se connecter
3. **Supprimer un utilisateur**
   - Efface le compte et toutes ses données
4. **Voir des statistiques basiques**
   - Nombre d'utilisateurs, inscriptions récentes, etc.

---

## 🔧 Ce qu'il faut AJOUTER

### **1. BASE DE DONNÉES** (1 modification)

**Table `users` - Ajouter 1 colonne :**
```sql
ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user';
-- Valeurs possibles : 'user' ou 'admin'
```

**Explication :**
- Tous les users normaux ont `role = 'user'`
- Vous (admin) aurez `role = 'admin'`
- On vérifie ce rôle pour accéder à `/admin`

---

### **2. BACKEND** (3 endpoints API)

**Fichier à créer : `backend/app/api/admin.py`**

```python
# 3 endpoints simples :

1. GET /api/v1/admin/users
   → Liste tous les utilisateurs
   → Filtre : actifs, bloqués, recherche par email

2. PUT /api/v1/admin/users/{id}/toggle-active
   → Bloquer ou débloquer un utilisateur
   → Change is_active entre True/False

3. DELETE /api/v1/admin/users/{id}
   → Supprimer complètement un utilisateur
   → ⚠️ Supprime aussi ses profils, offres, etc.
```

**Sécurité :**
- Middleware qui vérifie `current_user.role == 'admin'`
- Si pas admin → erreur 403 Forbidden

---

### **3. FRONTEND** (2 pages)

#### **Page 1 : `/admin/users` - Gestion des utilisateurs**

```
┌────────────────────────────────────────────────────────┐
│  👥 Gestion des Utilisateurs                           │
├────────────────────────────────────────────────────────┤
│  🔍 Recherche : [_________________]  [🔄 Actualiser]   │
│                                                         │
│  Email              | Inscrit le | Statut   | Actions  │
│  ──────────────────────────────────────────────────────│
│  jean@test.fr       | 03/02/26   | ✅ Actif  | 🔴 Bloquer│
│  marie@test.fr      | 02/02/26   | 🔴 Bloqué| ✅ Activer │
│  paul@test.fr       | 01/02/26   | ✅ Actif  | 🗑️ Supprimer│
│                                                         │
│  📄 Page 1 sur 5    [< Précédent] [Suivant >]         │
└────────────────────────────────────────────────────────┘
```

**Fonctionnalités :**
- Tableau avec tous les utilisateurs
- Barre de recherche par email
- Boutons : Bloquer/Activer + Supprimer
- Pagination (20 users par page)
- Badge coloré pour le statut

---

#### **Page 2 : `/admin/dashboard` - Statistiques**

```
┌────────────────────────────────────────────────────────┐
│  📊 Dashboard Admin                                     │
├────────────────────────────────────────────────────────┤
│                                                         │
│  📈 STATISTIQUES RAPIDES                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐│
│  │ 247 Users    │  │ 23 Nouveaux  │  │ 3 Bloqués    ││
│  │ Total        │  │ Cette semaine│  │              ││
│  └──────────────┘  └──────────────┘  └──────────────┘│
│                                                         │
│  📅 INSCRIPTIONS (7 derniers jours)                    │
│  ┌────────────────────────────────────────────────────┐│
│  │  Lun  Mar  Mer  Jeu  Ven  Sam  Dim                ││
│  │   5    8    12   7    15   3    2   (graphique)   ││
│  └────────────────────────────────────────────────────┘│
│                                                         │
│  👤 DERNIERS INSCRITS                                  │
│  • jean@test.fr - Il y a 2 heures                     │
│  • marie@test.fr - Il y a 5 heures                    │
│  • paul@test.fr - Hier                                │
│                                                         │
└────────────────────────────────────────────────────────┘
```

---

### **4. NAVIGATION** (1 lien dans le menu)

**Si l'utilisateur est admin, afficher dans le menu :**
```tsx
{user.role === 'admin' && (
  <Link href="/admin">
    <Button>🔐 Admin Panel</Button>
  </Link>
)}
```

---

## 🚀 PLAN D'ACTION

### **Étape 1 : Base de données** (5 min)
- [ ] Ajouter colonne `role` à la table users
- [ ] Mettre votre compte en `role='admin'`

### **Étape 2 : Backend** (1h30)
- [ ] Créer fichier `backend/app/api/admin.py`
- [ ] 3 endpoints : list, toggle-active, delete
- [ ] Middleware de vérification admin
- [ ] Ajouter les routes dans main.py

### **Étape 3 : Frontend** (1h30)
- [ ] Créer page `/admin/dashboard`
- [ ] Créer page `/admin/users`
- [ ] Créer composants : UserTable, UserCard, StatsCard
- [ ] Ajouter lien admin dans le menu (si role=admin)

### **Étape 4 : Tests** (30 min)
- [ ] Tester blocage d'un user
- [ ] Tester suppression d'un user
- [ ] Vérifier qu'un user normal ne peut pas accéder à /admin

---

## 💡 BONUS (Optionnel - plus tard)

Si vous voulez aller plus loin :
- Export CSV de la liste des users
- Logs d'actions admin (qui a fait quoi)
- Statistiques avancées (graphiques)
- Filtres avancés (par date, par statut)

---

## 🎨 Design

On utilise le même design moderne que le reste de l'app :
- Gradients bleu/violet/rose
- Cards avec hover effects
- Icons Lucide-react
- Responsive mobile

---

## ⏱️ Temps Estimé Total

- **Backend** : 1h30
- **Frontend** : 1h30
- **Tests** : 30 min
- **TOTAL** : ~3 heures

---

## ❓ Questions Importantes

1. **Validation des inscriptions ?**
   - NON pour l'instant → Users actifs dès l'inscription
   - Vous pouvez les bloquer manuellement après si besoin

2. **Notifications admin ?**
   - NON pour l'instant → Vous devez aller vérifier manuellement
   - Peut être ajouté plus tard (email quand nouvel user)

3. **Logs des actions ?**
   - NON pour l'instant → Actions non tracées
   - Peut être ajouté plus tard si besoin

---

## ✅ Résultat Final

Vous aurez un panel admin simple où vous pouvez :
1. ✅ Voir tous les utilisateurs
2. ✅ Bloquer un utilisateur (il ne peut plus se connecter)
3. ✅ Supprimer un utilisateur
4. ✅ Voir les stats basiques

**C'est simple, rapide, et ça fait le job ! 🚀**
