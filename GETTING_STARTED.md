# 🎯 Job Hunter AI - Guide de Démarrage Rapide

## ✅ Vérification de l'Environnement Terminée

Votre environnement de développement est maintenant **100% configuré** !

---

## 📊 Ce qui a été créé

### Backend (FastAPI)
- ✅ **15 fichiers Python** incluant :
  - Modèles de données (User, Profile, JobOffer, GeneratedDocument)
  - Configuration et connexion DB (SQLAlchemy Async)
  - Système d'authentification JWT
  - Migrations Alembic
  - Dockerfile optimisé avec Playwright

### Frontend (Next.js 14)
- ✅ **Configuration complète** :
  - App Router avec TypeScript
  - TailwindCSS + configuration ShadcnUI
  - Page d'accueil responsive
  - Configuration Docker

### Infrastructure
- ✅ **Docker Compose** avec :
  - PostgreSQL 16 + pgvector
  - Redis 7
  - Backend FastAPI
  - Frontend Next.js
  - Réseaux et volumes configurés

---

## 🚀 Démarrage du Projet

### Option 1 : Script Automatique (Recommandé)

```bash
./setup.sh
```

Ce script va :
1. Construire toutes les images Docker
2. Démarrer PostgreSQL et Redis
3. Exécuter les migrations de base de données
4. Démarrer tous les services

### Option 2 : Étape par Étape

```bash
# 1. Construire les images
docker-compose build

# 2. Démarrer tous les services
docker-compose up -d

# 3. Voir les logs en temps réel
docker-compose logs -f

# 4. (Première fois) Exécuter les migrations
docker-compose exec backend alembic upgrade head
```

---

## 🌐 Accéder aux Services

Une fois lancé, les services sont disponibles sur :

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Interface utilisateur |
| **Backend API** | http://localhost:8000 | API REST |
| **Documentation** | http://localhost:8000/docs | Swagger UI interactif |
| **ReDoc** | http://localhost:8000/redoc | Documentation alternative |
| **PostgreSQL** | localhost:5432 | Base de données |
| **Redis** | localhost:6379 | Cache & Queue |

---

## ⚙️ Configuration Requise

### Variables d'Environnement Importantes

Le fichier `.env` a été créé avec des valeurs par défaut. **Vous devez modifier** :

```bash
# OBLIGATOIRE : Votre clé OpenAI pour la génération de lettres
OPENAI_API_KEY=sk-votre-cle-openai-ici

# RECOMMANDÉ : Changer le mot de passe PostgreSQL en production
DB_PASSWORD=jobhunter_secure_password_2024

# Déjà configuré avec une clé aléatoire
SECRET_KEY=578a757e36cb45468116c5588889853627af926e3c822baccd79dcfb7c1faf80
```

---

## 🧪 Tester l'Installation

### 1. Vérifier que tous les conteneurs sont en cours d'exécution :

```bash
docker-compose ps
```

Vous devriez voir 4 services : `postgres`, `redis`, `backend`, `frontend`

### 2. Tester l'API Backend :

```bash
curl http://localhost:8000/health
```

Réponse attendue : `{"status":"healthy","version":"1.0.0"}`

### 3. Tester le Frontend :

Ouvrez http://localhost:3000 dans votre navigateur.

---

## 📝 Commandes Utiles

### Gestion des Services

```bash
# Démarrer les services
docker-compose up -d

# Arrêter les services
docker-compose down

# Voir les logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Reconstruire après modifications
docker-compose up -d --build

# Redémarrer un service spécifique
docker-compose restart backend
```

### Base de Données

```bash
# Se connecter à PostgreSQL
docker-compose exec postgres psql -U jobhunter -d jobhunter_db

# Créer une migration
docker-compose exec backend alembic revision --autogenerate -m "Description"

# Appliquer les migrations
docker-compose exec backend alembic upgrade head

# Revenir à la migration précédente
docker-compose exec backend alembic downgrade -1
```

### Développement

```bash
# Installer les dépendances Python (dev local)
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Installer les dépendances Node.js (dev local)
cd frontend
npm install
npm run dev
```

---

## 🐛 Dépannage

### Problème : Port déjà utilisé

```bash
# Trouver et arrêter le processus sur le port 8000
lsof -ti:8000 | xargs kill -9

# Ou changer le port dans .env
BACKEND_PORT=8001
```

### Problème : Erreur de connexion à PostgreSQL

```bash
# Vérifier les logs PostgreSQL
docker-compose logs postgres

# Recréer la base de données
docker-compose down -v
docker-compose up -d
```

### Problème : Module Python manquant

```bash
# Reconstruire l'image backend
docker-compose build backend --no-cache
```

---

## 📅 Prochaines Étapes (Phase 1 - Suite)

Maintenant que l'infrastructure est en place, nous allons implémenter :

1. ✅ **Routes d'authentification** (`/api/v1/auth/register`, `/api/v1/auth/login`)
2. ✅ **Schémas Pydantic** pour validation des requêtes
3. ✅ **Pages d'authentification** (Login/Register) dans le frontend
4. ✅ **Client API Axios** avec gestion des tokens
5. ✅ **Tests de bout en bout** (inscription → connexion → token)

**État actuel** : Infrastructure ✅ | Auth ⏳ | Profils ⏳ | Scraping ⏳ | Documents ⏳

---

## 📞 Support

En cas de problème :
1. Vérifier les logs : `docker-compose logs -f`
2. Vérifier le fichier `.env`
3. S'assurer que les ports ne sont pas déjà utilisés
4. Reconstruire les images : `docker-compose build --no-cache`

---

**Version** : 1.0.0  
**Date** : 2026-01-30  
**Status** : Phase 1 Infrastructure ✅ (80% complète)
