# 🚀 Guide Complet de Déploiement Job Hunter AI sur VPS

## 📋 Vue d'ensemble

**Architecture** : Full-Stack avec 5 conteneurs Docker
- Frontend Next.js (port 3000)
- Backend FastAPI (port 8000)
- PostgreSQL + pgvector (port 5432)
- Redis (port 6379)
- Celery Worker (tâches async)

**Domaines nécessaires** :
- `jobhunter.franckkenfack.works` → Frontend
- `api.jobhunter.franckkenfack.works` → Backend API

---

## ✅ ÉTAPE 1 : Installation Infrastructure VPS (Une seule fois)

### Sur votre PC local

1. **Transférer le script sur le VPS** :
```bash
scp deploy/vps-setup.sh ubuntu@152.228.128.95:~/
```

2. **Se connecter au VPS** :
```bash
ssh ubuntu@152.228.128.95
```

### Sur le VPS

3. **Exécuter le script d'installation** :
```bash
chmod +x ~/vps-setup.sh
./vps-setup.sh
```

Ce script installe :
- ✅ Docker + Docker Compose
- ✅ Réseau Docker `web_net`
- ✅ Dossiers de travail (`~/jobhunter`)
- ✅ Firewall (ports 22, 80, 443)

4. **Redémarrage (important)** :
```bash
sudo reboot
```

Attendez 1 minute puis reconnectez-vous.

5. **Vérifier l'installation** :
```bash
docker --version
docker compose version
docker network ls | grep web_net
```

Résultat attendu :
```
Docker version 24.x.x
Docker Compose version v2.x.x
web_net   bridge   local
```

---

## ✅ ÉTAPE 2 : Configuration Caddy (Reverse Proxy)

### Sur le VPS

1. **Créer le fichier `~/proxy/docker-compose.yml`** :
```bash
nano ~/proxy/docker-compose.yml
```

Coller :
```yaml
version: '3.8'

services:
  caddy:
    image: caddy:2-alpine
    container_name: caddy_proxy
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - ./data:/data
      - ./config:/config
    networks:
      - web_net

networks:
  web_net:
    external: true
```

2. **Créer le `~/proxy/Caddyfile`** :
```bash
nano ~/proxy/Caddyfile
```

Coller :
```
# Frontend Job Hunter AI
jobhunter.franckkenfack.works {
    reverse_proxy jobhunter-frontend:3000
}

# Backend API Job Hunter AI
api.jobhunter.franckkenfack.works {
    reverse_proxy jobhunter-backend:8000
}

# Portainer (optionnel)
portainer.franckkenfack.works {
    reverse_proxy portainer:9000
}
```

3. **Démarrer Caddy** :
```bash
cd ~/proxy
docker compose up -d
```

4. **Vérifier** :
```bash
docker ps | grep caddy
curl -I http://localhost
```

Résultat attendu : `HTTP/1.1 502 Bad Gateway` (normal, les apps ne tournent pas encore)

---

## ✅ ÉTAPE 3 : Configuration DNS

### Sur OVH (ou votre DNS provider)

Ajouter 2 enregistrements DNS de type **A** :

| Nom | Type | Valeur | TTL |
|-----|------|--------|-----|
| `jobhunter` | A | `152.228.128.95` | 300 |
| `api.jobhunter` | A | `152.228.128.95` | 300 |

**Attendre 5-10 minutes** pour propagation DNS.

**Vérifier** :
```bash
# Sur votre PC
nslookup jobhunter.franckkenfack.works
nslookup api.jobhunter.franckkenfack.works
```

Les 2 doivent répondre `152.228.128.95`.

---

## ✅ ÉTAPE 4 : Préparation du Projet (Sur votre PC)

### 4.1 Modifier `frontend/next.config.ts`

Ajouter `output: "standalone"` :
```typescript
const nextConfig: NextConfig = {
  output: "standalone",  // ← Ajouter cette ligne
  // ... reste de la config
};
```

### 4.2 Créer les Dockerfiles de production

**Créer `frontend/Dockerfile.prod`** :
```dockerfile
# frontend/Dockerfile.prod
FROM node:20-alpine AS base

# Dépendances
FROM base AS deps
WORKDIR /app
RUN apk add --no-cache libc6-compat
COPY package.json package-lock.json* ./
RUN npm ci

# Build
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1

# Variables d'environnement pour le build (API URL publique)
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

RUN npm run build

# Production
FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

**Créer `backend/Dockerfile.prod`** :
```dockerfile
# backend/Dockerfile.prod
FROM python:3.11-slim

WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code application
COPY app ./app

# Variables d'environnement par défaut
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4.3 Créer `docker-compose.prod.yml`

Ce fichier sera utilisé **SUR LE VPS** par le CI/CD.

```yaml
version: '3.8'

services:
  # PostgreSQL
  postgres:
    image: ankane/pgvector:latest
    container_name: jobhunter-postgres
    restart: always
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-jobhunter_db}
      POSTGRES_USER: ${POSTGRES_USER:-jobhunter}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - jobhunter_internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U jobhunter"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis
  redis:
    image: redis:7-alpine
    container_name: jobhunter-redis
    restart: always
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - jobhunter_internal
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  # Backend FastAPI
  backend:
    image: ${CI_REGISTRY_IMAGE}/backend:${IMAGE_TAG:-latest}
    container_name: jobhunter-backend
    restart: always
    environment:
      - DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
      - SECRET_KEY=${SECRET_KEY}
      - ALGORITHM=${ALGORITHM:-HS256}
      - ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES:-30}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - RAPIDAPI_KEY=${RAPIDAPI_KEY}
      - CORS_ORIGINS=${CORS_ORIGINS}
      - ENVIRONMENT=production
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - jobhunter_internal
      - web_net
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Celery Worker
  celery:
    image: ${CI_REGISTRY_IMAGE}/backend:${IMAGE_TAG:-latest}
    container_name: jobhunter-celery
    restart: always
    command: celery -A app.celery_app worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - RAPIDAPI_KEY=${RAPIDAPI_KEY}
    depends_on:
      - backend
      - redis
    networks:
      - jobhunter_internal

  # Frontend Next.js
  frontend:
    image: ${CI_REGISTRY_IMAGE}/frontend:${IMAGE_TAG:-latest}
    container_name: jobhunter-frontend
    restart: always
    environment:
      - NEXT_PUBLIC_API_URL=https://api.jobhunter.franckkenfack.works
    depends_on:
      - backend
    networks:
      - web_net
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  jobhunter_internal:
    driver: bridge
  web_net:
    external: true

volumes:
  postgres_data:
  redis_data:
```

### 4.4 Créer `.dockerignore`

```
node_modules
.next
.git
.env*
*.md
__pycache__
*.pyc
.pytest_cache
```

---

## ✅ ÉTAPE 5 : Configuration GitLab CI/CD

### 5.1 Créer `.gitlab-ci.yml`

```yaml
stages:
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

# Build Frontend
build_frontend:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - cd frontend
    - docker build 
        --build-arg NEXT_PUBLIC_API_URL=https://api.jobhunter.franckkenfack.works 
        -f Dockerfile.prod 
        -t $CI_REGISTRY_IMAGE/frontend:latest 
        .
    - docker push $CI_REGISTRY_IMAGE/frontend:latest
  only:
    - main

# Build Backend
build_backend:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - cd backend
    - docker build 
        -f Dockerfile.prod 
        -t $CI_REGISTRY_IMAGE/backend:latest 
        .
    - docker push $CI_REGISTRY_IMAGE/backend:latest
  only:
    - main

# Déploiement
deploy_production:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache openssh-client
    - eval $(ssh-agent -s)
    - echo "$SSH_PRIVATE_KEY" | base64 -d | ssh-add -
    - mkdir -p ~/.ssh
    - chmod 700 ~/.ssh
    - ssh-keyscan $SSH_IP >> ~/.ssh/known_hosts
  script:
    - echo "🚀 Déploiement Job Hunter AI..."
    # Créer fichier .env sur le serveur
    - |
      ssh $SSH_USER@$SSH_IP "cat > ~/jobhunter/.env << EOF
      POSTGRES_DB=jobhunter_db
      POSTGRES_USER=jobhunter
      POSTGRES_PASSWORD=$POSTGRES_PASSWORD
      SECRET_KEY=$SECRET_KEY
      OPENAI_API_KEY=$OPENAI_API_KEY
      GEMINI_API_KEY=$GEMINI_API_KEY
      RAPIDAPI_KEY=$RAPIDAPI_KEY
      CORS_ORIGINS=https://jobhunter.franckkenfack.works
      CI_REGISTRY_IMAGE=$CI_REGISTRY_IMAGE
      IMAGE_TAG=latest
      EOF"
    # Pull et démarrage
    - ssh $SSH_USER@$SSH_IP "
        cd ~/jobhunter &&
        docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY &&
        docker compose -f docker-compose.prod.yml pull &&
        docker compose -f docker-compose.prod.yml up -d
      "
  only:
    - main
  environment:
    name: production
    url: https://jobhunter.franckkenfack.works
```

### 5.2 Transférer `docker-compose.prod.yml` sur le VPS

```bash
scp docker-compose.prod.yml ubuntu@152.228.128.95:~/jobhunter/
```

---

## ✅ ÉTAPE 6 : Configuration GitLab (Secrets)

Aller sur **GitLab > Votre Projet > Settings > CI/CD > Variables**

Ajouter ces variables (**Protected** + **Masked** sauf SSH_PRIVATE_KEY) :

| Clé | Valeur | Type |
|-----|--------|------|
| `SSH_IP` | `152.228.128.95` | Variable |
| `SSH_USER` | `ubuntu` | Variable |
| `SSH_PRIVATE_KEY` | Votre clé privée en Base64 | Variable (ne PAS masquer) |
| `POSTGRES_PASSWORD` | Mot de passe sécurisé | Variable (masqué) |
| `SECRET_KEY` | Clé secrète JWT (32+ chars) | Variable (masqué) |
| `OPENAI_API_KEY` | Votre clé OpenAI | Variable (masqué) |
| `GEMINI_API_KEY` | Votre clé Gemini | Variable (masqué) |
| `RAPIDAPI_KEY` | Votre clé RapidAPI (JSearch) | Variable (masqué) |

### Génération de la clé SSH

**Sur votre PC** :
```bash
# Générer clé SSH dédiée CI/CD
ssh-keygen -t ed25519 -C "gitlab-ci-jobhunter" -f ~/.ssh/gitlab_jobhunter_key

# Copier la clé publique sur le VPS
ssh-copy-id -i ~/.ssh/gitlab_jobhunter_key.pub ubuntu@152.228.128.95

# Encoder la clé privée en Base64
base64 -w 0 ~/.ssh/gitlab_jobhunter_key
```

Copier la sortie (longue chaîne) dans la variable `SSH_PRIVATE_KEY` GitLab.

---

## ✅ ÉTAPE 7 : Déploiement

### 7.1 Commit et Push

```bash
git add .
git commit -m "feat: Production deployment configuration"
git push origin main
```

### 7.2 Surveiller le Pipeline

Aller sur **GitLab > CI/CD > Pipelines**

Vérifier :
- ✅ Build frontend (5-10 min)
- ✅ Build backend (3-5 min)
- ✅ Deploy production (2-3 min)

### 7.3 Vérifier le déploiement

**Sur le VPS** :
```bash
ssh ubuntu@152.228.128.95
cd ~/jobhunter
docker compose ps
```

Résultat attendu : **5 conteneurs running**
```
jobhunter-frontend   Up   3000/tcp
jobhunter-backend    Up   8000/tcp
jobhunter-postgres   Up   5432/tcp
jobhunter-redis      Up   6379/tcp
jobhunter-celery     Up   
```

### 7.4 Tester l'application

```bash
# Frontend
curl -I https://jobhunter.franckkenfack.works

# Backend API
curl https://api.jobhunter.franckkenfack.works/health
```

Résultats attendus :
- Frontend : `HTTP/2 200` + page HTML
- Backend : `{"status":"healthy"}`

---

## ✅ ÉTAPE 8 : Initialisation Base de Données

**Sur le VPS** :
```bash
# Créer les tables
docker exec jobhunter-backend python -c "
from app.database import engine, Base
Base.metadata.create_all(bind=engine)
print('✅ Tables créées')
"
```

---

## 🎉 CHECKLIST FINALE

- [ ] DNS configuré (jobhunter + api.jobhunter)
- [ ] Caddy configuré et démarré
- [ ] Variables GitLab ajoutées (8 variables)
- [ ] Pipeline GitLab vert ✅
- [ ] 5 conteneurs running sur le VPS
- [ ] Frontend accessible : https://jobhunter.franckkenfack.works
- [ ] Backend API répond : https://api.jobhunter.franckkenfack.works/health
- [ ] Tables DB créées

---

## 🐛 Dépannage

### Frontend affiche 502
```bash
docker logs jobhunter-frontend
# Vérifier NEXT_PUBLIC_API_URL
```

### Backend ne répond pas
```bash
docker logs jobhunter-backend
# Vérifier DATABASE_URL et REDIS_URL
```

### Base de données ne démarre pas
```bash
docker logs jobhunter-postgres
# Vérifier les permissions du volume
sudo chown -R 999:999 ~/jobhunter/data/postgres
```

### Celery ne traite pas les tâches
```bash
docker logs jobhunter-celery
# Vérifier connexion Redis
```

---

## 📊 Monitoring

**Logs en temps réel** :
```bash
# Tous les conteneurs
docker compose -f ~/jobhunter/docker-compose.prod.yml logs -f

# Un service spécifique
docker logs -f jobhunter-backend
```

**Redémarrage** :
```bash
cd ~/jobhunter
docker compose -f docker-compose.prod.yml restart
```

**Mise à jour** :
```bash
# Juste pousser sur main, GitLab CI/CD gère tout
git push origin main
```

---

## 🚀 Optimisations Futures

1. **SSL/TLS** : Déjà géré automatiquement par Caddy (Let's Encrypt)
2. **Backup DB** : Ajouter cron job pour `pg_dump`
3. **Monitoring** : Installer Grafana + Prometheus
4. **Logs centralisés** : Utiliser Loki
5. **Scaling** : Ajouter plusieurs workers Celery si nécessaire

---

**Temps total estimé** : 2-3 heures  
**Coût** : Gratuit (sauf VPS que vous avez déjà)
