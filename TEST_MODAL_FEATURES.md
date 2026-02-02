# 🧪 Tests - Nouvelles fonctionnalités Sprint 10

## ✅ Tests à effectuer

### 1. Modal Contact - Landing Page
**URL:** http://localhost:3000 (déconnecté)

**Actions:**
1. Ouvrir la page d'accueil
2. Scroller jusqu'au footer (bas de page)
3. Cliquer sur "Contact" dans la section Support
4. ✅ **Attendu:** Modal s'ouvre avec formulaire + informations

**Vérifications:**
- [ ] Modal s'affiche correctement
- [ ] Formulaire contient: Nom, Email, Sujet, Message
- [ ] Informations personnelles affichées (email, téléphone, LinkedIn)
- [ ] Bouton "Envoyer le message" présent
- [ ] Modal se ferme avec X ou clic extérieur

---

### 2. Modal Contact - Footer authentifié
**URL:** http://localhost:3000/dashboard (connecté)

**Actions:**
1. Se connecter
2. Scroller jusqu'au footer
3. Cliquer sur "Contact"
4. ✅ **Attendu:** Même modal s'ouvre

---

### 3. Modal Détails Offre
**URL:** http://localhost:3000/jobs (connecté)

**Actions:**
1. Se connecter
2. Aller sur "Offres"
3. Faire une recherche (ex: "developer")
4. Cliquer sur "👁 Voir détails" sur une card
5. ✅ **Attendu:** Modal s'ouvre avec détails complets

**Vérifications dans le modal:**
- [ ] Titre du poste en grand
- [ ] Nom de l'entreprise
- [ ] Localisation, Type, Salaire, Expérience (si disponibles)
- [ ] Date de publication + Source
- [ ] Description complète (scrollable)
- [ ] Exigences (si disponibles)
- [ ] Compétences requises en badges
- [ ] Boutons actions :
  - [ ] "Postuler sur [source]" (ouvre dans nouvel onglet)
  - [ ] "Analyser compatibilité" (ferme modal, ouvre modal d'analyse)
  - [ ] "Sauvegarder" (si offre non sauvegardée)
  - [ ] Badge "Sauvegardée" en haut (si déjà sauvegardée)

---

### 4. Workflow complet: Recherche → Détails → Analyse → Sauvegarde

**Scénario utilisateur:**
1. Rechercher "python remote"
2. Cliquer "Voir détails" sur une offre intéressante
3. Lire description complète
4. Cliquer "Analyser compatibilité"
5. ✅ Modal détails se ferme
6. ✅ Modal analyse s'ouvre avec score
7. Revenir aux résultats
8. Cliquer "Sauvegarder" sur cette offre
9. Re-cliquer "Voir détails" sur la même offre
10. ✅ Badge "Sauvegardée" apparaît
11. ✅ Bouton "Sauvegarder" absent (car déjà sauvegardée)

---

### 5. OnboardingWizard → CV Upload

**Nouveau compte uniquement:**
1. Se déconnecter
2. Créer nouveau compte
3. ✅ OnboardingWizard s'affiche automatiquement
4. Cliquer "Suivant" jusqu'à étape 2 (Créez votre profil)
5. Cliquer "Uploader mon CV"
6. ✅ Redirigé vers /profile/create?mode=upload
7. ✅ Interface d'upload CV s'affiche directement (pas de choix)

**OU**

1. Cliquer "Créer manuellement"
2. ✅ Redirigé vers /profile/create?mode=form
3. ✅ Formulaire manuel s'affiche directement

---

### 6. Test envoi email (si SMTP configuré)

**Prérequis:** Variables SMTP dans .env

**Actions:**
1. Ouvrir modal contact
2. Remplir tous les champs
3. Cliquer "Envoyer le message"
4. ✅ **Attendu:** Toast "Message envoyé avec succès !"
5. ✅ Email reçu à kenfackfranck08@gmail.com

**Si erreur:**
- Toast affiche fallback: "Écrivez-moi directement à kenfackfranck08@gmail.com"

---

## 🐛 Bugs à surveiller

### Connus
- **Modal détails:** Si `description` ou `requirements` vides → sections masquées
- **JobCard:** Bouton "Voir détails" n'apparaît que si `onClick` prop fourni
- **SMTP:** Si variables manquantes → emails loggés au lieu d'être envoyés

### À tester
- [ ] Modal détails avec offre sans salaire
- [ ] Modal détails avec très longue description (scroll)
- [ ] Modal détails sur mobile (responsive)
- [ ] Double-clic sur "Sauvegarder" (race condition?)
- [ ] Cliquer "Analyser" alors que modal détails ouvert

---

## 📱 Tests responsive

### Desktop (≥1024px)
- [ ] Modal contact : 2 colonnes (infos + formulaire)
- [ ] Modal détails : Largeur max-w-4xl
- [ ] JobCards : 3 colonnes

### Tablet (768-1023px)
- [ ] Modal contact : 2 colonnes
- [ ] JobCards : 2 colonnes

### Mobile (<768px)
- [ ] Modal contact : 1 colonne (formulaire en bas)
- [ ] Modal détails : Scroll vertical
- [ ] JobCards : 1 colonne

---

## ✅ Checklist complète

### Modal Contact
- [ ] Accessible depuis footer landing page (déconnecté)
- [ ] Accessible depuis footer dashboard (connecté)
- [ ] Formulaire fonctionnel
- [ ] Liens externes fonctionnent (LinkedIn, GitHub, Portfolio)
- [ ] Responsive sur tous écrans

### Modal Détails
- [ ] S'ouvre au clic sur "Voir détails"
- [ ] Affiche toutes les infos disponibles
- [ ] Bouton "Postuler" ouvre bon lien
- [ ] Bouton "Analyser" ouvre modal analyse
- [ ] Bouton "Sauvegarder" sauvegarde et disparaît
- [ ] Badge "Sauvegardée" apparaît si déjà sauvegardée

### Intégration OnboardingWizard
- [ ] Wizard redirige avec ?mode=upload
- [ ] Page profile détecte paramètre
- [ ] Affiche directement bon mode (skip choix)

### Général
- [ ] Aucune erreur console
- [ ] Pas de warning React
- [ ] Animations fluides
- [ ] Textes en français

---

## 🚀 Commandes utiles

```bash
# Restart frontend après changements
docker compose restart frontend

# Voir logs en temps réel
docker compose logs frontend -f

# Tester API backend
curl http://localhost:8000/health

# Vérifier PostgreSQL
docker compose exec postgres psql -U jobhunter -d jobhunter_db
```

---

**Test effectué le:** __/__/____  
**Testeur:** _________________  
**Résultat:** ✅ / ⚠️ / ❌  
**Notes:** _______________________________________________
