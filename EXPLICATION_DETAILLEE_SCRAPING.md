# 🔍 EXPLICATION ULTRA-DÉTAILLÉE DU SCRAPING

## 🎯 Votre Question

**"Tu scrapes d'abord tout avant de rechercher des mots-clés dans ce qui a été obtenu, ou bien tu fais comment? Sur quels sites?"**

---

## 📊 RÉPONSE COURTE

**NON, on ne scrape PAS tout!**

On envoie directement les mots-clés (ex: "data-science") aux sites web, et ils nous donnent leurs résultats de recherche. C'est comme si vous alliez sur Indeed et tapiez "data-science" dans la barre de recherche.

**3 sites web actuellement supportés**:
1. ✅ **RemoteOK.com** (spécialisé 100% remote)
2. ✅ **Indeed.fr** (site généraliste français)
3. ✅ **WelcomeToTheJungle.com** (startups françaises)

---

## 🔬 EXPLICATION TECHNIQUE DÉTAILLÉE

### Étape 1: Vous Cliquez "Rechercher"

**Frontend envoie**:
```javascript
GET /api/v1/jobs/search?keyword=data-science&location=Paris&job_type=Stage
```

---

### Étape 2: Backend Appelle `search_hybrid()`

**Fichier**: `backend/app/services/search_service.py`

```python
async def search_hybrid(db, user_id, keywords, location, job_type, ...):
    # 1. Recherche DB locale
    db_offers = await JobOfferService.search_job_offers(...)
    
    # 2. Scraping Internet (si keywords fourni)
    if enable_scraping and keywords:
        scraping_result = await search_with_scraping(
            keywords=keywords,  # "data-science"
            location=location,   # "Paris"
            job_type=job_type,   # "Stage"
        )
```

---

### Étape 3: `search_with_scraping()` Lance Le Scraping

**Fichier**: `backend/app/services/search_service.py` ligne 28

```python
async def search_with_scraping(keywords, location, job_type, ...):
    # 1. Appelle le ScrapingService
    raw_results = await scraping_service.scrape_all_platforms(
        keywords=keywords,      # "data-science"
        location=location,      # "Paris"
        limit_per_platform=30   # Max 30 offres par site
    )
    
    # raw_results = {
    #     "remoteok": [offre1, offre2, ...],
    #     "indeed": [offre1, offre2, ...],
    #     "welcometothejungle": [offre1, offre2, ...]
    # }
```

---

### Étape 4: `scrape_all_platforms()` Scrape Les 3 Sites EN PARALLÈLE

**Fichier**: `backend/app/services/scraping_service.py` ligne 226

```python
async def scrape_all_platforms(keywords, location, limit_per_platform):
    """
    Lance le scraping sur les 3 sites EN MÊME TEMPS (parallèle)
    """
    results = {}
    
    # Scraping PARALLÈLE (3 sites en même temps)
    tasks = []
    for platform_name in ["remoteok", "indeed", "welcometothejungle"]:
        task = scrape_platform(
            platform_name,
            keywords="data-science",
            location="Paris",
            limit=30
        )
        tasks.append(task)
    
    # Attendre que les 3 scrapers finissent
    platform_results = await asyncio.gather(*tasks, return_exceptions=True)
    
    return {
        "remoteok": platform_results[0],           # 10 offres
        "indeed": platform_results[1],             # 15 offres
        "welcometothejungle": platform_results[2]  # 8 offres
    }
```

**Important**: Les 3 sites sont scrapés **en même temps**, pas l'un après l'autre!

---

### Étape 5: Chaque Scraper Fait Sa Recherche

Maintenant, détaillons **comment chaque site est scrapé**.

---

## 🌐 SITE 1: RemoteOK.com

**Fichier**: `backend/app/services/scrapers/remoteok_scraper.py`

### Méthode: API Publique (Pas de Scraping HTML)

RemoteOK a une **API publique gratuite** : `https://remoteok.com/api`

```python
async def scrape(keywords, location, max_results):
    """
    Scraper RemoteOK avec leur API publique
    """
    
    # 1. Appeler l'API publique
    api_url = "https://remoteok.com/api"
    
    # Fetch JSON
    response = await fetch(api_url)
    jobs = await response.json()  # Retourne TOUTES les offres
    
    # 2. Filtrer côté client avec les mots-clés
    filtered_jobs = []
    for job in jobs:
        # Chercher "data-science" dans le titre, tags, description
        if match_keywords(job, keywords="data-science"):
            filtered_jobs.append(job)
        
        if len(filtered_jobs) >= max_results:
            break
    
    # 3. Convertir en format standardisé
    offers = []
    for job in filtered_jobs:
        offers.append({
            "title": job["position"],         # "Data Scientist"
            "company": job["company"],        # "Google"
            "location": job["location"] or "Remote",
            "description": job["description"],
            "url": f"https://remoteok.com/remote-jobs/{job['slug']}",
            "source_platform": "remoteok",
            "job_type": detect_job_type(job["tags"]),  # Détecte "Stage" depuis tags
            "work_mode": "remote",            # Toujours remote
            "scraped_at": datetime.utcnow()
        })
    
    return offers
```

### Processus RemoteOK:

```
1. GET https://remoteok.com/api
   → Retourne ~500 offres en JSON (TOUTES les offres du site)

2. Filtrage LOCAL (côté Python):
   - Pour chaque offre:
     - Est-ce que "data-science" est dans title, tags ou description?
     - Est-ce que "Paris" est dans location? (rarissime car 100% remote)
   
   - Si OUI → Garder
   - Si NON → Ignorer

3. Limiter à 30 offres max

4. Retourner les offres filtrées
```

**Avantages**:
- ✅ Très rapide (1 seul appel HTTP)
- ✅ Pas de détection anti-bot
- ✅ Données structurées (JSON)

**Inconvénients**:
- ⚠️ On récupère TOUTES les offres (~500), puis on filtre
- ⚠️ Pas de recherche côté serveur (RemoteOK ne propose pas d'API de recherche)

---

## 🌐 SITE 2: Indeed.fr

**Fichier**: `backend/app/services/scrapers/indeed_scraper.py`

### Méthode: Scraping HTML avec Playwright

Indeed n'a **pas d'API publique**, on doit scraper le HTML directement.

```python
async def scrape(keywords, location, job_type, max_results):
    """
    Scraper Indeed.fr en simulant un navigateur
    """
    
    # 1. Construire l'URL de recherche
    search_url = _build_search_url(keywords, location, job_type)
    # Résultat: "https://fr.indeed.com/jobs?q=data-science&l=Paris&jt=internship"
    
    # 2. Ouvrir un navigateur headless (Playwright)
    await init_browser()  # Lance Chrome en mode invisible
    
    # 3. Naviguer vers l'URL de recherche
    page = await browser.new_page()
    await page.goto(search_url)
    
    # Indeed affiche directement les résultats filtrés!
    # On ne récupère PAS toutes les offres, juste celles qui matchent.
    
    # 4. Attendre que la page charge
    await page.wait_for_selector(".job_seen_beacon, .jobsearch-ResultsList")
    await sleep(random(2, 4))  # Anti-bot: attente aléatoire
    
    # 5. Extraire les offres de la page HTML
    offers = []
    job_cards = await page.query_selector_all(".job_seen_beacon")
    
    for card in job_cards:
        # Extraire titre
        title_elem = await card.query_selector(".jobTitle span")
        title = await title_elem.inner_text()
        
        # Extraire entreprise
        company_elem = await card.query_selector(".companyName")
        company = await company_elem.inner_text()
        
        # Extraire localisation
        location_elem = await card.query_selector(".companyLocation")
        location = await location_elem.inner_text()
        
        # Extraire URL
        link_elem = await card.query_selector("a[id^='job_']")
        href = await link_elem.get_attribute("href")
        url = f"https://fr.indeed.com{href}"
        
        # Créer l'offre
        offers.append({
            "title": title,
            "company": company,
            "location": location,
            "description": "",  # Pas dispo sur page résultats
            "url": url,
            "source_platform": "indeed",
            "job_type": job_type or "fulltime",
            "work_mode": "onsite",  # Par défaut
            "scraped_at": datetime.utcnow()
        })
        
        if len(offers) >= max_results:
            break
    
    # 6. Pagination (si besoin)
    if len(offers) < max_results:
        # Cliquer sur "Page suivante"
        next_button = await page.query_selector("a[data-testid='pagination-page-next']")
        if next_button:
            await next_button.click()
            await page.wait_for_selector(".job_seen_beacon")
            # Répéter l'extraction...
    
    # 7. Fermer le navigateur
    await browser.close()
    
    return offers
```

### Processus Indeed:

```
1. Construire URL de recherche:
   https://fr.indeed.com/jobs?q=data-science&l=Paris&jt=internship
   
   Paramètres:
   - q = mots-clés ("data-science")
   - l = localisation ("Paris")
   - jt = job type ("internship" = Stage)

2. Indeed fait la recherche côté serveur:
   - Indeed cherche "data-science" dans sa base de données
   - Indeed filtre par "Paris"
   - Indeed filtre par "Stage"
   - Indeed retourne une page HTML avec 15 résultats

3. On ouvre la page HTML avec Playwright (Chrome headless)

4. On extrait les données HTML:
   - Sélecteurs CSS: ".job_seen_beacon", ".jobTitle", ".companyName"
   - On parse le HTML pour extraire texte

5. On pagine (cliquer "Page suivante") si besoin

6. On retourne les offres extraites
```

**Avantages**:
- ✅ Recherche côté serveur (Indeed filtre pour nous)
- ✅ Données déjà filtrées par Indeed
- ✅ Pas besoin de tout récupérer

**Inconvénients**:
- ⚠️ Plus lent (navigateur headless)
- ⚠️ Risque anti-bot (Playwright simule un vrai navigateur pour contourner)
- ⚠️ Parsing HTML fragile (si Indeed change le HTML, ça casse)

---

## 🌐 SITE 3: WelcomeToTheJungle.com

**Fichier**: `backend/app/services/scrapers/wttj_scraper.py`

### Méthode: Scraping HTML avec Playwright

Similaire à Indeed, mais pour le site français WTTJ.

```python
async def scrape(keywords, location, job_type, max_results):
    """
    Scraper WelcomeToTheJungle.com
    """
    
    # 1. Construire l'URL
    search_url = f"https://www.welcometothejungle.com/fr/jobs?query={keywords}&refinementList[location.name][]={location}"
    # Résultat: "https://www.welcometothejungle.com/fr/jobs?query=data-science&refinementList[location.name][]=Paris"
    
    # 2. Ouvrir navigateur
    page = await browser.new_page()
    await page.goto(search_url)
    
    # 3. Attendre chargement (WTTJ utilise React/JS)
    await page.wait_for_selector("li[data-testid='job-list-item']", timeout=10000)
    await sleep(random(2, 4))
    
    # 4. Extraire offres
    job_items = await page.query_selector_all("li[data-testid='job-list-item']")
    
    offers = []
    for item in job_items:
        # Titre
        title_elem = await item.query_selector("h3")
        title = await title_elem.inner_text()
        
        # Entreprise
        company_elem = await item.query_selector(".company-name")
        company = await company_elem.inner_text()
        
        # URL
        link = await item.query_selector("a")
        href = await link.get_attribute("href")
        url = f"https://www.welcometothejungle.com{href}"
        
        offers.append({
            "title": title,
            "company": company,
            "location": location or "Paris",
            "url": url,
            "source_platform": "welcometothejungle",
            "scraped_at": datetime.utcnow()
        })
        
        if len(offers) >= max_results:
            break
    
    await browser.close()
    return offers
```

**Processus WTTJ**: Identique à Indeed (recherche côté serveur, scraping HTML).

---

## 🔄 ÉTAPE 6: Déduplication et Filtrage

Une fois les 3 scrapers terminés:

```python
# Résultats bruts
raw_results = {
    "remoteok": [10 offres],
    "indeed": [15 offres],
    "welcometothejungle": [8 offres]
}

# Total: 33 offres brutes

# 1. Aplatir la liste
all_offers = []
for platform, offers in raw_results.items():
    all_offers.extend(offers)

# all_offers = [33 offres]

# 2. Déduplication (enlever doublons)
deduplicated = []
seen_urls = set()
seen_signatures = set()

for offer in all_offers:
    # Doublon par URL?
    if offer["url"] in seen_urls:
        continue  # Ignorer
    
    # Doublon par titre+entreprise?
    signature = f"{offer['title']}|{offer['company']}"
    if signature in seen_signatures:
        continue  # Ignorer
    
    # C'est unique, on garde
    deduplicated.append(offer)
    seen_urls.add(offer["url"])
    seen_signatures.add(signature)

# deduplicated = [30 offres] (3 doublons enlevés)

# 3. Filtrage par job_type (si spécifié)
if job_type == "Stage":
    filtered = []
    for offer in deduplicated:
        # Est-ce un stage?
        if is_internship(offer):
            filtered.append(offer)

# filtered = [12 offres] (que des stages)

# 4. Sauvegarde en DB
for offer in filtered:
    db.insert(JobOffer(**offer, user_id=current_user.id))

# 5. Retour au frontend
return filtered  # 12 offres
```

---

## 📊 RÉSUMÉ DU PROCESSUS COMPLET

### Vous cherchez: "data-science + Paris + Stage"

```
1. Frontend → Backend: GET /api/v1/jobs/search?keyword=data-science&location=Paris&job_type=Stage

2. Backend lance 3 scrapers EN PARALLÈLE:

   ┌─────────────────────────────────────────────────────────┐
   │                  ScrapingService                        │
   ├─────────────────────────────────────────────────────────┤
   │                                                         │
   │  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │
   │  │ RemoteOK    │  │ Indeed.fr   │  │ WTTJ.com     │  │
   │  │             │  │             │  │              │  │
   │  │ API: GET    │  │ URL: https  │  │ URL: https   │  │
   │  │ /api        │  │ //fr.indeed │  │ //wttj/jobs  │  │
   │  │             │  │ .com/jobs?q │  │ ?query=data  │  │
   │  │ Filtre:     │  │ =data-scien │  │ -science     │  │
   │  │ "data-sci"  │  │ ce&l=Paris  │  │ &location=   │  │
   │  │ in tags     │  │ &jt=intern  │  │ Paris        │  │
   │  │             │  │             │  │              │  │
   │  │ Résultat:   │  │ Résultat:   │  │ Résultat:    │  │
   │  │ 10 offres   │  │ 15 offres   │  │ 8 offres     │  │
   │  └─────────────┘  └─────────────┘  └──────────────┘  │
   │         ↓                 ↓                 ↓         │
   └─────────────────────────────────────────────────────────┘
                              ↓
                    [33 offres brutes]
                              ↓
                    ┌──────────────────┐
                    │  Déduplication   │
                    │  - Par URL       │
                    │  - Par titre+cie │
                    └──────────────────┘
                              ↓
                    [30 offres uniques]
                              ↓
                    ┌──────────────────┐
                    │  Filtrage Stage  │
                    │  - Cherche "stag"│
                    │    "intern" dans │
                    │    titre/type    │
                    └──────────────────┘
                              ↓
                    [12 offres de stage]
                              ↓
                    ┌──────────────────┐
                    │  Sauvegarde DB   │
                    │  user_id=vous    │
                    └──────────────────┘
                              ↓
                    [Retour Frontend]
                    12 offres affichées
```

---

## 🎯 RÉPONSES À VOS QUESTIONS

### Q1: "Tu scrapes tout avant de rechercher?"

**NON!** 

- ✅ **RemoteOK**: On récupère toutes les ~500 offres de l'API, PUIS on filtre localement
- ✅ **Indeed**: On envoie directement "data-science + Paris" dans l'URL, Indeed filtre côté serveur
- ✅ **WTTJ**: Pareil, on envoie les mots-clés, WTTJ filtre côté serveur

**Seul RemoteOK récupère tout** (car leur API ne supporte pas la recherche).

---

### Q2: "Sur quels sites?"

**3 sites actuellement**:

1. ✅ **RemoteOK.com** 
   - Spécialité: Jobs 100% remote
   - Méthode: API publique JSON
   - Vitesse: Très rapide (1 requête HTTP)

2. ✅ **Indeed.fr**
   - Spécialité: Site généraliste français
   - Méthode: Scraping HTML avec Playwright
   - Vitesse: Moyen (3-5 secondes par page)

3. ✅ **WelcomeToTheJungle.com**
   - Spécialité: Startups et scale-ups françaises
   - Méthode: Scraping HTML avec Playwright
   - Vitesse: Moyen (3-5 secondes)

**Total temps**: 10-30 secondes pour scraper les 3 sites en parallèle.

---

### Q3: "Comment tu filtres?"

**Filtrage en 2 étapes**:

1. **Filtrage par site** (pendant le scraping):
   - RemoteOK: Cherche "data-science" dans title, tags, description
   - Indeed: Indeed filtre côté serveur (URL avec ?q=data-science)
   - WTTJ: WTTJ filtre côté serveur

2. **Filtrage après scraping** (backend Python):
   ```python
   # Filtre job_type="Stage"
   for offer in all_offers:
       title_lower = offer["title"].lower()
       job_type_lower = offer.get("job_type", "").lower()
       
       # Détecte "stage" ou "internship"
       if "stage" in title_lower or "intern" in title_lower or "internship" in job_type_lower:
           # C'est un stage!
           filtered_offers.append(offer)
   ```

---

## 🔧 CONFIGURATION DES PLATEFORMES

**Fichier**: `backend/app/platforms_config/platforms.py`

```python
PLATFORMS = {
    "remoteok": {
        "enabled": True,
        "priority": 1,
        "rate_limit": 500,  # 500 requêtes/heure
        "scraper_class": "RemoteOKScraper"
    },
    "indeed": {
        "enabled": True,
        "priority": 2,
        "rate_limit": 100,  # 100 requêtes/heure
        "scraper_class": "IndeedScraper"
    },
    "welcometothejungle": {
        "enabled": True,
        "priority": 3,
        "rate_limit": 200,
        "scraper_class": "WTTJScraper"
    }
}
```

---

## 🚀 EN RÉSUMÉ

| Site | Méthode | Recherche | Vitesse | Limites |
|------|---------|-----------|---------|---------|
| RemoteOK | API JSON | Local (Python) | ⚡ Très rapide | 500 req/h |
| Indeed | HTML Scraping | Serveur (URL) | 🐢 Moyen | 100 req/h, anti-bot |
| WTTJ | HTML Scraping | Serveur (URL) | 🐢 Moyen | 200 req/h |

**Stratégie**: 
- On envoie les mots-clés directement aux sites
- Les sites filtrent (sauf RemoteOK)
- On récupère les résultats filtrés
- On déduplique et re-filtre si besoin

**Pas de "scrape tout puis filtre"** sauf pour RemoteOK!

---

**Date**: 2026-01-31  
**Fichiers analysés**: 
- `backend/app/services/scraping_service.py`
- `backend/app/services/scrapers/remoteok_scraper.py`
- `backend/app/services/scrapers/indeed_scraper.py`
- `backend/app/services/scrapers/wttj_scraper.py`
