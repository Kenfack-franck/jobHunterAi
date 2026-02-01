# 📦 Documentation de Déploiement Job Hunter AI

## 🎯 Fichiers de déploiement créés

```
📁 hackaton/
├── 📄 DEPLOY_QUICK_START.md   ← START HERE (guide rapide 5 étapes)
├── 📄 DEPLOY_GUIDE.md          ← Guide complet détaillé
├── 📄 DEPLOY_CHECKLIST.md      ← Checklist exhaustive
│
├── 📁 deploy/
│   └── 📄 vps-setup.sh         ← Script d'installation VPS
│
├── 📁 frontend/
│   └── 📄 Dockerfile.prod      ← Dockerfile production Next.js
│
├── 📁 backend/
│   └── 📄 Dockerfile.prod      ← Dockerfile production FastAPI
│
├── 📄 docker-compose.prod.yml  ← Orchestration 5 services
├── 📄 .gitlab-ci.yml           ← Pipeline CI/CD
└── 📄 .dockerignore            ← Fichiers à exclure
```

---

## 🚀 Par où commencer ?

### Pour les pressés (2-3h)
👉 **Lire `DEPLOY_QUICK_START.md`**
- Guide en 5 étapes
- Commandes ready-to-copy
- Va droit au but

### Pour la compréhension complète
👉 **Lire `DEPLOY_GUIDE.md`**
- Explications détaillées de chaque étape
- Contexte et architecture
- Section dépannage complète

### Pour suivre l'avancement
👉 **Utiliser `DEPLOY_CHECKLIST.md`**
- Cochez chaque étape
- Vérifications à chaque niveau
- Aucune étape oubliée

---

## 📋 Prérequis

### Vous avez besoin de :
- ✅ Un VPS OVH (Ubuntu 24.04) → Vous l'avez déjà
- ✅ Accès SSH au VPS → `ssh ubuntu@152.228.128.95`
- ✅ Un compte GitLab → gratuit sur gitlab.com
- ✅ 2 sous-domaines DNS configurables sur OVH
- ✅ Clés API (OpenAI, Gemini)

### Vous n'avez PAS besoin de :
- ❌ Connaissances Docker avancées (scripts fournis)
- ❌ Connaissances Kubernetes
- ❌ Serveur de build séparé
- ❌ Expertise DevOps

---

## 🏗️ Architecture de déploiement

```
[INTERNET]
    ⬇ HTTPS
[CADDY] (Reverse Proxy avec SSL automatique)
    ┣━ jobhunter.franckkenfack.works → Frontend Next.js
    ┗━ api.jobhunter.franckkenfack.works → Backend FastAPI
        ⬇
[Docker Network: web_net + jobhunter_internal]
    ├── Frontend (Next.js SSR)
    ├── Backend (FastAPI)
    ├── PostgreSQL (DB + pgvector)
    ├── Redis (Cache + Queue)
    └── Celery (Workers async)
```

**Sécurité** :
- SSL/TLS automatique (Let's Encrypt via Caddy)
- Conteneurs isolés (réseaux Docker séparés)
- Secrets gérés via GitLab CI/CD
- Firewall actif (ports 22, 80, 443)

---

## ⚙️ Workflow de déploiement

### Premier déploiement (Manuel + CI/CD)
```
1. Configuration VPS (15 min)
   ↓
2. Configuration DNS (5 min)
   ↓
3. Configuration GitLab (10 min)
   ↓
4. Push code → GitLab CI/CD automatique (15 min)
   ↓
5. Vérification (5 min)
```

### Mises à jour (100% automatique)
```
git push gitlab main
   ↓
GitLab CI/CD :
  - Build Frontend Docker image
  - Build Backend Docker image
  - Push vers registre GitLab
  - Déploie sur VPS
  - Redémarre services
   ↓
Application mise à jour (15 min)
```

---

## 🔑 Variables d'environnement requises

| Variable | Où la trouver | Obligatoire |
|----------|---------------|-------------|
| `SSH_IP` | IP de votre VPS | ✅ |
| `SSH_USER` | Utilisateur SSH (ubuntu) | ✅ |
| `SSH_PRIVATE_KEY` | Générer avec ssh-keygen | ✅ |
| `POSTGRES_PASSWORD` | À générer (mot de passe fort) | ✅ |
| `SECRET_KEY` | À générer (32+ chars) | ✅ |
| `OPENAI_API_KEY` | https://platform.openai.com | ✅ |
| `GEMINI_API_KEY` | https://makersuite.google.com | ✅ |
| `RAPIDAPI_KEY` | https://rapidapi.com (JSearch) | ⚠️ Optionnel |

---

## 📊 Temps et coûts

### Temps
- **Premier déploiement** : 2-3 heures
- **Mises à jour** : 10-15 minutes (automatique)
- **Monitoring** : 5 min/jour

### Coûts
- **VPS OVH** : Déjà possédé ✅
- **GitLab** : Gratuit ✅
- **Caddy** : Open source ✅
- **SSL/TLS** : Gratuit (Let's Encrypt) ✅
- **Docker** : Open source ✅

**Total** : 0€ (sauf VPS existant)

---

## 🆘 Support

### En cas de problème

1. **Vérifier les logs** :
   ```bash
   docker logs jobhunter-backend
   docker logs jobhunter-frontend
   ```

2. **Consulter les guides** :
   - Dépannage : `DEPLOY_GUIDE.md` section 9
   - Checklist : `DEPLOY_CHECKLIST.md` section dépannage

3. **Commandes utiles** :
   ```bash
   # État des conteneurs
   docker compose -f ~/jobhunter/docker-compose.prod.yml ps
   
   # Redémarrer un service
   docker compose -f ~/jobhunter/docker-compose.prod.yml restart backend
   
   # Voir les logs en temps réel
   docker compose -f ~/jobhunter/docker-compose.prod.yml logs -f
   ```

---

## 🚀 Prêt à déployer ?

### Étape par étape :
```bash
# 1. Lire le guide rapide
cat DEPLOY_QUICK_START.md

# 2. Transférer le script sur le VPS
scp deploy/vps-setup.sh ubuntu@152.228.128.95:~/

# 3. Suivre les 5 étapes du guide
# (Configuration VPS → DNS → GitLab → Push → Vérification)
```

### En cas de doute :
- Référez-vous à `DEPLOY_GUIDE.md` pour les détails
- Utilisez `DEPLOY_CHECKLIST.md` pour ne rien oublier

---

## 🎉 Après le déploiement

Votre application sera accessible sur :
- **Frontend** : https://jobhunter.franckkenfack.works
- **Backend API** : https://api.jobhunter.franckkenfack.works

**Prochaines étapes recommandées** :
1. Configurer backup automatique PostgreSQL
2. Configurer monitoring (Grafana/Prometheus)
3. Optimiser performances (cache Redis, CDN)
4. Mettre en place alerting (Sentry, Discord webhook)

---

**Bon déploiement ! 🚀**
