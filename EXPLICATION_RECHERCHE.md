# 🔍 EXPLICATION: Comment Fonctionne la Recherche d'Offres

## ❓ Votre Question

**"Quand je cherche 'data-science + Paris + Stage', j'ai 0 résultats. Comment faites-vous la recherche sur Internet et comment triez-vous les offres?"**

---

## 🚨 LA VÉRITÉ: PAS DE SCRAPING EN TEMPS RÉEL ACTUELLEMENT

### Ce Qui Se Passe VRAIMENT

Quand vous cliquez sur "Rechercher", voici ce qui arrive:

```
1. Frontend envoie requête → Backend endpoint GET /api/v1/jobs/search
2. Backend fait une requête SQL sur la BASE DE DONNÉES
3. Backend cherche UNIQUEMENT dans les offres DÉJÀ ENREGISTRÉES
4. Backend retourne les résultats (ou 0 si rien ne matche)
```

**Il N'Y A PAS de scraping en temps réel sur Internet!**

### Code Actuel (Backend)

**Fichier**: `backend/app/services/job_offer_service.py` ligne 111

```python
async def search_job_offers(
    db: AsyncSession,
    user_id: UUID,
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    job_type: Optional[str] = None,
    company_name: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
) -> List[JobOffer]:
    """
    Rechercher des offres avec filtres
    Recherche dans: job_title, description, company_name
    """
    # JUSTE UNE REQUÊTE SQL!
    query = select(JobOffer).where(JobOffer.user_id == user_id)
    
    if keyword:
        keyword_filter = or_(
            JobOffer.job_title.ilike(f"%{keyword}%"),
            JobOffer.description.ilike(f"%{keyword}%"),
            JobOffer.requirements.ilike(f"%{keyword}%")
        )
        query = query.where(keyword_filter)
    
    if location:
        query = query.where(JobOffer.location.ilike(f"%{location}%"))
    
    if job_type:
        query = query.where(JobOffer.job_type.ilike(f"%{job_type}%"))
    
    result = await db.execute(query)
    return list(result.scalars().all())
```

**Traduction**: 
- ✅ Cherche dans la base de données PostgreSQL
- ❌ NE fait PAS de scraping sur LinkedIn, Indeed, RemoteOK, etc.
- ❌ NE va PAS sur Internet chercher de nouvelles offres

---

## 📊 Pourquoi Vous Avez 0 Résultats

### Base de Données Actuelle

Voici ce qu'il y a dans la DB (5 offres de test):

```sql
-- Offre 1
job_title: "Senior Python Developer"
location: "Paris, France"
job_type: "CDI"
user_id: <john.doe@testmail.com>

-- Offre 2
job_title: "Python Backend Engineer"
location: "Paris"
job_type: "CDI"
user_id: <john.doe@testmail.com>

-- Offre 3, 4, 5
job_title: "Backend Developer", "Full-Stack Engineer", "DevOps Engineer"
location: "Remote", "Lyon", "Marseille"
job_type: "CDI", "CDD", "Freelance"
user_id: <john.doe@testmail.com>
```

### Votre Recherche

```
Mot-clé: "data-science"
Lieu: "Paris"
Type: "Stage"
User: kenfackfranck08@gmail.com
```

### Pourquoi 0 Résultats?

**3 raisons**:

1. ❌ **Aucune offre "data-science"** dans la DB (seulement Python Developer)
2. ❌ **Aucune offre de type "Stage"** dans la DB (seulement CDI, CDD, Freelance)
3. ❌ **Les offres existantes appartiennent à john.doe@testmail.com**, PAS à vous!

**Le code filtre par `user_id`** (ligne 125):
```python
query = select(JobOffer).where(JobOffer.user_id == user_id)
```

Donc même si une offre "Python + Paris" existe, si elle appartient à un autre utilisateur, vous ne la verrez pas!

---

## 🛠️ Comment Ça DEVRAIT Fonctionner (Architecture Prévue)

### Scénario Idéal

```
1. Vous cherchez "data-science + Paris + Stage"
2. Backend lance une TASK CELERY asynchrone
3. Celery déclenche le SCRAPING:
   - RemoteOK scraper → cherche sur remoteok.com
   - Indeed scraper → cherche sur indeed.fr
   - WTTJ scraper → cherche sur welcometothejungle.com
4. Les scrapers récupèrent 50+ offres en temps réel
5. Backend déduplique (enlève les doublons)
6. Backend filtre par vos critères (Stage, Paris, data-science)
7. Backend SAUVEGARDE les offres dans la DB
8. Backend retourne les résultats
9. Vous voyez 15 offres fraîches d'Internet
```

### Code Qui Existe Déjà (Mais Pas Utilisé)

**Fichier**: `backend/app/services/search_service.py`

```python
async def search_with_scraping(
    self,
    db: AsyncSession,
    keywords: str,
    location: Optional[str] = None,
    job_type: Optional[str] = None,
    work_mode: Optional[str] = None,
    company: Optional[str] = None,
    limit_per_platform: int = 100,
    user_id: Optional[str] = None
) -> Dict:
    """
    Recherche d'offres avec scraping des plateformes activées
    """
    # 1. Scraping depuis toutes les plateformes
    raw_results = await self.scraping_service.scrape_all_platforms(
        keywords=keywords,
        location=location or "",
        limit_per_platform=limit_per_platform
    )
    
    # 2. Déduplication
    deduplicated_offers = await self.deduplicate_offers(all_offers)
    
    # 3. Filtrage par critères
    filtered_offers = self._filter_offers(
        deduplicated_offers,
        job_type=job_type,
        work_mode=work_mode,
        company=company
    )
    
    # 4. Sauvegarde en DB
    saved_offers = await self._save_offers_to_db(
        db, filtered_offers, user_id
    )
    
    return {
        "offers": saved_offers,
        "count": len(saved_offers),
        "metadata": { ... }
    }
```

**CE CODE EXISTE** mais n'est **PAS APPELÉ** par l'endpoint `/api/v1/jobs/search`!

---

## 🔧 Pourquoi Ce N'est Pas Activé?

### Problème 1: Celery Worker Ne Fonctionne Pas

```bash
# Logs du worker
ModuleNotFoundError: No module named 'pgvector'
```

Le worker Celery crash immédiatement, donc impossible de lancer des tasks asynchrones.

### Problème 2: Endpoint Utilise La Mauvaise Fonction

**Actuellement** (`backend/app/api/job_offer.py` ligne 74):
```python
offers = await JobOfferService.search_job_offers(db, user_id, ...)
                                # ^^^^^ Recherche DB uniquement
```

**Devrait être**:
```python
from app.services.search_service import search_service

result = await search_service.search_with_scraping(
    db, keywords, location, job_type, ...
)
offers = result["offers"]
```

### Problème 3: Frontend N'Utilise Pas L'API Async

**Frontend** (`src/lib/jobOffer.ts` ligne 39):
```typescript
async searchJobOffers(params: JobOfferSearchParams): Promise<JobOffer[]> {
    const response = await axios.get(`${API_URL}/jobs/search`, {
        params: queryParams
    });
    return response.data;
}
```

**Devrait utiliser** (ligne 82-95):
```typescript
async searchJobsAsync(params: JobOfferSearchParams) {
    // Lance la recherche async
    const { task_id } = await axios.post(`${API_URL}/jobs/search/async`, ...)
    
    // Poll le statut
    while (true) {
        const status = await axios.get(`${API_URL}/jobs/search/status/${task_id}`)
        if (status.state === "SUCCESS") return status.result;
    }
}
```

---

## ✅ SOLUTION COMPLÈTE

### Option A: Recherche Synchrone avec Scraping (Sans Celery)

**Avantage**: Pas besoin de Celery  
**Inconvénient**: Temps d'attente de 30-60 secondes

**Modification**: `backend/app/api/job_offer.py`

```python
@router.get("/search", response_model=List[JobOfferResponse])
async def search_job_offers(
    keyword: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    job_type: Optional[str] = Query(None),
    company_name: Optional[str] = Query(None),
    scraping_enabled: bool = Query(True),  # NOUVEAU!
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Recherche avec ou sans scraping"""
    
    if scraping_enabled and keyword:  # Si scraping demandé
        from app.services.search_service import search_service
        
        result = await search_service.search_with_scraping(
            db=db,
            keywords=keyword,
            location=location,
            job_type=job_type,
            company=company_name,
            limit_per_platform=50,
            user_id=str(current_user.id)
        )
        return result["offers"]
    else:  # Sinon, recherche DB classique
        offers = await JobOfferService.search_job_offers(
            db, current_user.id, keyword, location, job_type, company_name
        )
        return offers
```

---

### Option B: Recherche Asynchrone avec Celery (Idéal)

**Étape 1**: Fixer Celery

```bash
echo "pgvector==0.2.4" >> backend/requirements.txt
docker-compose down
docker-compose up -d --build
```

**Étape 2**: Modifier le frontend pour utiliser l'endpoint async

```typescript
// Dans jobs/page.tsx
const loadJobs = async (params: JobOfferSearchParams = {}) => {
    setLoading(true);
    setSearchStatus("searching");
    setSearchMessage("🔄 Lancement du scraping...");
    
    try {
        // Lancer la recherche async
        const { task_id } = await jobOfferService.searchJobsAsync(params);
        
        // Polling toutes les 2 secondes
        const interval = setInterval(async () => {
            const status = await jobOfferService.getSearchStatus(task_id);
            
            if (status.state === "STARTED") {
                setSearchMessage(`🔍 Scraping en cours... ${status.found_count || 0} offres trouvées`);
            } else if (status.state === "SUCCESS") {
                clearInterval(interval);
                setJobs(status.result);
                setSearchStatus("success");
                setSearchMessage(`✅ ${status.result.length} offres trouvées !`);
                setLoading(false);
            }
        }, 2000);
    } catch (error) {
        // ...
    }
};
```

---

## 🎯 RÉSUMÉ

| Question | Réponse |
|----------|---------|
| **Comment vous faites la recherche sur Internet?** | ❌ Actuellement: ON NE LE FAIT PAS. Recherche uniquement en DB |
| **Comment vous triez les offres?** | ❌ Actuellement: Pas de tri, juste un filtre SQL WHERE |
| **Pourquoi 0 résultats?** | Aucune offre "data-science + Stage" dans la DB, et les offres existantes appartiennent à un autre user |
| **Le scraping existe?** | ✅ OUI! Code existe mais pas utilisé (Celery crash) |
| **Comment activer le scraping?** | Option A: Modifier endpoint pour appeler `search_service.search_with_scraping()` <br> Option B: Fixer Celery et utiliser l'API async |

---

## 🚀 ACTIONS POSSIBLES

### Action Immédiate (Pour Tester Avec Vraies Offres)

**Ajouter manuellement des offres de test dans VOTRE compte**:

```sql
-- Se connecter à Postgres
docker exec -it <postgres_container> psql -U postgres -d jobhunter

-- Ajouter des offres pour votre user_id
INSERT INTO job_offers (
    id, user_id, company_name, job_title, location, job_type, 
    description, created_at, updated_at
) VALUES (
    gen_random_uuid(),
    '<votre_user_id>',  -- Trouver avec SELECT * FROM users WHERE email='kenfackfranck08@gmail.com';
    'Google',
    'Data Scientist - Stage',
    'Paris',
    'Stage',
    'Analyser des données avec Python et TensorFlow',
    NOW(),
    NOW()
);
```

### Action Court-Terme (Activer Scraping Synchrone)

Modifier `backend/app/api/job_offer.py` pour appeler `search_with_scraping()` au lieu de `search_job_offers()`.

### Action Long-Terme (Vrai Scraping Async)

1. Fixer Celery (pgvector)
2. Modifier frontend pour utiliser API async
3. Tester avec vraies recherches

---

**Date**: 2026-01-31  
**Conclusion**: La recherche actuelle est une **recherche en base de données locale**, PAS un scraping en temps réel d'Internet. Le code de scraping existe mais n'est pas activé.
