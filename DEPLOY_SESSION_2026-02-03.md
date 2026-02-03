# 🚀 Déploiement Version 2026-02-03 - Guide Complet

## 📋 Résumé des Changements

Cette version contient les améliorations suivantes :
- ✅ **Design responsive complet** (mobile, tablette, desktop)
- ✅ **Sidebar fixe** (ne bouge plus entre les pages)
- ✅ **Footer qui défile** avec le contenu
- ✅ **Page Contact supprimée** (intégrée dans FeedbackButton)
- ✅ **Barre de recherche supprimée** du header
- ✅ **Settings page fonctionnelle** (save + persist + change password)
- ✅ **Endpoints API ajoutés** : PUT /auth/me, PUT /auth/me/password, DELETE /auth/me, GET /auth/me/export
- ✅ **Nouvelle page Sources** (/settings/sources)
- ✅ **Tables DB ajoutées** : user_source_preferences, search_results_cache
- ✅ **Menu hamburger mobile** avec Sheet drawer

## ⚠️ Changements Importants pour le Déploiement

### 1. **Nouvelles Dépendances Frontend**
```json
"@radix-ui/react-tabs": "^1.1.13"  // Upgraded from 1.0.4
"@radix-ui/react-dialog": "^1.0.x"  // Pour Sheet component
```

### 2. **Nouvelles Migrations Base de Données**
```bash
# Deux nouvelles migrations à appliquer
- 2026_02_02_2144-973f0a15e9d8_add_user_source_preferences_table.py
- 2026_02_02_2235-29ca0abe9c64_add_search_results_cache_table.py
```

### 3. **Nouveaux Fichiers Backend**
```
backend/app/api/sources.py                    # Nouvelle route /sources
backend/app/models/user_source_preferences.py # Nouveau modèle
backend/app/models/search_cache.py            # Nouveau modèle
backend/app/schemas/source_preferences.py     # Nouveaux schémas
backend/app/services/search_cache_service.py  # Nouveau service
backend/app/core/predefined_sources.py        # Sources prédéfinies
```

### 4. **Fichiers Frontend Supprimés**
```
frontend/src/app/contact/page.tsx  # ❌ SUPPRIMÉ (duplication)
```

### 5. **Nouveaux Composants Frontend**
```
frontend/src/components/ui/sheet.tsx          # Menu mobile drawer
frontend/src/components/ui/tabs.tsx           # Tabs pour sources
frontend/src/components/feedback/FeedbackButton.tsx  # Feedback global
frontend/src/app/settings/sources/page.tsx    # Page sources
```

---

## 🔧 Checklist de Déploiement

### ✅ AVANT de Pousser sur GitLab

1. **Vérifier que tous les fichiers sont commités**
   ```bash
   git status
   git add .
   git commit -m "feat: Responsive design + Settings fixes + New endpoints"
   ```

2. **Vérifier les variables d'environnement**
   ```bash
   # S'assurer que .env contient toutes les clés
   cat .env | grep -E "SECRET_KEY|OPENAI_API_KEY|SMTP|DATABASE_URL"
   ```

3. **Tester en local une dernière fois**
   ```bash
   docker compose down -v
   docker compose up --build
   # Tester : Settings, Sources, Mobile menu, Footer scroll
   ```

---

## 🚀 Procédure de Déploiement GitLab

### Étape 1 : Pousser sur GitLab

```bash
# Ajouter le remote GitLab si pas encore fait
git remote add gitlab https://gitlab.com/VOTRE_USERNAME/job-hunter-ai.git

# Ou si déjà configuré
git push gitlab main
```

### Étape 2 : GitLab CI/CD s'exécute automatiquement

Le pipeline va :
1. **Build Frontend** (si `frontend/**` a changé) ✅ OUI
2. **Build Backend** (si `backend/**` a changé) ✅ OUI  
3. **Deploy Frontend** (après build réussi)
4. **Deploy Backend** (après build réussi)

**⏱️ Temps estimé : 8-12 minutes**

### Étape 3 : Vérifier le Pipeline

```
GitLab → Votre Projet → CI/CD → Pipelines
```

**Statuts attendus :**
- ✅ build_frontend → ✅ deploy_frontend
- ✅ build_backend → ✅ deploy_backend

---

## 🔍 Post-Déploiement : Vérifications

### 1. **SSH dans le VPS**

```bash
ssh ubuntu@152.228.128.95
cd ~/jobhunter
```

### 2. **Appliquer les Migrations DB**

```bash
# Entrer dans le conteneur backend
docker compose -f docker-compose.prod.yml exec backend bash

# Appliquer les migrations
alembic upgrade head

# Vérifier les tables
python -c "
from app.database import engine
from sqlalchemy import inspect
inspector = inspect(engine)
print('Tables:', inspector.get_table_names())
"

# Sortir
exit
```

### 3. **Vérifier les Conteneurs**

```bash
docker compose -f docker-compose.prod.yml ps

# Devrait afficher :
# ✅ jobhunter-frontend    (port 3000)
# ✅ jobhunter-backend     (port 8000)
# ✅ jobhunter-postgres    (port 5432)
# ✅ jobhunter-redis       (port 6379)
# ✅ jobhunter-celery      (pas de port)
```

### 4. **Vérifier les Logs**

```bash
# Backend
docker compose -f docker-compose.prod.yml logs backend --tail=50

# Frontend
docker compose -f docker-compose.prod.yml logs frontend --tail=50

# Chercher des erreurs
docker compose -f docker-compose.prod.yml logs | grep -i error
```

### 5. **Tester l'API Backend**

```bash
# Health check
curl https://api.jobhunter.franckkenfack.works/health

# Documentation
curl https://api.jobhunter.franckkenfack.works/docs

# Test endpoint /auth/me (devrait retourner 401 sans token)
curl https://api.jobhunter.franckkenfack.works/api/v1/auth/me
# Réponse attendue: {"detail":"Not authenticated"}
```

### 6. **Tester le Frontend**

```bash
# Homepage
curl -I https://jobhunter.franckkenfack.works
# Devrait retourner : HTTP/2 200

# Vérifier le responsive
# Ouvrir dans navigateur avec DevTools (F12)
# Tester : Mobile (375px), Tablet (768px), Desktop (1920px)
```

---

## 🧪 Tests Fonctionnels à Faire

### 1. **Responsive Design** ✅
- [ ] Ouvrir https://jobhunter.franckkenfack.works sur mobile
- [ ] Vérifier menu hamburger fonctionne
- [ ] Tester navigation entre pages
- [ ] Vérifier textes adaptés (ex: "Dashboard" vs "Mon Dashboard")

### 2. **Sidebar Fixe** ✅
- [ ] Se connecter au dashboard
- [ ] Cliquer sur différentes pages (Dashboard → Jobs → Profile)
- [ ] ✅ Sidebar ne bouge pas (reste fixe à gauche)
- [ ] ✅ Footer défile avec le contenu

### 3. **Settings Page** ✅
- [ ] Aller dans /settings
- [ ] Changer le nom → Enregistrer
- [ ] Recharger la page
- [ ] ✅ Le nom est persistant
- [ ] Tester changement de mot de passe
- [ ] ✅ Pas d'erreur 500

### 4. **Sources Page** ✅
- [ ] Aller dans /settings/sources
- [ ] Vérifier liste des 17 sources
- [ ] Activer/désactiver des sources
- [ ] Enregistrer
- [ ] ✅ Préférences sauvegardées

### 5. **Feedback Button** ✅
- [ ] Vérifier bouton flottant en bas à droite
- [ ] Cliquer dessus
- [ ] Vérifier coordonnées affichées
- [ ] Envoyer un test
- [ ] ✅ Email reçu

### 6. **Menu Mobile** ✅
- [ ] Réduire fenêtre < 1024px
- [ ] Vérifier menu hamburger apparaît
- [ ] Cliquer dessus
- [ ] ✅ Drawer slide depuis la gauche
- [ ] Vérifier toutes les options de navigation

---

## 🐛 Dépannage

### Problème : Migrations échouent

```bash
# Solution : Reset et recréer
docker compose -f docker-compose.prod.yml exec backend bash
alembic downgrade base
alembic upgrade head
exit
```

### Problème : Frontend ne se connecte pas au Backend

```bash
# Vérifier les variables d'env
docker compose -f docker-compose.prod.yml exec frontend printenv | grep API_URL
# Doit afficher: NEXT_PUBLIC_API_URL=https://api.jobhunter.franckkenfack.works/api/v1

# Si mauvaise valeur, rebuild
docker compose -f docker-compose.prod.yml build --no-cache frontend
docker compose -f docker-compose.prod.yml up -d frontend
```

### Problème : Sidebar toujours sticky/bouge

```bash
# Vérifier que les derniers fichiers sont déployés
docker compose -f docker-compose.prod.yml exec frontend cat /app/.next/standalone/app/layout.tsx | grep "h-screen"
# Doit contenir: className="flex flex-col h-screen"
```

### Problème : Settings ne sauvegardent pas

```bash
# Vérifier endpoint existe
curl https://api.jobhunter.franckkenfack.works/api/v1/auth/me -X PUT \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Test"}'

# Devrait retourner 200 et user data
```

---

## 📊 Métriques de Succès

Après déploiement, vérifier :
- ✅ Pipeline GitLab : 100% success
- ✅ Conteneurs : 5/5 running
- ✅ Frontend accessible : 200 OK
- ✅ Backend API docs : 200 OK
- ✅ Tests fonctionnels : 6/6 passed
- ✅ Erreurs logs : 0 critical

---

## 🔐 Variables GitLab Requises

**Vérifier que ces 8 variables existent dans GitLab :**

```
CI/CD → Variables → Add Variable
```

| Variable | Type | Protégé | Masqué | Exemple |
|----------|------|---------|--------|---------|
| `SSH_PRIVATE_KEY` | File | ✅ | ✅ | Base64 de la clé SSH |
| `SSH_IP` | Variable | ❌ | ❌ | `152.228.128.95` |
| `SSH_USER` | Variable | ❌ | ❌ | `ubuntu` |
| `SECRET_KEY` | Variable | ✅ | ✅ | 64 caractères hex |
| `OPENAI_API_KEY` | Variable | ✅ | ✅ | `sk-...` |
| `SMTP_PASSWORD` | Variable | ✅ | ✅ | App password Gmail |
| `POSTGRES_PASSWORD` | Variable | ✅ | ✅ | Password fort |
| `ADZUNA_APP_ID` | Variable | ❌ | ✅ | ID Adzuna API |

---

## 📝 Commandes Utiles

```bash
# Voir les logs en temps réel
docker compose -f docker-compose.prod.yml logs -f

# Redémarrer un service
docker compose -f docker-compose.prod.yml restart backend

# Rebuild complet (si problème cache)
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml build --no-cache
docker compose -f docker-compose.prod.yml up -d

# Vérifier l'espace disque
df -h
docker system df

# Nettoyer les images inutilisées
docker system prune -a --volumes
```

---

## ✅ Checklist Finale

- [ ] Code commité sur GitLab main
- [ ] Pipeline GitLab terminé avec succès
- [ ] Migrations DB appliquées
- [ ] 5 conteneurs running
- [ ] Frontend accessible (https)
- [ ] Backend API accessible (https)
- [ ] Tests responsive OK
- [ ] Tests fonctionnels OK
- [ ] Logs sans erreurs critiques
- [ ] Performance acceptable (< 2s load time)

---

## 📞 Support

En cas de problème :
1. Vérifier logs : `docker compose -f docker-compose.prod.yml logs`
2. Vérifier variables GitLab
3. Vérifier DNS (OVH)
4. Vérifier Caddy (reverse proxy)
5. Rollback si nécessaire : `git revert HEAD && git push`

---

**Date de création** : 2026-02-03  
**Version** : v2.3.0 (Responsive + Settings + New Endpoints)  
**Temps de déploiement estimé** : 15-20 minutes
