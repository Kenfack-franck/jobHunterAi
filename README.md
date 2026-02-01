# 🎯 Job Hunter AI

Un assistant personnel intelligent pour automatiser la recherche d'emploi et la génération de candidatures personnalisées.

## 📋 Fonctionnalités (V1.0 - MVP)

- ✅ **Authentification sécurisée** (JWT)
- ✅ **Gestion de profil candidat** (expériences, compétences, formations)
- ✅ **Analyse d'offres d'emploi** (scraping LinkedIn/Indeed)
- ✅ **Génération intelligente de CV** (personnalisé par offre)
- ✅ **Génération de lettres de motivation** (IA GPT-4)
- ✅ **Export PDF professionnel**

## 🛠️ Stack Technique

### Backend
- **FastAPI** (Python 3.12) - API REST
- **SQLAlchemy 2.0** - ORM Async
- **PostgreSQL 16** - Base de données
- **Redis** - Cache & tasks queue
- **Alembic** - Migrations
- **OpenAI API** - Génération de contenu

### Frontend
- **Next.js 14** (App Router)
- **React 18**
- **TailwindCSS** - Styling
- **ShadcnUI** - Composants
- **Axios + React Query** - API calls

### DevOps
- **Docker & Docker Compose** - Containerisation
- **Nginx** - Reverse proxy (production)

## 🚀 Installation

### Prérequis

- Docker & Docker Compose
- Node.js 18+ (pour développement frontend local)
- Python 3.12+ (pour développement backend local)

### Démarrage rapide

1. **Cloner le repository**
```bash
git clone <repo-url>
cd job-hunter-ai
```

2. **Configurer les variables d'environnement**
```bash
cp .env.example .env
# Éditer .env et remplir les valeurs (SECRET_KEY, OPENAI_API_KEY, etc.)
```

3. **Générer une clé secrète**
```bash
openssl rand -hex 32
```

4. **Lancer avec Docker Compose**
```bash
docker-compose up --build
```

5. **Accéder à l'application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentation API: http://localhost:8000/docs

## 📁 Structure du projet

```
job-hunter-ai/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── models/       # Modèles SQLAlchemy
│   │   ├── schemas/      # Schémas Pydantic
│   │   ├── api/          # Routes API
│   │   ├── services/     # Logique métier
│   │   ├── core/         # Config & sécurité
│   │   └── tasks/        # Tâches asynchrones
│   └── alembic/          # Migrations DB
├── frontend/             # Application Next.js
│   └── src/
│       ├── app/          # Pages (App Router)
│       ├── components/   # Composants React
│       ├── lib/          # Utilitaires
│       └── types/        # Types TypeScript
├── docker/               # Configurations Docker
└── docker-compose.yml    # Orchestration
```

## 🔧 Développement

### Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

### Migrations de base de données

```bash
cd backend
# Créer une migration
alembic revision --autogenerate -m "Description"

# Appliquer les migrations
alembic upgrade head
```

## 📚 Documentation API

Une fois le backend lancé, accédez à:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🗓️ Roadmap

### V1.0 - MVP (Actuel)
- Profil unique par utilisateur
- Analyse manuelle d'offres (URL)
- Génération CV/LM basique

### V2.0 - Intelligence
- Upload et parsing de CV PDF
- Profils multiples (variantes)
- Matching sémantique (pgvector)
- Recherche d'offres intégrée

### V3.0 - Automatisation
- Envoi d'emails automatique
- Journal de candidatures
- Sources personnalisées

### V3.5 - Final
- Conformité RGPD complète
- Templates CV multiples
- Vérification email

## 📄 Licence

Propriétaire - Tous droits réservés

## 👥 Équipe

Développé avec ❤️ pour automatiser la recherche d'emploi
