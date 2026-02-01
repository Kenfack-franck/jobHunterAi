# Plan: Recherche Asynchrone avec Feedback Temps Réel

## 🎯 Objectif
Implémenter un système de recherche d'offres asynchrone avec feedback progressif pour l'utilisateur.

## 📋 Flux Souhaité

```
1. Frontend → Backend: POST /jobs/search/async
   ↓
2. Backend → Frontend: Réponse immédiate { task_id, status: "pending" }
   ↓
3. Frontend: Affiche spinner/barre de progression
   ↓
4. Backend: Lance Celery task pour scraping
   ↓
5. Frontend: Poll GET /jobs/search/status/{task_id} toutes les 2s
   ↓
6. Backend → Frontend: Status updates
   - "pending": Recherche en file d'attente
   - "processing": Scraping en cours (X offres trouvées)
   - "completed": Terminé avec succès (retourne les offres)
   - "failed": Erreur (retourne le message d'erreur)
   ↓
7. Frontend: Affiche les résultats ou l'erreur
```

## 🔧 Implémentation

### Backend

#### 1. Nouveau endpoint: POST /api/v1/jobs/search/async
```python
@router.post("/search/async")
async def search_jobs_async(params: SearchRequest, user: User):
    # Lance la task Celery
    task = scrape_jobs_task.delay(
        user_id=str(user.id),
        keywords=params.keywords,
        location=params.location,
        job_type=params.job_type
    )
    
    return {
        "task_id": task.id,
        "status": "pending",
        "message": "Recherche lancée"
    }
```

#### 2. Nouveau endpoint: GET /api/v1/jobs/search/status/{task_id}
```python
@router.get("/search/status/{task_id}")
async def get_search_status(task_id: str, user: User):
    task = AsyncResult(task_id)
    
    if task.state == 'PENDING':
        return {"status": "pending", "message": "En attente..."}
    elif task.state == 'STARTED':
        return {"status": "processing", "message": "Scraping en cours..."}
    elif task.state == 'SUCCESS':
        return {
            "status": "completed",
            "offers": task.result,
            "count": len(task.result)
        }
    elif task.state == 'FAILURE':
        return {"status": "failed", "error": str(task.info)}
```

#### 3. Celery Task: scrape_jobs_task
```python
@celery_app.task(bind=True)
def scrape_jobs_task(self, user_id, keywords, location, job_type):
    self.update_state(state='STARTED', meta={'message': 'Scraping démarré'})
    
    try:
        # Scraping des offres
        offers = scrape_from_platforms(keywords, location, job_type)
        
        # Mise à jour progressive
        self.update_state(state='STARTED', meta={
            'message': f'{len(offers)} offres trouvées',
            'count': len(offers)
        })
        
        # Sauvegarde en base
        saved = save_offers_to_db(offers, user_id)
        
        return saved
    except Exception as e:
        self.update_state(state='FAILURE', meta={'error': str(e)})
        raise
```

### Frontend

#### 1. Fonction de recherche asynchrone
```typescript
const handleSearch = async () => {
  setSearchStatus('searching');
  
  // Lancer la recherche
  const response = await api.post('/jobs/search/async', searchParams);
  const { task_id } = response.data;
  
  // Polling du status
  const pollStatus = async () => {
    const statusResponse = await api.get(`/jobs/search/status/${task_id}`);
    const { status, offers, count, error } = statusResponse.data;
    
    if (status === 'pending' || status === 'processing') {
      setSearchStatus('searching');
      setStatusMessage(statusResponse.data.message);
      setTimeout(pollStatus, 2000); // Poll toutes les 2s
    } else if (status === 'completed') {
      setSearchStatus('success');
      setOffers(offers);
      setStatusMessage(`${count} offres trouvées`);
    } else if (status === 'failed') {
      setSearchStatus('error');
      setStatusMessage(error);
    }
  };
  
  pollStatus();
};
```

#### 2. UI avec barre de progression
```tsx
{searchStatus === 'searching' && (
  <div className="flex items-center gap-2 p-4 bg-blue-50">
    <Loader2 className="animate-spin" />
    <span>{statusMessage || 'Recherche en cours...'}</span>
  </div>
)}

{searchStatus === 'success' && (
  <div className="flex items-center gap-2 p-4 bg-green-50">
    <CheckCircle2 />
    <span>{statusMessage}</span>
  </div>
)}

{searchStatus === 'error' && (
  <div className="flex items-center gap-2 p-4 bg-red-50">
    <XCircle />
    <span>{statusMessage}</span>
  </div>
)}
```

## 📝 Fichiers à Créer/Modifier

### Backend
1. ✅ `backend/app/tasks/scraping_tasks.py` - Celery task pour scraping
2. ✅ `backend/app/api/job_offer.py` - Ajouter endpoints async
3. ✅ `backend/app/services/job_offer_service.py` - Logique de scraping

### Frontend
1. ✅ `frontend/src/lib/jobs.ts` - Service API pour recherche async
2. ✅ `frontend/src/app/jobs/page.tsx` - UI avec polling et feedback
3. ✅ `frontend/src/components/jobs/SearchStatus.tsx` - Composant de status

## 🎨 Design du Feedback

### États Visuels

**Idle** (Avant recherche):
```
[ Barre de recherche ]
[  Bouton Rechercher  ]
```

**Pending** (En attente):
```
🔵 ⟳ Recherche en file d'attente...
```

**Processing** (En cours):
```
🔵 ⟳ Scraping en cours... (X offres trouvées)
[================>      ] 60%
```

**Completed** (Succès):
```
✅ 25 offres trouvées et prêtes à l'affichage
[Liste des offres]
```

**Failed** (Erreur):
```
❌ Erreur: Impossible de se connecter aux plateformes
[Bouton Réessayer]
```

## ⚡ Optimisations

1. **Cache Redis**: Stocker les résultats de recherche pendant 5 min
2. **Debouncing**: Éviter les recherches multiples simultanées
3. **Annulation**: Permettre d'annuler une recherche en cours
4. **Pagination**: Charger les résultats par batch de 20

## 🧪 Tests à Effectuer

1. ✅ Recherche normale qui réussit
2. ✅ Recherche qui ne trouve rien
3. ✅ Recherche qui échoue (erreur réseau)
4. ✅ Recherches multiples en parallèle
5. ✅ Fermer le navigateur pendant la recherche (persistance)
6. ✅ Polling qui s'arrête après succès/erreur

---

**Prochaine étape**: Implémenter le backend (Celery task + endpoints)
