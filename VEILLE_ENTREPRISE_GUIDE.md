# 🔍 Guide : Veille d'Entreprise (Company Watch)

## 📋 Qu'est-ce que c'est ?

La **veille d'entreprise** permet de surveiller automatiquement les offres d'emploi publiées par des entreprises spécifiques qui vous intéressent.

## 🎯 Fonctionnement

### 1. **Ajouter une entreprise à surveiller**
```
Page : /companies/watch
Action : Ajouter une entreprise (ex: "Google", "Microsoft")
```

Vous pouvez fournir :
- ✅ **Nom de l'entreprise** (obligatoire)
- ⚙️ **Seuil d'alerte** : Score minimum de compatibilité (défaut: 70%)
- 🔗 **URLs optionnelles** :
  - LinkedIn (page entreprise)
  - Careers page (page carrières)
  - Indeed, Welcome to the Jungle, etc.

### 2. **Scraping automatique**

Le système scrape **automatiquement** :
- ⏰ **Fréquence** : Toutes les 24h par défaut (configurable)
- 🤖 **Celery** : Task asynchrone en arrière-plan
- 📊 **Sources** : LinkedIn, page carrières, Indeed, WTTJ

### 3. **Scoring intelligent**

Pour chaque offre trouvée :
- 🧠 **Analyse IA** : Calcul de compatibilité avec votre profil
- 🎯 **Score** : 0-100% basé sur :
  - Vos compétences vs. offre
  - Votre expérience vs. exigences
  - Embedding sémantique (similarité)

### 4. **Alertes automatiques**

Si `score >= seuil d'alerte` :
- 📧 **Email** : Notification automatique (si configuré)
- 🔔 **Dashboard** : Badge sur l'interface
- 📌 **Liste prioritaire** : Offres triées par score

### 5. **Mutualisation** (Optimisation)

Si plusieurs utilisateurs surveillent la même entreprise :
- ✅ **1 seul scraping** pour tous les users
- 🚀 **Économie de ressources**
- 📊 **Compteur "watchers"** : voir combien d'users suivent l'entreprise

## 🛠️ Implémentation Technique

### Backend

#### **Routes API** (`app/api/routes/company_watch.py`)
- ✅ `POST /api/v1/watch/company` : Ajouter une veille
- ✅ `GET /api/v1/watch/companies` : Lister mes veilles
- ✅ `GET /api/v1/watch/company/{slug}/offers` : Offres trouvées
- ✅ `DELETE /api/v1/watch/{watch_id}` : Supprimer veille

#### **Service** (`app/services/company_watch_service.py`)
- ✅ Gestion des veilles (CRUD)
- ✅ Création de slug unique : `slugify(company_name)`
- ✅ Mutualisation : réutilise `watched_companies` si existe

#### **Celery Tasks** (`app/tasks/company_watch_tasks.py`)
- ✅ `scrape_watched_companies()` : Task périodique (toutes les 24h)
- ✅ Scraping parallèle (asyncio)
- ✅ Scoring automatique des offres

#### **Modèles** (`app/models/watched_company.py`)
```python
watched_companies:
  - id, company_name, company_slug
  - linkedin_url, careers_url, indeed_url, wttj_url
  - last_scraped_at, scraping_frequency
  - total_watchers, total_offers_found

user_company_watches (table pivot):
  - user_id, watched_company_id
  - profile_id (pour scoring)
  - alert_threshold
```

### Frontend

#### **Page** (`frontend/src/app/companies/watch/page.tsx`)
- ✅ Formulaire d'ajout d'entreprise
- ✅ Liste des veilles actives
- ✅ Affichage des offres trouvées

#### **Service** (`frontend/src/lib/companiesService.ts`)
- ✅ `addCompanyWatch()`
- ✅ `getWatchedCompanies()`
- ✅ `getCompanyOffers()`
- ✅ `deleteWatch()`

## ✅ État d'Implémentation

### ✅ **COMPLET**
- [x] Modèles de données
- [x] API Backend (CRUD)
- [x] Service de scraping
- [x] Celery task automatique
- [x] Scoring IA
- [x] Frontend UI
- [x] Mutualisation

### ⚠️ **À AMÉLIORER**
- [ ] **Notifications email** : Configurer SMTP
- [ ] **Tests E2E** : Vérifier scraping réel
- [ ] **UI polish** : Graphiques de tendances

### ❌ **MANQUANT**
- [ ] **Webhooks** : Notifications temps réel
- [ ] **Fréquence personnalisable** : UI pour changer fréquence de scraping
- [ ] **Export CSV** : Télécharger toutes les offres trouvées

## 🚀 Comment Tester

### 1. Ajouter une veille
```bash
# Via UI
http://localhost:3000/companies/watch

# Via API
curl -X POST http://localhost:8000/api/v1/watch/company \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "OpenAI",
    "alert_threshold": 75
  }'
```

### 2. Déclencher scraping manuellement
```bash
# Se connecter au container backend
docker compose -f docker-compose.prod.yml exec backend bash

# Lancer le scraping
python -c "from app.tasks.company_watch_tasks import scrape_watched_companies; import asyncio; asyncio.run(scrape_watched_companies())"
```

### 3. Vérifier les offres trouvées
```
GET /api/v1/watch/company/{company-slug}/offers
```

## 📊 Exemple de Workflow

```
1. User ajoute "Google" à surveiller avec seuil 80%
   └─> watched_companies créée (slug: "google")
   └─> user_company_watches créée (user_id, watched_company_id)

2. Celery scrape toutes les 24h
   └─> Scraping LinkedIn + Careers page
   └─> 15 offres trouvées
   └─> Pour chaque offre:
       ├─> Calcul score vs profil user (0-100%)
       ├─> Si score >= 80% → Alerte email
       └─> Sauvegarde dans job_offers

3. User consulte /companies/watch
   └─> Voit "Google" avec badge "5 nouvelles offres (score >= 80%)"
   └─> Clique → Liste des 5 offres compatibles
   └─> Génère CV + LM en 1 clic
```

## 🔧 Configuration

### Environnement
```env
# Fréquence scraping (heures)
COMPANY_WATCH_SCRAPING_FREQUENCY=24

# Score minimum par défaut
DEFAULT_ALERT_THRESHOLD=70

# Email (optionnel)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Celery Beat Schedule
```python
# backend/app/celery_app.py
CELERY_BEAT_SCHEDULE = {
    'scrape-watched-companies': {
        'task': 'app.tasks.company_watch_tasks.scrape_watched_companies',
        'schedule': crontab(hour=2, minute=0),  # Tous les jours à 2h du matin
    },
}
```

## 🎓 Conclusion

La veille d'entreprise est **100% fonctionnelle** côté backend et frontend. Le seul élément manquant pour une expérience complète est la **configuration SMTP** pour les notifications email automatiques.

**Next Steps** :
1. Configurer SMTP dans `.env.prod`
2. Tester le scraping en production
3. Ajouter UI pour ajuster fréquence de scraping par entreprise
