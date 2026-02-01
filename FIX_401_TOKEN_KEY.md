# 🔧 Fix: Erreur 401 Unauthorized - Clé localStorage Incohérente

## 🐛 Problème

**Symptôme**: `401 Unauthorized` sur `/api/v1/jobs/search`  
**Message**: "Impossible de valider les credentials"  
**Cause**: Incohérence des clés localStorage pour le token d'authentification

---

## 🔍 Analyse

### Clés localStorage Utilisées

**auth.ts** (service d'authentification):
```typescript
localStorage.setItem('auth_token', token);  // ✅ Correct
localStorage.getItem('auth_token');          // ✅ Correct
```

**jobOffer.ts** (avant le fix):
```typescript
localStorage.getItem('token');  // ❌ Mauvaise clé!
```

**Résultat**: 
- Le token est sauvegardé sous la clé `auth_token`
- Mais `jobOffer.ts` cherche sous la clé `token`
- → Le token n'est pas trouvé
- → Requête sans token
- → 401 Unauthorized

---

## ✅ Solution

### Changement dans jobOffer.ts

**Avant**:
```typescript
private getHeaders() {
  const token = localStorage.getItem("token");  // ❌ Mauvaise clé
  return {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  };
}
```

**Après**:
```typescript
private getHeaders() {
  const token = localStorage.getItem("auth_token");  // ✅ Bonne clé
  return {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  };
}
```

---

## 📁 Fichiers Modifiés

1. ✅ `frontend/src/lib/jobOffer.ts` - Ligne 8
   - Changé `localStorage.getItem("token")` → `localStorage.getItem("auth_token")`

---

## 🧪 Comment Tester

### 1. Effacez le cache du navigateur
```
F12 → Application → Local Storage → localhost:3000
→ Supprimer toutes les entrées
→ Ou simplement Ctrl+Shift+R (hard refresh)
```

### 2. Reconnectez-vous
```
1. Allez sur http://localhost:3000/auth/login
2. Email: john.doe@testmail.com
3. Password: Test2026!
4. Cliquez "Se connecter"
```

### 3. Testez la recherche
```
1. Allez sur http://localhost:3000/jobs
2. Entrez: Python / Paris
3. Cliquez "Rechercher"

ATTENDU:
✅ Pas d'erreur 401
✅ 🔵 Spinner "Recherche en cours..."
✅ ✅ "2 offres trouvées"
✅ Liste des offres affichée
```

---

## 🔍 Comment Détecter ce Bug

### Signes
- Erreur 401 alors qu'on est connecté
- Message "Impossible de valider les credentials"
- Token existe dans localStorage mais n'est pas envoyé
- Dans DevTools Network: Header `Authorization: Bearer null`

### Debug
```javascript
// Dans la console du navigateur (F12)
console.log('Token auth_token:', localStorage.getItem('auth_token'));
console.log('Token token:', localStorage.getItem('token'));
// Si le premier existe mais pas le second, c'est ce bug!
```

---

## 📊 Standardisation des Clés localStorage

Pour éviter ce problème à l'avenir, voici les clés utilisées dans l'application:

| Donnée | Clé localStorage | Utilisé par |
|--------|------------------|-------------|
| Token JWT | `auth_token` | auth.ts, api.ts, jobOffer.ts |
| User info | `user` | AuthContext.tsx |

**Règle**: Toujours utiliser `auth_token` pour le token, jamais `token`!

---

## 🎯 Résultat

**L'authentification fonctionne maintenant correctement!**

### État des Services
✅ Login/Register  
✅ Token sauvegardé  
✅ Token envoyé dans les requêtes  
✅ API accessible  
✅ Recherche fonctionnelle  

---

## 📝 Leçons Apprises

### ❌ Mauvaise Pratique
```typescript
// Différentes clés dans différents fichiers
localStorage.getItem('token');       // fichier1.ts
localStorage.getItem('auth_token');  // fichier2.ts
localStorage.getItem('jwt');         // fichier3.ts
```

### ✅ Bonne Pratique
```typescript
// Constante centralisée
const TOKEN_KEY = 'auth_token';

// Partout dans l'app
localStorage.getItem(TOKEN_KEY);
localStorage.setItem(TOKEN_KEY, value);
```

**Ou mieux encore**: Utiliser uniquement `authService.getToken()` qui gère la clé en interne!

---

## 🚨 Important

**Si vous voyez toujours l'erreur 401 après le fix**:
1. Effacez complètement le localStorage (F12 → Application → Clear)
2. Fermez le navigateur
3. Rouvrez et reconnectez-vous
4. Le nouveau token sera sauvegardé avec la bonne clé

---

**Date**: 2026-01-31 19:23  
**Status**: ✅ Corrigé et testé  
**Impact**: Critique → Recherche inutilisable sans authentification
