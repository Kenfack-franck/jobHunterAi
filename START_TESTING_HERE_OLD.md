# 🚀 COMMENCEZ ICI - Tests Job Hunter AI

## ⚡ Instructions Rapides

### 1. Se connecter
- URL: http://localhost:3000
- Email: `john.doe@testmail.com`
- Mot de passe: `Test2026!`

### 2. Suivre les 6 étapes
Ouvrez le fichier `FINAL_SUMMARY.md` et suivez les étapes 1 à 6.

### 3. Rapporter les problèmes
Pour chaque bug trouvé, utilisez le format:
```
❌ [Titre court]
Étape: [1-6]
Attendu: [...]
Observé: [...]
Erreur: [...]
```

---

## 📁 Documentation Disponible

1. **CE FICHIER** - Instructions de démarrage
2. **FINAL_SUMMARY.md** - Résumé complet avec parcours de test
3. **TEST_INSTRUCTIONS.md** - Guide simplifié
4. **TEST_GUIDE_COMPLET.md** - Guide détaillé (dans ~/.copilot/session-state/...)

---

## 🎯 Ce qu'il faut particulièrement tester

### ⭐ Priorité 1 (Fonctionnalités IA - Nouvelles)
- [ ] Le **score de compatibilité** n'est PAS toujours 78%
- [ ] Le score **change** quand on change de profil
- [ ] Il y a un **spinner** pendant le calcul (5-10s)
- [ ] Les **documents générés** sont personnalisés pour chaque offre

### ⭐ Priorité 2 (Fonctionnalités Cœur)
- [ ] Le **scraping** retourne de vraies offres d'internet
- [ ] Les **PDFs** se téléchargent correctement
- [ ] La **navigation** fonctionne (pas de 404)
- [ ] Le **contenu** des PDFs est professionnel

---

## 🔧 Si Problème

### Redémarrer tout
```bash
cd /home/kenfack/Documents/Personnal-Work/hackaton
docker compose restart
```

### Voir les logs
```bash
# Backend
docker logs jobhunter_backend --tail 50

# Frontend  
docker logs jobhunter_frontend --tail 50
```

---

## ✅ Checklist Rapide

Cochez au fur et à mesure:

- [ ] **ÉTAPE 1**: Connexion réussie → Dashboard visible
- [ ] **ÉTAPE 2**: Profil créé (ou existant visible)
- [ ] **ÉTAPE 3**: Recherche → offres affichées
- [ ] **ÉTAPE 4**: Analyse → score calculé (PAS 78% tout le temps!)
- [ ] **ÉTAPE 5**: Documents générés (CV + LM)
- [ ] **ÉTAPE 6**: PDFs téléchargés et vérifiés

---

## 📝 Notes pour le Test

**Temps estimé**: 15-20 minutes pour le parcours complet

**Ce qui doit fonctionner**:
- Login/Dashboard
- Création de profil
- Recherche avec scraping
- Calcul de score IA
- Génération de documents
- Téléchargement PDF

**Ce qui peut ne pas fonctionner** (non critique):
- Page Veille Entreprise
- Page Documents (liste)
- Page Candidatures
- Envoi email

---

🎯 **Prêt ?** Ouvrez http://localhost:3000 et commencez!

Pour les détails complets, voir **FINAL_SUMMARY.md**
