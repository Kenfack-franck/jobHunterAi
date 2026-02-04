# 🛡️ Configuration Admin en Production

## 📋 Problème

Le compte admin créé en local n'existe pas sur le serveur de production. Il faut un moyen sécurisé de créer un admin sur le serveur.

---

## ✅ Solution 1: Script Python CLI (Recommandé)

### Étapes pour créer un admin en production

#### 1. Créer d'abord un compte utilisateur normal

Allez sur votre site en production:
```
https://votre-domaine.com/auth/register
```

Créez un compte avec votre email (ex: `kenfackfranck08@gmail.com`)

#### 2. Promouvoir ce compte en admin via Docker

Connectez-vous en SSH sur votre serveur et exécutez:

```bash
# Si vous utilisez docker compose
docker compose exec backend python scripts/create_admin.py --email kenfackfranck08@gmail.com

# OU si vous utilisez docker-compose (ancien)
docker-compose exec backend python scripts/create_admin.py --email kenfackfranck08@gmail.com
```

#### 3. Vérifier les admins

```bash
docker compose exec backend python scripts/create_admin.py --list
```

#### 4. Accéder au panel admin

Connectez-vous sur votre site et accédez à:
```
https://votre-domaine.com/admin
```

Le lien "🛡️ Admin Panel" apparaîtra dans la sidebar.

---

## 📝 Solution 2: SQL Direct (Alternative)

Si vous avez accès à PostgreSQL en direct:

### Via Docker

```bash
# Accéder au container PostgreSQL
docker compose exec postgres psql -U jobhunter -d jobhunter_db

# Exécuter le SQL
UPDATE users 
SET role = 'admin' 
WHERE email = 'kenfackfranck08@gmail.com';

-- Vérifier
SELECT email, full_name, role, is_active FROM users WHERE role = 'admin';

-- Quitter
\q
```

### Via fichier SQL

```bash
# Copier le script dans le container
docker cp backend/scripts/set_admin_role.sql postgres:/tmp/

# Exécuter le script (après l'avoir modifié avec votre email)
docker compose exec postgres psql -U jobhunter -d jobhunter_db -f /tmp/set_admin_role.sql
```

---

## 🔒 Solution 3: Variable d'environnement (Future)

Pour automatiser, vous pouvez ajouter dans `.env`:

```bash
# Admin initial (sera créé au premier démarrage si n'existe pas)
FIRST_ADMIN_EMAIL=kenfackfranck08@gmail.com
FIRST_ADMIN_PASSWORD=VotreMotDePasseSecurise123!
```

**Note**: Cette fonctionnalité nécessite un script de démarrage supplémentaire (non implémenté actuellement).

---

## 📊 Comparaison des Solutions

| Solution | Sécurité | Facilité | Automatique | Recommandé |
|----------|----------|----------|-------------|------------|
| **Script Python** | ✅✅✅ | ✅✅✅ | ✅ | **OUI** |
| **SQL Direct** | ✅✅ | ✅✅ | ❌ | Si besoin |
| **Var ENV** | ✅ | ✅✅✅ | ✅✅✅ | Future |

---

## 🛠️ Script Python - Détails

### Fonctionnalités

Le script `scripts/create_admin.py` permet:

1. **Promouvoir un user en admin** (sans toucher au mot de passe)
2. **Lister tous les admins**
3. **Vérifier si déjà admin**
4. **Messages clairs** sur le statut

### Avantages

- ✅ **Sécurisé**: Pas de mot de passe par défaut
- ✅ **Simple**: Une seule commande
- ✅ **Idempotent**: Peut être réexécuté sans problème
- ✅ **Production-ready**: Fonctionne avec Docker
- ✅ **Logs clairs**: Messages de confirmation

### Usage

```bash
# Promouvoir un user
python scripts/create_admin.py --email user@example.com

# Lister les admins
python scripts/create_admin.py --list

# Aide
python scripts/create_admin.py --help
```

### Output Exemple

```
✅ Successfully promoted 'kenfackfranck08@gmail.com' to admin role!
   Name: Kenfack Franck
   Active: True

🎯 You can now access the admin panel at: https://votre-domaine.com/admin
```

---

## 🚀 Processus de Déploiement

### Workflow recommandé pour le premier déploiement

```bash
# 1. Déployer l'application
docker compose up -d

# 2. Vérifier que tout fonctionne
curl https://votre-domaine.com/api/v1/health

# 3. Créer un compte admin depuis l'interface web
# Aller sur https://votre-domaine.com/auth/register
# Email: kenfackfranck08@gmail.com
# Password: <votre-mot-de-passe-sécurisé>

# 4. Promouvoir en admin via script
docker compose exec backend python scripts/create_admin.py --email kenfackfranck08@gmail.com

# 5. Vérifier
docker compose exec backend python scripts/create_admin.py --list

# 6. Se connecter et accéder à /admin
```

---

## 🔐 Sécurité

### Bonnes Pratiques

1. **Ne jamais commiter** de mots de passe admin dans le code
2. **Utiliser un mot de passe fort** (12+ caractères, mixte)
3. **Limiter le nombre d'admins** (1-2 maximum recommandé)
4. **Logs d'actions** : Toutes les actions admin sont loguées
5. **2FA recommandé** (à implémenter dans une version future)

### Protection Admin Panel

Le panel admin est protégé par:
- ✅ JWT avec rôle `admin` dans le token
- ✅ Middleware `require_admin()` sur toutes les routes
- ✅ Vérification côté frontend (sidebar + routes)
- ✅ Vérification côté backend (FastAPI dependencies)

---

## 🐛 Troubleshooting

### Erreur: "User not found"

```bash
# Vérifier que le compte existe
docker compose exec postgres psql -U jobhunter -d jobhunter_db \
  -c "SELECT email, full_name FROM users WHERE email = 'votre@email.com';"
```

**Solution**: Créez d'abord le compte via `/auth/register`

---

### Erreur: "Cannot connect to database"

```bash
# Vérifier que le backend peut accéder à la DB
docker compose logs backend | grep -i database
docker compose logs postgres
```

**Solution**: Vérifiez `DATABASE_URL` dans `.env`

---

### Panel admin non visible après promotion

1. **Déconnectez-vous** de l'application
2. **Reconnectez-vous** (pour régénérer le JWT avec le role admin)
3. Le lien "🛡️ Admin Panel" devrait apparaître dans la sidebar

---

## 📞 Support

Pour toute question sur la configuration admin:
1. Consulter ce guide
2. Vérifier les logs Docker: `docker compose logs backend`
3. Tester le script en local d'abord
4. Contacter: kenfackfranck08@gmail.com

---

## ✅ Checklist de Setup Admin

- [ ] Application déployée et fonctionnelle
- [ ] Compte utilisateur créé via `/auth/register`
- [ ] Script `create_admin.py` exécuté avec succès
- [ ] Commande `--list` montre l'admin
- [ ] Déconnexion puis reconnexion
- [ ] Lien "🛡️ Admin Panel" visible dans sidebar
- [ ] Accès à `/admin` fonctionne
- [ ] Accès à `/admin/users` fonctionne
- [ ] Filtres et actions admin testés

---

**Date**: 2026-02-04  
**Version**: 1.0  
**Auteur**: Job Hunter AI Team
