# 🧪 Guide de Test : Nouvelles Sources d'Offres

## 🎯 Objectif
Tester l'intégration de **RemoteOK + The Muse** (2 sources API gratuites)

---

## ✅ Configuration actuelle

| Source | Statut | Type | Offres attendues |
|--------|--------|------|------------------|
| **RemoteOK** | ✅ Actif | API publique | 20-50 (100% remote) |
| **The Muse** | ✅ Actif | API publique | 20-100 (tech/startups) |
| Adzuna | ⏸️ Désactivé | API (clés requises) | 0 (nécessite config) |
| Indeed | ⏸️ Désactivé | Anti-bot | 0 |
| WTTJ | ⏸️ Désactivé | Sélecteurs cassés | 0 |

**Résultat attendu** : 40-150 offres par recherche (au lieu de 20 avant)

---

## 🧪 Tests à effectuer

### Test 1 : Recherche Remote Tech ✅
**Critères** :
- Intitulé : `developer` ou `engineer`
- Mode : **Télétravail / Remote**
- Ville : *vide*
- Type : Fulltime

**Résultats attendus** :
- ✅ 20-50 offres **RemoteOK** (badge `🌐 RemoteOK`)
- ✅ 20-50 offres **The Muse** (badge `🎨 The Muse`)
- ✅ Total : **40-100 offres**

**Vérifications** :
1. Les badges sources sont différents (remoteok vs themuse)
2. Pas de doublons (même URL)
3. Descriptions sans HTML (`<div>`, etc.)

---

### Test 2 : Recherche Spécialisée (Python) ✅
**Critères** :
- Intitulé : `python developer`
- Mode : **Télétravail / Remote**
- Type : Fulltime

**Résultats attendus** :
- ✅ 10-30 offres **RemoteOK** (Python dans titre/tags)
- ✅ 5-20 offres **The Muse** (Python dans titre/description)
- ✅ Total : **15-50 offres**

---

### Test 3 : Recherche Stage Remote ⚠️
**Critères** :
- Intitulé : `software engineer`
- Mode : **Télétravail / Remote**
- Type : **Stage / Internship**

**Résultats attendus** :
- ✅ 5-15 offres **RemoteOK** (rare)
- ✅ 5-15 offres **The Muse** (stages remote)
- ✅ Total : **10-30 offres**

---

### Test 4 : Recherche Locale (Paris) ⚠️
**Critères** :
- Intitulé : `data scientist`
- Mode : Mixte ou Présentiel
- Ville : `Paris`
- Type : Fulltime

**Résultats attendus** :
- ⚠️ 0-5 offres **RemoteOK** (focus remote)
- ⚠️ 5-20 offres **The Muse** (quelques offres Paris)
- ⚠️ Total : **5-25 offres**

**Note** : Pour Paris, il faudra activer **Adzuna** (nécessite clés API).

---

## 🐛 Problèmes connus et solutions

### Problème 1 : "0 offre trouvée"
**Causes possibles** :
- Backend pas redémarré → `docker compose restart backend`
- Scrapers désactivés → Vérifier `platforms.py`
- Timeout API → Attendre 30-45 secondes

**Solution** :
```bash
docker compose logs backend --tail 30
# Chercher "[RemoteOK]" et "[TheMuse]"
```

---

### Problème 2 : Erreur 500 lors de la recherche
**Causes possibles** :
- Erreur dans un scraper (crash)
- API externe down

**Solution** :
```bash
docker compose logs backend --tail 50
# Identifier le scraper en erreur
```

Les autres scrapers continuent de fonctionner (erreurs isolées).

---

### Problème 3 : Doublons entre sources
**Normal** : La déduplication se fait par URL.

Si doublons persistent :
- Vérifier que les URLs sont identiques
- La déduplication par "signature" (titre+company) est à 90% de similarité

---

### Problème 4 : HTML dans descriptions
**Déjà corrigé** : La fonction `stripHtml()` nettoie le HTML.

Si ça persiste sur une source :
```typescript
// frontend/src/components/jobs/JobOfferCard.tsx:21
const stripHtml = (html: string) => {
  // Déjà implémenté
}
```

---

## 📊 Logs à surveiller

### Logs Backend (recherche)
```bash
docker compose logs backend -f | grep -E "(RemoteOK|TheMuse|SearchService)"
```

**Exemple de logs normaux** :
```
[SearchService] Début scraping: keywords=developer, location=remote
[RemoteOK] API: 23 offres récupérées
[TheMuse] Début scraping: keywords=developer, location=Flexible / Remote
[TheMuse] Scraping terminé. 18 offres récupérées.
[SearchService] 41 offres brutes récupérées
[SearchService] 40 offres après déduplication
```

---

## ✅ Checklist de validation

Après chaque test :
- [ ] La recherche retourne des offres
- [ ] Les badges sources sont visibles (🌐 RemoteOK, 🎨 The Muse)
- [ ] Pas de HTML dans les descriptions
- [ ] Le bouton "Enregistrer" apparaît sur les offres scrapées
- [ ] Le bouton "Analyser" fonctionne
- [ ] Génération CV/LM fonctionne (timeout 120s)

---

## 🚀 Activer Adzuna (optionnel)

Pour obtenir **100-200 offres** au lieu de 40-100 :

1. Créer compte sur https://developer.adzuna.com/signup
2. Obtenir APP_ID et APP_KEY
3. Éditer `backend/app/services/scrapers/adzuna_scraper.py` :
   ```python
   self.app_id = "VOTRE_APP_ID"
   self.app_key = "VOTRE_APP_KEY"
   ```
4. Activer dans `backend/app/platforms_config/platforms.py` :
   ```python
   "adzuna": {"enabled": True}
   ```
5. Redémarrer : `docker compose restart backend`

Voir **SCRAPERS_CONFIG.md** pour plus de détails.

---

## 📝 Rapport de test

**Résultats attendus** :
- Test 1 (remote tech) : ✅ 40-100 offres
- Test 2 (python remote) : ✅ 15-50 offres
- Test 3 (stage remote) : ✅ 10-30 offres
- Test 4 (Paris local) : ⚠️ 5-25 offres (attendre Adzuna)

**Temps de réponse** : 30-45 secondes (2 API en parallèle)

**Sources actives** : RemoteOK + The Muse (2/5)
