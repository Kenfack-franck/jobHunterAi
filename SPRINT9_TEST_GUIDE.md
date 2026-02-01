# 🧪 GUIDE DE TEST - SPRINT 9

## Objectif
Valider que les pages sont bien connectées au backend et affichent les vraies données.

---

## 🔐 CONNEXION

### 1. Ouvrir l'application
```
URL: http://localhost:3000
```

### 2. Se connecter avec le compte test
```
Email: john.doe@testmail.com
Password: Test2026!
```

**Attendu** : Redirection vers `/dashboard`

---

## 🏢 TEST: VEILLE ENTREPRISE

### Navigation
```
Dashboard → Sidebar → Veille Entreprise
OU
URL directe: http://localhost:3000/companies/watch
```

### Scénarios à tester

#### ✅ 1. Affichage des entreprises existantes
- **Attendu**: Voir 6 entreprises (données du test user)
- **Vérifier**: 
  - Nom des entreprises affichés
  - URLs carrières visibles
  - Compteur d'offres
  - Date dernière MAJ

#### ✅ 2. Ajout d'une nouvelle entreprise
1. Cliquer sur "Ajouter"
2. Remplir:
   - Nom: "Amazon"
   - URL: "https://amazon.jobs"
3. Cliquer "Ajouter"
- **Attendu**: 
  - Toast success "Amazon ajoutée à la veille !"
  - Liste rafraîchie avec Amazon
  - Total entreprises = 7

#### ✅ 3. Scraping manuel
1. Cliquer sur icône refresh d'une entreprise
- **Attendu**:
  - Toast "Scraping en cours..."
  - Puis "Scraping terminé !"
  - Compteur offres potentiellement mis à jour

#### ✅ 4. Suppression d'entreprise
1. Cliquer sur icône poubelle
2. Confirmer suppression
- **Attendu**:
  - Modal de confirmation
  - Toast "Entreprise supprimée"
  - Liste rafraîchie

#### ✅ 5. État vide
1. Supprimer toutes les entreprises
- **Attendu**:
  - EmptyState affiché
  - "Aucune entreprise surveillée"
  - Bouton "Ajouter une entreprise"

---

## 📄 TEST: DOCUMENTS

### Navigation
```
Dashboard → Sidebar → Documents
OU
URL directe: http://localhost:3000/documents
```

### Scénarios à tester

#### ✅ 1. État initial (aucun document)
- **Attendu**:
  - EmptyState affiché
  - "Aucun document"
  - Message: "Analysez une offre..."
  - Bouton "Voir les offres"

#### ✅ 2. Filtres
1. Cliquer sur "CV", "Lettres", "Tous"
- **Attendu**:
  - Bouton actif change de style (variant="default")
  - Liste filtrée (vide pour l'instant)

#### ✅ 3. Génération d'un document (test complet)
**Préalable**: Générer un document depuis une offre

1. Aller dans Jobs → Offres
2. Cliquer sur une offre
3. Générer CV/LM
4. Retourner sur /documents

- **Attendu**:
  - Document(s) listé(s)
  - Type affiché (CV badge bleu, LM badge vert)
  - Entreprise + poste affichés
  - Date de génération
  - Actions: Download, Preview, Regenerate, Delete

#### ✅ 4. Téléchargement
1. Cliquer sur icône Download
- **Attendu**:
  - Téléchargement PDF démarré
  - Toast "document_X.pdf téléchargé"

#### ✅ 5. Suppression
1. Cliquer sur icône poubelle
2. Confirmer
- **Attendu**:
  - Modal confirmation
  - Toast "Document supprimé"
  - Liste rafraîchie

---

## 👁️ TEST: CANDIDATURES

### Navigation
```
Dashboard → Sidebar → Candidatures
OU
URL directe: http://localhost:3000/applications
```

### Scénarios

#### ⚠️ MOCK DATA
- **Note**: Cette page utilise encore des données mock
- L'API /applications n'existe pas dans le backend
- Test uniquement l'UI pour l'instant

#### ✅ 1. Affichage mock
- **Attendu**:
  - 4 candidatures affichées
  - Statuts variés (En attente, Réponse, Entretien, Refusé)
  - Stats (Total, Taux réponse)
  - Badges colorés selon statut

---

## ⚙️ TEST: PARAMÈTRES

### Navigation
```
Dashboard → Sidebar → Paramètres
OU
URL directe: http://localhost:3000/settings
```

### Scénarios

#### ✅ 1. Onglet Compte
- **Attendu**:
  - Email affiché: john.doe@testmail.com
  - Nom complet: John Doe
  - Date membre: Janvier 2026

#### ✅ 2. Modification mot de passe
1. Remplir:
   - Mot de passe actuel
   - Nouveau mot de passe
   - Confirmation
2. Cliquer "Enregistrer"
- **Attendu**:
  - Toast "Compte mis à jour"
  - (Feature backend à implémenter)

#### ✅ 3. Onglet Notifications
- **Attendu**:
  - 4 checkboxes
  - Toggle fonctionne
  - Bouton "Enregistrer les préférences"

#### ✅ 4. Onglet Confidentialité
- **Attendu**:
  - Bouton "Exporter mes données"
  - Zone danger rouge
  - Bouton "Supprimer mon compte"

---

## ❓ TEST: AIDE

### Navigation
```
Dashboard → Sidebar → Aide
OU
URL directe: http://localhost:3000/help
```

### Scénarios

#### ✅ 1. Recherche FAQ
1. Taper "profil" dans la barre de recherche
- **Attendu**:
  - Liste filtrée à 2-3 questions
  - Highlight des résultats

#### ✅ 2. Expand/Collapse FAQ
1. Cliquer sur une question
- **Attendu**:
  - Réponse s'affiche
  - Icône chevron change (down → up)

#### ✅ 3. Catégories
- **Attendu**:
  - 6 catégories affichées
  - Démarrage, Recherche, Documents IA, Candidatures, Compte

---

## 🎯 CHECKLIST GLOBALE

### Loading States ✅
- [ ] Companies Watch affiche spinner au chargement
- [ ] Documents affiche spinner au chargement
- [ ] Spinner disparaît après load

### Empty States ✅
- [ ] Companies Watch: EmptyState si 0 entreprises
- [ ] Documents: EmptyState si 0 documents
- [ ] Applications: EmptyState si 0 candidatures (mock)

### Error Handling ✅
- [ ] Toast error si API échoue
- [ ] Toast success sur action réussie
- [ ] Confirmation avant suppression

### Navigation ✅
- [ ] Tous les liens Sidebar fonctionnent
- [ ] Page active highlightée dans Sidebar
- [ ] Navbar persiste sur toutes les pages
- [ ] Footer présent sur toutes les pages

### Performance ✅
- [ ] Pages chargent < 2s
- [ ] Pas de freeze UI pendant fetch
- [ ] Smooth transitions

---

## 🐛 BUGS À REPORTER

Si vous trouvez des problèmes, notez:
1. Page concernée
2. Action effectuée
3. Résultat attendu vs obtenu
4. Message erreur (console + toast)

---

## ✅ RÉSULTAT ATTENDU

À la fin de ces tests:
- ✅ 2 pages pleinement intégrées (Companies, Documents)
- ✅ 2 pages fonctionnelles UI (Applications, Settings)
- ✅ 1 page statique (Help)
- ✅ 0 erreurs console critiques
- ✅ Toutes les actions donnent du feedback (toast)
- ✅ Backend répond correctement

**Status** : SPRINT 9 - 50% COMPLET
**Prochaine étape** : Finaliser Settings + tests backend complets
