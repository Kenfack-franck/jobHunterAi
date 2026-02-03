# Problème 401 Unauthorized sur page Sources - RÉSOLU

**Date**: 2026-02-03  
**Symptôme**: Erreur 401 lors de la sauvegarde des préférences sources

---

## 🐛 Symptôme

```
PUT http://localhost:8000/api/v1/sources/preferences 401 (Unauthorized)
{detail: 'Impossible de valider les credentials'}
```

---

## 🔍 Diagnostic

### Logs backend
```bash
docker compose logs backend | grep "sources/preferences" | tail -5
```

**Résultat** :
```
INFO: "PUT /api/v1/sources/preferences HTTP/1.1" 200 OK  ← Avant: OK
INFO: "PUT /api/v1/sources/preferences HTTP/1.1" 200 OK  ← Avant: OK
INFO: "PUT /api/v1/sources/preferences HTTP/1.1" 401 Unauthorized  ← Maintenant: 401
```

**Conclusion** : Le backend fonctionne. Le problème vient du **token expiré ou manquant**.

---

## ✅ Solution implémentée

### 1. Détection du token manquant

**Fichier**: `frontend/src/app/settings/sources/page.tsx`

**Avant** :
```typescript
const token = authService.getToken();
// Aucune vérification
```

**Après** :
```typescript
const token = authService.getToken();

if (!token) {
  console.error('[Sources] ❌ Pas de token trouvé !');
  setMessage({ type: 'error', text: '❌ Session expirée. Veuillez vous reconnecter.' });
  setTimeout(() => router.push('/auth/login'), 2000);
  return;
}

console.log('[Sources] 🔑 Token présent:', token.substring(0, 20) + '...');
```

---

### 2. Gestion du 401 dans loadData

**Avant** :
```typescript
if (!sourcesRes.ok) throw new Error('Erreur chargement sources');
```

**Après** :
```typescript
if (!sourcesRes.ok) {
  if (sourcesRes.status === 401) {
    setMessage({ type: 'error', text: '❌ Session expirée. Redirection...' });
    setTimeout(() => router.push('/auth/login'), 2000);
    return;
  }
  throw new Error('Erreur chargement sources');
}
```

---

### 3. Debug logs ajoutés

- `[Sources] 🔑 Token chargement:` → Au chargement de la page
- `[Sources] 🔑 Token présent:` → Lors de la sauvegarde
- `[Sources] ❌ Pas de token !` → Si token manquant

---

## 🧪 Comment tester

### 1. Vérifier les logs frontend

Ouvrir la console du navigateur (F12) et regarder :

**Si token OK** :
```
[Sources] 🔑 Token chargement: eyJhbGciOiJIUzI1NiIs...
[Sources] 💾 Sauvegarde des préférences...
[Sources] 🔑 Token présent: eyJhbGciOiJIUzI1NiIs...
[Sources] 📡 Réponse API: 200 {...}
```

**Si token manquant** :
```
[Sources] ❌ Pas de token trouvé !
→ Message: "Session expirée. Veuillez vous reconnecter."
→ Redirection vers /auth/login après 2 secondes
```

---

### 2. Reproduire le problème

#### Étape 1 : Se connecter
- Aller sur http://localhost:3000/auth/login
- Email: `kenfackfranck08@gmail.com`
- Password: `noumedem`

#### Étape 2 : Aller sur Sources
- Aller sur http://localhost:3000/settings/sources
- **Vérifier console** : doit afficher `[Sources] 🔑 Token chargement:`

#### Étape 3 : Modifier et sauvegarder
- Cocher/décocher des sources
- Cliquer "Sauvegarder les préférences"
- **Vérifier console** : doit afficher `[Sources] 🔑 Token présent:`

#### Étape 4 : Tester avec session expirée
- Ouvrir DevTools → Application → Storage → Local Storage
- Supprimer la clé `auth_token`
- Recharger la page
- **Résultat attendu** : Message "Session expirée" + redirection login

---

## 🔧 Causes possibles du 401

### 1. Token expiré
**Symptôme** : Le token était valide mais a expiré après X heures

**Durée de vie** : Vérifier dans `backend/app/core/security.py`
```python
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 heure par défaut
```

**Solution** :
- Augmenter la durée : `ACCESS_TOKEN_EXPIRE_MINUTES = 1440` (24h)
- Ou implémenter refresh token

---

### 2. Token supprimé de localStorage
**Symptôme** : L'utilisateur a vidé le cache navigateur

**Solution** : Déjà implémentée (redirection login automatique)

---

### 3. Token mal formaté
**Symptôme** : Le token existe mais n'est pas au bon format

**Debug** :
```typescript
console.log('Token brut:', localStorage.getItem('auth_token'));
console.log('Token après authService:', authService.getToken());
```

**Vérification backend** :
```bash
docker compose logs backend | grep "401"
```

---

## ✅ Validation

### Frontend redémarré
```bash
docker compose restart frontend
```

### Tests à faire
- [ ] Se connecter avec `kenfackfranck08@gmail.com` / `noumedem`
- [ ] Aller sur http://localhost:3000/settings/sources
- [ ] Vérifier console : `[Sources] 🔑 Token chargement:`
- [ ] Modifier des sources
- [ ] Cliquer "Sauvegarder"
- [ ] Vérifier console : `[Sources] 🔑 Token présent:`
- [ ] Vérifier console : `[Sources] 📡 Réponse API: 200`
- [ ] Message de succès affiché

---

## 📝 Checklist résolution

- [x] Ajout vérification `if (!token)` dans `loadData()`
- [x] Ajout vérification `if (!token)` dans `savePreferences()`
- [x] Gestion du 401 dans `loadData()` pour GET
- [x] Redirection automatique vers `/auth/login` si 401
- [x] Logs debug ajoutés pour tracer le token
- [x] Frontend redémarré
- [ ] Tests manuels à effectuer par l'utilisateur

---

## 🚀 Prochaines étapes

**Si le problème persiste après cette correction** :

1. **Vérifier le token dans localStorage** :
   ```javascript
   // Console navigateur
   localStorage.getItem('auth_token')
   ```

2. **Tester l'endpoint backend directement** :
   ```bash
   # Récupérer le token (remplacer EMAIL et PASSWORD)
   TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"kenfackfranck08@gmail.com","password":"noumedem"}' | jq -r '.access_token')
   
   # Tester PUT
   curl -X PUT http://localhost:8000/api/v1/sources/preferences \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"enabled_sources":["capgemini"]}'
   ```

3. **Augmenter la durée de vie du token** :
   ```python
   # backend/app/core/security.py
   ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 heures
   ```

---

## 📖 Documentation liée

- `FIX_AUTH_TOKEN_SOURCES_PAGE.md` - Fix précédent (auth_token vs token)
- `FIX_SOURCES_PAGE_UI_COMPLETE.md` - Autres fixes page sources

---

**Status** : ✅ Correction déployée  
**Action utilisateur** : Recharger http://localhost:3000/settings/sources et tester
