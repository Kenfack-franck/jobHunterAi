# 🧪 Tests Admin Panel - Interface Web

## 📋 Pré-requis
1. Backend lancé: `docker compose up -d`
2. Frontend lancé: http://localhost:3000
3. Connecté comme admin: `kenfackfranck08@gmail.com` / `noumedem`

---

## ✅ Test 1: Navigation
1. Va sur http://localhost:3000/dashboard
2. Dans la sidebar, cherche "🛡️ Admin Panel" (violet/rose)
3. Clique dessus
4. **Résultat attendu**: Tu arrives sur `/admin` avec les stats

---

## ✅ Test 2: Dashboard Stats
Sur `/admin`:
- ✅ Total users affiché (21 attendu)
- ✅ Active users (21 attendu)
- ✅ Blocked users (0 attendu)
- ✅ Graphique registrations par jour

---

## ✅ Test 3: Liste Utilisateurs
1. Clique sur "Gestion des utilisateurs"
2. **Résultat attendu**: Liste de 20 users/page

### Vérifications:
- ✅ Emails affichés
- ✅ Rôles (admin / user) visibles
- ✅ Status (Actif / Bloqué) avec badges
- ✅ Date d'inscription
- ✅ Boutons d'actions (🔴 Bloquer, 🗑️ Supprimer)

---

## ✅ Test 4: Filtres
Sur `/admin/users`:

### Filtre par rôle:
1. Sélectionne "Administrateurs" dans le dropdown
2. **Attendu**: 1 seul user (kenfackfranck08@gmail.com)
3. Sélectionne "Utilisateurs"
4. **Attendu**: 20 users (sans l'admin)

### Filtre par status:
1. Sélectionne "Actifs"
2. **Attendu**: 21 users
3. Sélectionne "Bloqués"
4. **Attendu**: 0 users (ou ceux bloqués)

### Recherche:
1. Tape "kenfack" dans la barre de recherche
2. **Attendu**: 1 résultat (ton compte admin)

---

## ✅ Test 5: Bloquer/Débloquer User

### Bloquer:
1. Sur un user normal (pas admin), clique sur 🔴 (icône UserX orange)
2. Confirme dans l'alert
3. **Attendu**: 
   - Badge change de "Actif" (vert) → "Bloqué" (rouge)
   - Icône change de 🔴 → ✅ (UserCheck vert)

### Débloquer:
1. Clique à nouveau sur ✅ (icône UserCheck)
2. Confirme
3. **Attendu**: Badge redevient "Actif" (vert)

---

## ✅ Test 6: Supprimer User

### Créer user test:
1. Ouvre une fenêtre incognito
2. Va sur http://localhost:3000/auth/register
3. Crée un compte: `test-delete@test.com` / `password123`
4. Ferme l'incognito

### Supprimer:
1. Retourne sur `/admin/users` (connecté admin)
2. Cherche "test-delete" dans la recherche
3. Clique sur 🗑️ (Trash2 rouge)
4. Confirme l'alert (avec avertissement)
5. **Attendu**: 
   - User disparaît de la liste
   - Total users diminue de 1

---

## ✅ Test 7: Protection Auto-Suppression
1. Cherche ton propre email (kenfackfranck08@gmail.com)
2. Essaie de cliquer sur 🗑️
3. **Attendu**: 
   - Alert "Vous ne pouvez pas supprimer votre propre compte"
   - Aucune suppression

---

## 🚨 Si ça ne marche pas:

### Actions ne répondent pas:
```bash
# Dans la console du navigateur (F12)
const token = localStorage.getItem('auth_token');
console.log('Token:', token ? 'Présent' : 'MANQUANT');

# Vérifie que le token contient role='admin'
const payload = JSON.parse(atob(token.split('.')[1]));
console.log('Role:', payload.role); // Doit être 'admin'
```

### Filtres ne marchent pas:
```bash
# Test manuel dans la console
const token = localStorage.getItem('auth_token');
fetch('http://localhost:8000/api/v1/admin/users?role=admin', {
  headers: { 'Authorization': 'Bearer ' + token }
})
.then(r => r.json())
.then(d => console.log('Admins:', d.total));
```

### Erreur CORS:
```bash
# Vérifie les logs backend
docker compose logs backend | grep CORS
```

---

## ✅ Checklist Finale

- [ ] Dashboard accessible via sidebar
- [ ] Stats affichées correctement
- [ ] Liste users avec pagination
- [ ] Filtre "Administrateurs" → 1 résultat
- [ ] Filtre "Utilisateurs" → 20 résultats
- [ ] Recherche fonctionne
- [ ] Bloquer user fonctionne
- [ ] Débloquer user fonctionne
- [ ] Supprimer user fonctionne
- [ ] Protection auto-suppression active

---

**Note**: Tous ces tests ont réussi en ligne de commande (curl). Si ça ne marche pas dans le browser, c'est probablement un problème de token JWT ou CORS.
