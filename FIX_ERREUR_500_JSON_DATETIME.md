# Fix Erreur 500 - JSON Serialization (datetime)

**Date**: 2026-02-03  
**Erreur**: `TypeError: Object of type datetime is not JSON serializable`

---

## 🐛 Problème

Lors de la recherche avec le mot-clé "Ingénieur", le backend récupérait 98 offres mais plantait lors de la sauvegarde dans le cache avec l'erreur :

```
TypeError: Object of type datetime is not JSON serializable
```

### Cause
Les objets d'offres contiennent des champs `scraped_at`, `published_at`, etc. qui sont des objets `datetime` Python. Quand le cache essaie de les sauvegarder en JSONB dans PostgreSQL, il ne peut pas les sérialiser.

---

## ✅ Solution

**Fichier** : `backend/app/services/search_cache_service.py`

### Ajout d'une fonction de nettoyage

```python
def _serialize_for_json(self, obj: Any) -> Any:
    """
    Convertit récursivement les objets datetime en chaînes ISO
    pour permettre la sérialisation JSON
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: self._serialize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [self._serialize_for_json(item) for item in obj]
    else:
        return obj
```

### Application avant sauvegarde

**Ligne 165** :
```python
# Nettoyer les résultats pour JSON (convertir datetime en ISO)
cleaned_results = self._serialize_for_json(results)

# Sauvegarder cleaned_results au lieu de results
cache_entry = SearchResultsCache(
    ...
    results=cleaned_results,  # ← Au lieu de results
    ...
)
```

---

## 🔍 Détails techniques

### Avant (erreur)
```python
results = [
    {
        "title": "Ingénieur...",
        "scraped_at": datetime(2026, 2, 3, 12, 10, 0),  # ❌ Objet datetime
        ...
    }
]
# → Erreur lors de INSERT INTO search_results_cache
```

### Après (fonctionnel)
```python
cleaned_results = [
    {
        "title": "Ingénieur...",
        "scraped_at": "2026-02-03T12:10:00",  # ✅ Chaîne ISO
        ...
    }
]
# → Sauvegarde OK
```

---

## ✅ Test

```bash
# Redémarrer backend
docker compose restart backend

# Tester recherche
http://localhost:3000/jobs
Intitulé: "Ingénieur"
→ Cliquer "Rechercher"
```

**Résultat attendu** : Offres affichées sans erreur 500

---

**Status** : ✅ Corrigé  
**Fichier modifié** : `backend/app/services/search_cache_service.py`  
**Backend redémarré** : Oui
