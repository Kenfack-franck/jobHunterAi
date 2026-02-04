# 🧪 Test Message Blocage Utilisateur

## ✅ Backend Testé - Fonctionne parfaitement

```bash
# Test automatique réussi
✅ HTTP 403 Forbidden quand user bloqué
✅ Message: "Votre compte a été bloqué par un administrateur. Veuillez contacter kenfackfranck08@gmail.com..."
✅ Déblocage fonctionne (200 OK après toggle)
```

---

## 🧪 Test Manuel Frontend

### Option 1: Depuis l'interface web

1. **Connecte-toi comme admin**
   - Va sur http://localhost:3000/auth/login
   - Login: `kenfackfranck08@gmail.com` / `noumedem`

2. **Bloque un utilisateur**
   - Va sur `/admin/users`
   - Cherche "blocked-test@example.com" (ou crée ce compte)
   - Clique sur l'icône 🔴 (UserX orange)
   - Confirme le blocage

3. **Déconnecte-toi**
   - Clique sur ton profil → Déconnexion

4. **Essaie de te connecter avec le user bloqué**
   - Va sur `/auth/login`
   - Entre: `blocked-test@example.com` / `testpass123`
   - Clique sur "Se connecter"

5. **Résultat attendu**
   ```
   ❌ Votre compte a été bloqué par un administrateur. 
      Veuillez contacter kenfackfranck08@gmail.com pour plus d'informations.
   ```
   - Message en rouge
   - Toast d'erreur affiché
   - Connexion refusée

---

### Option 2: Test avec page HTML standalone

Ouvre dans ton navigateur:
```bash
file:///tmp/test_blocked_frontend.html
```

Puis clique sur les boutons dans l'ordre 1-2-3-4

---

### Option 3: Test depuis la console navigateur

```javascript
// Sur http://localhost:3000 (F12 → Console)

// Test login user bloqué
fetch('http://localhost:8000/api/v1/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'blocked-test@example.com',
    password: 'testpass123'
  })
})
.then(r => r.json())
.then(data => {
  console.log('Status:', data.detail);
  // Doit afficher: "Votre compte a été bloqué..."
});
```

---

## 🔍 Vérification erreur affichée

Sur la page login, quand user bloqué tente de se connecter:

**❌ Zone d'erreur rouge doit apparaître:**
```
 🔴 Votre compte a été bloqué par un administrateur.
    Veuillez contacter kenfackfranck08@gmail.com pour plus d'informations.
```

**Toast (notification coin haut droit):**
```
❌ Votre compte a été bloqué par un administrateur...
```

---

## ✅ Checklist Test

- [ ] Message backend fonctionne (HTTP 403) ✅ Testé en CLI
- [ ] Message affiché dans zone d'erreur rouge (login page)
- [ ] Toast d'erreur affiché
- [ ] Message mentionne "bloqué par un administrateur"
- [ ] Message contient email de contact (kenfackfranck08@gmail.com)
- [ ] User débloqué peut se reconnecter normalement

---

## 🚨 Si le message n'apparaît pas

### Debug frontend:

```javascript
// Dans la console du navigateur (page login)
// Essaie de te connecter, puis regarde:

console.log('Dernier fetch login:');
// Tu devrais voir: Response { status: 403 }

// Vérifie que l'erreur est bien catchée:
// Dans login/page.tsx ligne 39-43, le catch devrait logger
```

### Debug backend:

```bash
# Vérifie les logs
docker compose logs backend | grep -A 5 "blocked"
# Doit contenir: ValueError("blocked")
```

---

## 📝 Notes

- Le message backend est en français (explicite pour l'utilisateur)
- HTTP 403 (Forbidden) plutôt que 401 (Unauthorized) car c'est une restriction volontaire
- L'email de contact est hardcodé: `kenfackfranck08@gmail.com`
- Pour changer l'email, modifie: `backend/app/api/auth.py` ligne ~74

---

**Status:** ✅ Backend testé et fonctionnel | Frontend à tester manuellement
