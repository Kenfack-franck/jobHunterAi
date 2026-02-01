# 🎯 TESTEZ L'APPLICATION MAINTENANT!

## ⚠️ IMPORTANT: Effacez d'abord le cache!

```
Appuyez sur: Ctrl + Shift + R
```

## 🔑 Connexion

**URL**: http://localhost:3000/auth/login  
**Email**: `john.doe@testmail.com`  
**Password**: `Test2026!`

---

## ✅ Test 1: Recherche (1 min)

1. Allez sur "Recherche d'Offres"
2. Entrez: `Python` + `Paris`
3. Cliquez "Rechercher"

**Attendu**:
- 🔵 Message bleu "Recherche en cours..."
- ✅ Message vert "2 offres trouvées"
- 📋 2 offres affichées

---

## ✅ Test 2: Analyse (1 min)

1. Sur une offre, cliquez "Analyser"
2. Modal s'ouvre

**Attendu**:
- ✅ Score de compatibilité (ex: 58%)
- ✅ Sélection de profil
- ✅ Bouton "Générer les documents"
- ❌ Pas d'erreur 404 ou 401

---

## ✅ Test 3: Formulaire (2 min)

1. Allez sur "Profil"
2. Ajoutez une expérience:
   - Poste: Tech Lead
   - Entreprise: Test Inc
   - Date début: 2025-01-01
   - **NE PAS remplir date fin**
   - Cocher "Poste actuel"
3. Cliquez "Ajouter"

**Attendu**:
- ✅ Expérience ajoutée sans erreur 422

---

## 🐛 Si Ça Ne Marche Pas

### Erreur 401
```
1. F12 → Application → Local Storage → Clear
2. Fermez le navigateur
3. Rouvrez et reconnectez-vous
```

### Erreur 404
```
1. Vérifiez l'URL dans Network (F12)
2. Si /api/v1/api/v1/: Frontend pas à jour
3. Solution: docker compose restart frontend
```

---

**Donnez-moi vos retours!** 🚀
