# 📋 CHECKLIST DE DÉPLOIEMENT JOB HUNTER AI

## ✅ PRÉ-REQUIS (À faire une seule fois)

### 1. VPS (Serveur)
- [ ] VPS accessible : `ssh ubuntu@152.228.128.95`
- [ ] Script d'installation transféré : `scp deploy/vps-setup.sh ubuntu@152.228.128.95:~/`
- [ ] Script exécuté : `./vps-setup.sh`
- [ ] Serveur redémarré : `sudo reboot`
- [ ] Docker fonctionnel : `docker --version`
- [ ] Réseau `web_net` créé : `docker network ls | grep web_net`

### 2. DNS (Domaines)
- [ ] Enregistrement A `jobhunter.franckkenfack.works` → `152.228.128.95`
- [ ] Enregistrement A `api.jobhunter.franckkenfack.works` → `152.228.128.95`
- [ ] DNS propagé : `nslookup jobhunter.franckkenfack.works`

### 3. Caddy (Reverse Proxy)
- [ ] Fichier `~/proxy/docker-compose.yml` créé
- [ ] Fichier `~/proxy/Caddyfile` créé avec les 2 domaines
- [ ] Caddy démarré : `cd ~/proxy && docker compose up -d`
- [ ] Caddy fonctionne : `docker ps | grep caddy`

### 4. Clé SSH GitLab CI
- [ ] Clé SSH générée : `ssh-keygen -t ed25519 -f ~/.ssh/gitlab_jobhunter_key`
- [ ] Clé publique copiée sur VPS : `ssh-copy-id -i ~/.ssh/gitlab_jobhunter_key.pub ubuntu@152.228.128.95`
- [ ] Clé privée encodée Base64 : `base64 -w 0 ~/.ssh/gitlab_jobhunter_key`

---

## ✅ CONFIGURATION PROJET (Local)

### 5. Fichiers Docker
- [ ] `frontend/Dockerfile.prod` créé ✅
- [ ] `backend/Dockerfile.prod` créé ✅
- [ ] `docker-compose.prod.yml` créé ✅
- [ ] `.dockerignore` créé ✅
- [ ] `.gitlab-ci.yml` créé ✅

### 6. Configuration Next.js
- [ ] `frontend/next.config.js` a `output: 'standalone'` ✅ (déjà fait)

### 7. Fichiers à transférer sur VPS
```bash
scp docker-compose.prod.yml ubuntu@152.228.128.95:~/jobhunter/
```
- [ ] `docker-compose.prod.yml` copié sur VPS

---

## ✅ GITLAB CI/CD (Variables)

### 8. Créer projet GitLab
- [ ] Projet créé sur GitLab : `https://gitlab.com/VOTRE_USER/job-hunter-ai`
- [ ] Remote ajouté localement : `git remote add gitlab https://gitlab.com/VOTRE_USER/job-hunter-ai.git`

### 9. Variables GitLab (Settings > CI/CD > Variables)

| Nom | Valeur | Masqué | Exemple |
|-----|--------|--------|---------|
| `SSH_IP` | `152.228.128.95` | Non | - |
| `SSH_USER` | `ubuntu` | Non | - |
| `SSH_PRIVATE_KEY` | Votre clé Base64 | **Non** | `LS0tLS1CRUdJTi...` |
| `POSTGRES_PASSWORD` | Mot de passe DB | Oui | `SuperSecurePass123!` |
| `SECRET_KEY` | Clé JWT (32+ chars) | Oui | `578a757e36cb45468116c5588889853627af926e3c822baccd79dcfb7c1faf80` |
| `OPENAI_API_KEY` | Clé OpenAI | Oui | `sk-proj-...` |
| `GEMINI_API_KEY` | Clé Gemini | Oui | `AIzaSy...` |
| `RAPIDAPI_KEY` | Clé JSearch (optionnel) | Oui | `abc123...` |

- [ ] 8 variables ajoutées dans GitLab

**Générer SECRET_KEY** :
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## ✅ DÉPLOIEMENT

### 10. Premier déploiement
```bash
git add .
git commit -m "feat: Production deployment configuration"
git push gitlab main
```
- [ ] Code poussé sur GitLab
- [ ] Pipeline GitLab démarré
- [ ] Stage `build_frontend` ✅ (5-10 min)
- [ ] Stage `build_backend` ✅ (3-5 min)
- [ ] Stage `deploy_production` ✅ (2-3 min)

### 11. Vérifications VPS
```bash
ssh ubuntu@152.228.128.95
cd ~/jobhunter
docker compose -f docker-compose.prod.yml ps
```
- [ ] 5 conteneurs running :
  - [ ] `jobhunter-frontend`
  - [ ] `jobhunter-backend`
  - [ ] `jobhunter-postgres`
  - [ ] `jobhunter-redis`
  - [ ] `jobhunter-celery`

### 12. Tests d'accès
```bash
# Frontend
curl -I https://jobhunter.franckkenfack.works

# Backend API
curl https://api.jobhunter.franckkenfack.works/health
```
- [ ] Frontend répond : `HTTP/2 200`
- [ ] Backend API répond : `{"status":"healthy"}`

### 13. Initialisation Base de Données
```bash
ssh ubuntu@152.228.128.95
docker exec jobhunter-backend alembic upgrade head
```
- [ ] Migrations appliquées
- [ ] Tables créées

---

## ✅ TESTS FONCTIONNELS

### 14. Tests Frontend
- [ ] Ouvrir : `https://jobhunter.franckkenfack.works`
- [ ] Page d'accueil s'affiche
- [ ] Formulaire inscription fonctionne
- [ ] Connexion fonctionne

### 15. Tests Backend
- [ ] API Health : `https://api.jobhunter.franckkenfack.works/health`
- [ ] Créer compte test
- [ ] Créer profil
- [ ] Lancer recherche d'offres

---

## ✅ MONITORING

### 16. Logs
```bash
# Tous les services
docker compose -f ~/jobhunter/docker-compose.prod.yml logs -f

# Un service spécifique
docker logs -f jobhunter-backend
```
- [ ] Aucune erreur critique dans les logs

### 17. Ressources
```bash
# Utilisation CPU/RAM
docker stats

# Espace disque
df -h
```
- [ ] CPU < 80%
- [ ] RAM disponible > 1GB
- [ ] Disk disponible > 5GB

---

## 🎉 DÉPLOIEMENT COMPLET !

Si tous les éléments sont cochés ✅, votre application est en ligne !

**URLs** :
- Frontend : https://jobhunter.franckkenfack.works
- Backend API : https://api.jobhunter.franckkenfack.works

**Prochaines étapes** :
1. Configurer backup automatique PostgreSQL
2. Configurer monitoring (Grafana/Prometheus)
3. Optimiser performances (cache, CDN)

---

## 🆘 DÉPANNAGE RAPIDE

### Pipeline GitLab échoue
```bash
# Vérifier les logs dans GitLab
# Cause fréquente : SSH_PRIVATE_KEY mal formaté
```

### Conteneur ne démarre pas
```bash
docker logs jobhunter-NOMSERVICE
# Vérifier les variables d'environnement dans .env
```

### 502 Bad Gateway
```bash
# Vérifier que le conteneur tourne
docker ps | grep jobhunter-frontend
# Vérifier le nom dans Caddyfile
cat ~/proxy/Caddyfile
```

### Base de données vide
```bash
# Relancer les migrations
docker exec jobhunter-backend alembic upgrade head
```

---

**Temps total estimé** : 2-3 heures (première fois)  
**Mises à jour ultérieures** : 10-15 minutes (automatique via GitLab CI)
