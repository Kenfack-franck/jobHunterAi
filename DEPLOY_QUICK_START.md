# 🚀 Déploiement Job Hunter AI - Guide Rapide

## 📌 Résumé

**Architecture** : 5 conteneurs Docker (Frontend + Backend + PostgreSQL + Redis + Celery)  
**Domaines** : 2 sous-domaines requis  
**CI/CD** : GitLab automatique  
**Temps** : 2-3h (première fois)

---

## 🎯 Ordre d'exécution

### 1️⃣ SUR LE VPS (15 min) - UNE SEULE FOIS

```bash
# Se connecter au VPS
ssh ubuntu@152.228.128.95

# Télécharger et exécuter le script d'installation
wget https://raw.githubusercontent.com/VOTRE_USER/job-hunter-ai/main/deploy/vps-setup.sh
chmod +x vps-setup.sh
./vps-setup.sh

# Redémarrer
sudo reboot
```

**Installer Caddy** (après redémarrage) :
```bash
# Créer ~/proxy/docker-compose.yml (voir DEPLOY_GUIDE.md section 2.1)
# Créer ~/proxy/Caddyfile (voir DEPLOY_GUIDE.md section 2.2)
cd ~/proxy
docker compose up -d
```

**Transférer docker-compose** :
```bash
# Sur votre PC
scp docker-compose.prod.yml ubuntu@152.228.128.95:~/jobhunter/
```

---

### 2️⃣ DNS OVH (5 min)

Ajouter 2 enregistrements A :
- `jobhunter` → `152.228.128.95`
- `api.jobhunter` → `152.228.128.95`

Attendre 5-10 min pour propagation.

---

### 3️⃣ GITLAB (10 min)

**Créer projet** : `https://gitlab.com`

**Ajouter 8 variables** (Settings > CI/CD > Variables) :
```
SSH_IP              = 152.228.128.95
SSH_USER            = ubuntu
SSH_PRIVATE_KEY     = (votre clé Base64, voir guide)
POSTGRES_PASSWORD   = (générer mot de passe fort)
SECRET_KEY          = (python3 -c "import secrets; print(secrets.token_hex(32))")
OPENAI_API_KEY      = sk-proj-...
GEMINI_API_KEY      = AIzaSy...
RAPIDAPI_KEY        = (optionnel)
```

**Générer clé SSH** :
```bash
ssh-keygen -t ed25519 -f ~/.ssh/gitlab_jobhunter_key
ssh-copy-id -i ~/.ssh/gitlab_jobhunter_key.pub ubuntu@152.228.128.95
base64 -w 0 ~/.ssh/gitlab_jobhunter_key  # Copier dans SSH_PRIVATE_KEY
```

---

### 4️⃣ PUSH CODE (5 min)

```bash
# Ajouter remote GitLab
git remote add gitlab https://gitlab.com/VOTRE_USER/job-hunter-ai.git

# Push
git add .
git commit -m "feat: Production deployment"
git push gitlab main
```

**Surveiller pipeline** : GitLab > CI/CD > Pipelines  
Durée : 10-15 minutes

---

### 5️⃣ VÉRIFICATION (5 min)

```bash
# Sur VPS
ssh ubuntu@152.228.128.95
cd ~/jobhunter
docker compose -f docker-compose.prod.yml ps

# Devrait afficher 5 conteneurs UP
```

**Tester l'accès** :
- Frontend : https://jobhunter.franckkenfack.works
- API : https://api.jobhunter.franckkenfack.works/health

**Initialiser DB** :
```bash
docker exec jobhunter-backend alembic upgrade head
```

---

## ✅ C'EST FAIT !

Votre application est en ligne 🎉

---

## 📚 Documentation complète

- **Guide détaillé** : `DEPLOY_GUIDE.md`
- **Checklist complète** : `DEPLOY_CHECKLIST.md`
- **Dépannage** : Voir section "Dépannage" dans `DEPLOY_GUIDE.md`

---

## 🔄 Mises à jour futures

```bash
# Sur votre PC
git add .
git commit -m "update: nouvelle fonctionnalité"
git push gitlab main
```

GitLab CI/CD fait tout automatiquement (10-15 min).

---

## 🆘 Problème ?

1. Vérifier logs : `docker logs jobhunter-backend`
2. Vérifier variables GitLab (8 variables)
3. Vérifier DNS : `nslookup jobhunter.franckkenfack.works`
4. Consulter `DEPLOY_GUIDE.md` section Dépannage
