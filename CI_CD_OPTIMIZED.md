# CI/CD Pipeline Optimisé - Job Hunter AI

## 🚀 Comment ça fonctionne

Le pipeline GitLab CI est maintenant **intelligent** : il ne rebuil que ce qui a changé !

### 📊 Scénarios de déploiement

#### 1️⃣ Changement Frontend uniquement
**Fichiers modifiés** : `frontend/**/*`  
**Pipeline** :
```
✅ build_frontend  → Rebuild Next.js (~30s)
✅ deploy_frontend → Redémarre frontend uniquement
❌ build_backend   → SKIP
❌ deploy_backend  → SKIP
```
**Temps** : ~1-2 min (au lieu de 15+ min)

---

#### 2️⃣ Changement Backend uniquement
**Fichiers modifiés** : `backend/**/*`  
**Pipeline** :
```
❌ build_frontend  → SKIP
❌ deploy_frontend → SKIP
✅ build_backend   → Rebuild FastAPI + PyTorch (~10 min)
✅ deploy_backend  → Redémarre backend + celery
```
**Temps** : ~10-12 min (normal pour PyTorch)

---

#### 3️⃣ Changement Infrastructure
**Fichiers modifiés** : `docker-compose.prod.yml` ou `.gitlab-ci.yml`  
**Pipeline** :
```
❌ build_frontend  → SKIP
❌ deploy_frontend → SKIP
❌ build_backend   → SKIP
❌ deploy_backend  → SKIP
✅ deploy_full     → Met à jour docker-compose + redémarre tout
```
**Temps** : ~2-3 min (pull des images existantes)

---

#### 4️⃣ Changement Frontend + Backend
**Pipeline** :
```
✅ build_frontend  → Rebuild Next.js
✅ build_backend   → Rebuild FastAPI
✅ deploy_frontend → Déploie frontend
✅ deploy_backend  → Déploie backend + celery
```
**Temps** : ~12-15 min (les 2 builds en parallèle)

---

## 📁 Détection des changements

GitLab CI détecte automatiquement avec `only: changes:` :

| Chemin modifié | Jobs déclenchés |
|----------------|-----------------|
| `frontend/src/**` | `build_frontend` + `deploy_frontend` |
| `backend/app/**` | `build_backend` + `deploy_backend` |
| `docker-compose.prod.yml` | `deploy_full` |
| `.gitlab-ci.yml` | Tout se rebuil (sécurité) |

---

## 🎯 Avantages

### Avant (pipeline monolithique)
```
Changement 1 ligne CSS → Rebuild 4.4GB PyTorch → 15+ min 😭
```

### Après (pipeline intelligent)
```
Changement 1 ligne CSS → Rebuild Next.js → 1 min 🎉
```

**Économies** :
- ⚡ **93% plus rapide** pour frontend seul
- 💰 **Moins de ressources** consommées sur le runner
- 🔋 **Moins d'espace disque** utilisé
- 🚀 **Déploiements plus fréquents** possibles

---

## 🧪 Test du nouveau pipeline

### Test 1 : Frontend uniquement
```bash
# Modifier un fichier frontend
echo "// Test" >> frontend/src/app/page.tsx
git add frontend/
git commit -m "test: frontend only"
git push

# Résultat attendu : Seulement build_frontend + deploy_frontend
```

### Test 2 : Backend uniquement
```bash
# Modifier un fichier backend
echo "# Test" >> backend/app/main.py
git add backend/
git commit -m "test: backend only"
git push

# Résultat attendu : Seulement build_backend + deploy_backend
```

### Test 3 : Infrastructure
```bash
# Modifier docker-compose
echo "# Comment" >> docker-compose.prod.yml
git add docker-compose.prod.yml
git commit -m "chore: update compose"
git push

# Résultat attendu : Seulement deploy_full (pas de rebuild)
```

---

## 🔍 Vérifier dans GitLab

**GitLab → CI/CD → Pipelines**

Vous verrez maintenant :
```
Pipeline #123
├─ build_frontend  ✅ (1m 30s)
└─ deploy_frontend ✅ (45s)

Total: 2m 15s  (au lieu de 15min+)
```

---

## ⚠️ Notes importantes

### Quand TOUT se rebuil
Le pipeline complet s'exécute si :
- ✅ Modifications dans `frontend/` **ET** `backend/`
- ✅ Modifications dans `.gitlab-ci.yml`
- ✅ Premier commit après ajout du nouveau pipeline

### Dépendances
- `deploy_frontend` nécessite `build_frontend` (avec `needs:`)
- `deploy_backend` nécessite `build_backend` (avec `needs:`)
- Si un build échoue, le deploy correspondant ne s'exécute pas

### Images Docker
Les images sont taguées `:latest`. Pour des tags versionnés :
```yaml
# Dans .gitlab-ci.yml, remplacer :latest par :
$CI_COMMIT_SHORT_SHA  # Tag avec hash du commit
```

---

## 🛠️ Dépannage

### "No jobs to run"
**Cause** : Aucun fichier surveillé n'a changé  
**Solution** : Normal ! GitLab skip le pipeline si rien à faire

### Build skipped mais deploy run
**Cause** : Image déjà présente dans le registry  
**Solution** : Forcer rebuild avec :
```bash
git commit --allow-empty -m "chore: force rebuild"
```

### "Service is already running"
**Cause** : Le service n'a pas besoin de redémarrer  
**Solution** : Normal, Docker Compose est idempotent

---

## 📈 Monitoring

Commandes utiles sur le VPS :

```bash
# Voir les images déployées
docker images | grep jobhunter

# Voir les services actifs
docker compose -f docker-compose.prod.yml ps

# Logs en temps réel
docker compose -f docker-compose.prod.yml logs -f

# Espace disque des images
docker system df
```

---

## 🎓 Pour aller plus loin

### Cache Docker layers
Ajouter dans les jobs build :
```yaml
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .docker-cache/
```

### Multi-environment
Créer `develop` et `staging` avec :
```yaml
deploy_staging:
  only:
    - develop
  environment:
    name: staging
```

### Rollback automatique
Ajouter healthchecks et rollback si échec :
```yaml
after_script:
  - if [ $CI_JOB_STATUS == "failed" ]; then
      ssh $SSH_USER@$SSH_IP "cd ~/jobhunter && docker compose -f docker-compose.prod.yml rollback";
    fi
```

---

## ✅ Checklist post-migration

- [x] `.gitlab-ci.yml` mis à jour
- [ ] Tester un push frontend seul
- [ ] Tester un push backend seul
- [ ] Vérifier les logs GitLab CI
- [ ] Mesurer le gain de temps

**Économie attendue** : ~85% de temps de CI pour 90% des commits 🚀
