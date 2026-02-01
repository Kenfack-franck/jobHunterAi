# 🔐 IDENTIFIANTS UTILISATEUR DE TEST

## ✅ Compte Créé avec Succès !

**URL Application** : http://localhost:3000

### Identifiants de Connexion

```
📧 Email    : john.doe@testmail.com
🔑 Password : Test2026!
👤 Nom      : John Doe
```

---

## 📊 Données Pré-Remplies

Le compte de test contient **toutes les données nécessaires** pour tester l'application complète :

### 👤 Profil Utilisateur (95% complet)
- **Titre** : Senior Full Stack Developer
- **Résumé** : Développeur passionné avec 5 ans d'expérience...
- **Localisation** : Paris, France
- **Contact** : +33 6 12 34 56 78
- **Liens** :
  - LinkedIn: linkedin.com/in/johndoe
  - GitHub: github.com/johndoe  
  - Portfolio: johndoe.dev

### 💼 Expériences Professionnelles (3)

1. **Senior Full Stack Developer** @ TechCorp France
   - Période : Mars 2021 - Actuellement
   - Localisation : Paris, France
   - Technologies : Next.js, FastAPI, Docker, Kubernetes, GPT-4
   - Réalisations : Architecture microservices, Lead équipe 4 devs

2. **Full Stack Developer** @ StartupLab
   - Période : Juin 2019 - Février 2021
   - Localisation : Lyon, France
   - Technologies : React, Django, Stripe, GitHub Actions
   - Réalisations : MVP e-commerce, CI/CD

3. **Junior Developer** @ WebAgency Pro
   - Période : Septembre 2018 - Mai 2019
   - Localisation : Marseille, France
   - Technologies : WordPress, APIs REST
   - Réalisations : Sites web, Intégrations API

### 🎓 Formations (2)

1. **Master Informatique** - Intelligence Artificielle et Data Science
   - Institution : Université Paris-Saclay
   - Période : 2016 - 2018
   - Spécialisation : Machine Learning, Deep Learning, NLP

2. **Licence Informatique** - Développement Logiciel
   - Institution : Université Lyon 1
   - Période : 2013 - 2016

### 🛠️ Compétences Techniques (19)

**Backend** :
- Python (expert)
- FastAPI (expert)
- Django (advanced)
- Node.js (advanced)

**Frontend** :
- React (expert)
- Next.js (expert)
- TypeScript (expert)
- TailwindCSS (advanced)

**Database** :
- PostgreSQL (advanced)
- Redis (intermediate)

**DevOps** :
- Docker (advanced)
- Kubernetes (intermediate)
- CI/CD (advanced)
- AWS (intermediate)

**IA** :
- OpenAI API (advanced)
- Langchain (intermediate)
- Machine Learning (intermediate)

**Outils** :
- Git (expert)
- Agile/Scrum (advanced)

### 📋 Offres d'Emploi Sauvegardées (5)

1. **Senior Full Stack Developer** @ Google France
   - Type : CDI | Mode : Remote
   - Localisation : Paris, France
   - Stack : React, TypeScript, Go, Kubernetes
   - Plateforme : LinkedIn

2. **Lead Developer Python** @ Datadog
   - Type : CDI | Mode : Hybrid
   - Localisation : Paris, France
   - Stack : Python, Go, PostgreSQL, Kafka
   - Plateforme : Welcome to the Jungle

3. **Full Stack Engineer (Remote)** @ Stripe
   - Type : CDI | Mode : Remote
   - Localisation : Remote Europe
   - Stack : Ruby, React, TypeScript, PostgreSQL
   - Plateforme : Stripe Careers

4. **Senior Backend Developer** @ OVHcloud
   - Type : CDI | Mode : Hybrid
   - Localisation : Roubaix, France
   - Stack : Python, FastAPI, Kubernetes, Terraform
   - Plateforme : OVHcloud Careers

5. **AI/ML Engineer** @ Hugging Face
   - Type : CDI | Mode : Remote
   - Localisation : Paris, France
   - Stack : Python, PyTorch, FastAPI, Kubernetes
   - Plateforme : Hugging Face Jobs

---

## 🧪 SCÉNARIO DE TEST COMPLET

Pour tester toutes les fonctionnalités, suivez le document :  
**→ `TEST_SCENARIO.md`**

Le scénario couvre :
1. ✅ Authentification & Login
2. ✅ Navigation (Navbar, Sidebar, Footer)
3. ✅ Gestion Profil (voir, éditer, ajouter expériences/compétences)
4. ✅ Recherche d'Offres (liste, détails, filtres)
5. ✅ Veille Entreprise (ajouter, scraper)
6. ✅ Analyse Compatibilité (score, points forts/manquants)
7. ✅ Génération Documents (CV, Lettre de motivation)
8. ✅ Sources Personnalisées (ajouter, scraper)

---

## 🚀 QUICK START

### 1. Lancer l'application

```bash
cd /home/kenfack/Documents/Personnal-Work/hackaton
docker compose up -d
```

### 2. Accéder à l'interface

Ouvrir dans le navigateur :  
**http://localhost:3000**

### 3. Se connecter

```
Email    : john.doe@testmail.com
Password : Test2026!
```

### 4. Explorer

Vous arriverez sur le Dashboard avec :
- ✅ Navbar en haut (user menu, notifications)
- ✅ Sidebar à gauche (7 items navigation)
- ✅ Dashboard center avec cards (Profil, Recherche, Documents)
- ✅ Footer en bas

**Badge "Profil 95%"** visible dans Navbar → profil quasi complet

---

## 📸 Captures d'Écran Attendues

En vous connectant, vous devriez voir :

### Dashboard
- Card "Mon Profil" avec :
  - Titre : Senior Full Stack Developer
  - Barre complétion : 95%
  - Statistiques : 3 exp. | 2 form. | 19 comp.

### Page Profil (`/profile`)
- Informations générales complètes
- 3 expériences listées avec dates
- 2 formations listées
- 19 compétences avec badges colorés (expert/advanced/intermediate)

### Page Recherche (`/jobs/search`)
- 5 offres affichées en cards
- Filtres disponibles (type, mode, localisation)
- Bouton "Voir détails" sur chaque offre

### Détail Offre (`/jobs/[id]`)
- Titre : Senior Full Stack Developer @ Google France
- Description complète
- Stack technique
- Boutons : "Analyser", "Générer documents", "Supprimer"

---

## ⚙️ Commandes Utiles

### Vérifier que l'utilisateur existe

```bash
docker compose exec backend python -c "
from sqlalchemy import create_engine, text
engine = create_engine('postgresql://jobhunter:jobhunter_secure_password_2024@postgres:5432/jobhunter_db')
with engine.connect() as conn:
    result = conn.execute(text('SELECT email, full_name FROM users WHERE email = :email'), {'email': 'john.doe@testmail.com'})
    for row in result:
        print(f'✅ User: {row[0]} - {row[1]}')
"
```

### Réinitialiser le mot de passe

Si nécessaire, exécuter :
```bash
docker compose exec backend python /tmp/delete_test_user.py
docker compose exec backend python create_test_user.py
```

---

## 🎯 Fonctionnalités à Tester

### ✅ Implémentées et Testables

- [x] Inscription / Login / Logout
- [x] Navigation (Navbar + Sidebar + Footer)
- [x] Gestion profil complet
- [x] Recherche offres avec filtres
- [x] Ajout offre manuelle
- [x] Détail offre
- [x] Suppression offre

### ⏳ Implémentées mais Non Testées (à vérifier manuellement)

- [ ] Veille entreprise (ajouter, scraper)
- [ ] Custom sources (ajouter, scraper)
- [ ] Analyse compatibilité avec score
- [ ] Génération CV/Lettre avec IA
- [ ] Feed personnalisé

### ❌ Non Implémentées (Sprints futurs)

- Search bar Navbar
- Notifications réelles
- Page Help
- Page Settings
- Page Applications (journal)
- Page Documents (liste générés)

---

## 🐛 Issues Connues

1. **Scraping Indeed bloqué** - Anti-bot (utiliser RemoteOK à la place)
2. **Page analyze ne compile pas** - Import manquant (test en dev mode uniquement)
3. **Search bar non fonctionnelle** - Sprint 10
4. **Help/Settings pages manquantes** - Sprint 8

---

## 📞 Support

Si problèmes :
1. Vérifier que Docker est lancé : `docker compose ps`
2. Vérifier logs frontend : `docker compose logs frontend --tail 50`
3. Vérifier logs backend : `docker compose logs backend --tail 50`
4. Relancer services : `docker compose restart`

---

**Document créé le** : 2026-01-30  
**Version** : Sprint 7 Complete + Test User Ready  
**Auteur** : GitHub Copilot + Kenfack

**🎉 Profitez du test !**
