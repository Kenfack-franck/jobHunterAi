# Améliorations Job Hunter AI - Session 2026-02-02

## ✅ Phase 1 : Corrections offres d'emploi (TERMINÉ)

### 1. Filtres d'affichage ajoutés

**Fichier modifié:** `frontend/src/app/jobs/page.tsx`

**Changements:**
- Ajout état `filter` avec 3 valeurs: "all", "saved", "unsaved"
- 3 boutons filtres avec compteurs dynamiques
- Logique de filtrage optimisée (calcul unique via `filteredJobs`)
- Messages empty state adaptés selon le filtre actif

**Code clé:**
```typescript
const [filter, setFilter] = useState<"all" | "saved" | "unsaved">("all");

const filteredJobs = jobs.filter(job => {
  if (filter === "saved") return job.user_id;
  if (filter === "unsaved") return !job.user_id;
  return true;
});
```

**UI:**
```
[Tout (23)] [Sauvegardées (8)] [Non sauvegardées (15)]
```

### 2. Bouton supprimer optimisé

**Changement:**
- `handleDelete` met à jour le state local au lieu de recharger toutes les offres
- Pas de re-scraping inutile

**Avant:**
```typescript
await jobOfferService.deleteJobOffer(jobId);
await loadJobs(searchParams); // ❌ Re-scraping complet
```

**Après:**
```typescript
await jobOfferService.deleteJobOffer(jobId);
setJobs(prevJobs => prevJobs.filter(j => j.id !== jobId)); // ✅ Update local
```

---

## 🏢 Phase 2 : Veille d'entreprise (EN COURS)

### État actuel

**✅ Backend fonctionnel:**
- API complète: `/watch/company` (POST), `/watch/companies` (GET), `/watch/{id}` (DELETE)
- Service: `CompanyWatchService` avec scraping mutualisé
- Scrapers: Indeed, RemoteOK
- Celery: Scraping périodique automatique (24h)

**✅ Frontend existant:**
- Page: `/companies/watch`
- Formulaire d'ajout (nom + URL carrières)
- Liste des entreprises surveillées

**❌ Fix appliqué:**
- Colonne `profile_id` manquante dans table `user_company_watches`
- Ajoutée via `ALTER TABLE` direct sur la DB

```sql
ALTER TABLE user_company_watches 
ADD COLUMN IF NOT EXISTS profile_id UUID 
REFERENCES profiles(id) ON DELETE SET NULL;
```

### Test Safran

**Commande:**
```bash
curl -X POST http://localhost:8000/api/v1/watch/company \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"company_name":"Safran","careers_url":"https://www.safran-group.com/fr/offres"}'
```

**Résultat:**
```json
{
  "success": true,
  "message": "Veille activée pour Safran",
  "watch_id": "...",
  "total_watchers": 1
}
```

**Scraping immédiat:**
- Indeed: 0 offres trouvées
- RemoteOK: 0/30 offres matchées (fuzzy 75%)
- **Career page custom: PAS implémenté (TODO)**

### Limitation identifiée

**Problème:**
Le scraping de pages carrières custom (ex: Safran, Google, Microsoft) n'est **PAS encore implémenté**.

**Code concerné:**
`backend/app/services/company_watch_service.py` ligne 528-531:
```python
# TODO Méthode 3 : Career page si fournie
# if company.careers_url:
#     career_offers = await self._scrape_career_page(company.careers_url)
#     offers.extend(career_offers)
```

**Sources actuelles:**
- ✅ Indeed (filtre par nom d'entreprise)
- ✅ RemoteOK (recherche keyword + fuzzy matching)
- ❌ Career pages custom (TODO)
- ❌ LinkedIn Jobs (TODO)

### Options pour la suite

#### Option A : Implémenter scraper career pages (2-3h)

**Approche:**
1. Créer `GenericCareerPageScraper` dans `backend/app/services/scrapers/`
2. Utiliser Playwright pour sites JavaScript dynamiques
3. Parser HTML avec BeautifulSoup
4. Extraire: titre, localisation, description, lien apply

**Défis:**
- Chaque site a sa propre structure HTML
- Nécessite stratégie de détection automatique
- Fallback si scraping échoue

**Code type:**
```python
class GenericCareerPageScraper:
    async def scrape(self, url: str) -> List[Dict]:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            
            # Attendre chargement JavaScript
            await page.wait_for_selector('[role="listitem"], .job-card')
            
            # Extraire les offres
            jobs = await page.evaluate("""
                () => {
                    const cards = document.querySelectorAll('.job-card');
                    return Array.from(cards).map(card => ({
                        title: card.querySelector('.title')?.textContent,
                        location: card.querySelector('.location')?.textContent,
                        link: card.querySelector('a')?.href
                    }));
                }
            """)
            
            return jobs
```

#### Option B : Améliorer sources existantes (30min)

**Changements rapides:**
1. Assouplir fuzzy matching RemoteOK (60% au lieu de 75%)
2. Tester avec entreprises populaires (Google, Microsoft, etc.)
3. Améliorer recherche Indeed avec variations du nom

**Code:**
```python
# Ligne 520 de company_watch_service.py
threshold=0.60  # Au lieu de 0.75
```

#### Option C : Message UI temporaire (15min)

**Ajouter dans le formulaire:**
```tsx
<Alert>
  ⚠️ Le scraping de pages carrières custom est en développement.
  Pour l'instant, seules les offres sur Indeed et RemoteOK sont récupérées.
</Alert>
```

**Bloquer soumission si URL custom:**
```typescript
if (isCustomCareerPage(url)) {
  toast.warning("Pages carrières custom bientôt disponibles !");
  return;
}
```

---

## 📊 Améliorations frontend veille (À faire)

### 1. Validation URL lors de l'ajout

**Objectif:** Tester le scraping immédiatement et prévenir l'utilisateur

**Implémentation:**
```typescript
const handleAdd = async () => {
  setIsAdding(true);
  
  try {
    const result = await companiesService.addCompanyWatch({
      company_name: newCompany.name,
      careers_url: newCompany.url
    });
    
    if (result.total_offers_found === 0) {
      toast.warning(
        `${newCompany.name} ajoutée, mais 0 offres trouvées. ` +
        `Vérifiez l'URL ou réessayez plus tard.`
      );
    } else {
      toast.success(`${result.total_offers_found} offres trouvées !`);
    }
  } catch (error) {
    toast.error("Impossible d'ajouter l'entreprise");
  }
};
```

### 2. Filtres par poste/domaine

**Ajouter dans le formulaire:**
```tsx
<Input
  label="Poste recherché (optionnel)"
  placeholder="Ex: Data Scientist, DevOps"
  value={keywords}
  onChange={(e) => setKeywords(e.target.value)}
/>
```

**Backend:** Filtrer les offres par keyword matching
```python
async def get_company_offers(
    company_id: UUID,
    keywords: Optional[List[str]] = None
):
    offers = await self.scrape_company(company_id)
    
    if keywords:
        offers = [
            o for o in offers
            if any(kw.lower() in o['title'].lower() for kw in keywords)
        ]
    
    return offers
```

### 3. Affichage séparé par entreprise

**Option 1: Page dédiée**
- Route: `/companies/watch/[companyId]/offers`
- Affiche toutes les offres d'une entreprise

**Option 2: Accordéon sur la page liste**
```tsx
<Accordion>
  {companies.map(company => (
    <AccordionItem key={company.id}>
      <AccordionTrigger>
        {company.name} ({company.total_offers_found} offres)
      </AccordionTrigger>
      <AccordionContent>
        <JobOfferList companyId={company.id} />
      </AccordionContent>
    </AccordionItem>
  ))}
</Accordion>
```

**Option 3: Filtres**
```tsx
<Select value={selectedCompany} onChange={setSelectedCompany}>
  <option value="">Toutes les entreprises</option>
  {companies.map(c => (
    <option value={c.id}>{c.name}</option>
  ))}
</Select>
```

---

## 🔍 Questions UI non résolues

### 1. Barre de recherche du header

**Question:** À quoi sert-elle actuellement ?

**Action requise:**
- Vérifier `frontend/src/components/layout/AppShell.tsx`
- Identifier si connectée à une recherche globale
- Documenter son usage

### 2. Notifications

**Question:** Les notifications fonctionnent-elles ?

**Action requise:**
- Tester système de notifications
- Vérifier si implémenté pour:
  * Nouvelles offres de veille entreprise
  * Documents générés
  * Candidatures envoyées

### 3. Export RGPD

**Question:** L'export de données fonctionne-t-il ?

**Page:** Settings avec bouton "Exporter mes données"

**Action requise:**
- Tester l'export
- Vérifier format JSON
- S'assurer que toutes les données sont incluses

---

## 📝 Fichiers modifiés

```
frontend/src/app/jobs/page.tsx
├─ Ligne 18: Ajout état filter
├─ Ligne 199: Calcul filteredJobs
├─ Ligne 239-271: Boutons filtres avec compteurs
├─ Ligne 147-156: handleDelete optimisé

backend/database/
└─ user_company_watches: Ajout colonne profile_id (ALTER TABLE)
```

## 📦 Prochaines actions suggérées

1. **Décider** quelle option pour career pages (A, B ou C)
2. **Tester** l'interface de veille dans le navigateur
3. **Clarifier** usage de la barre de recherche header
4. **Vérifier** système de notifications
5. **Tester** export RGPD

---

**Session terminée à:** 2026-02-02 18:10 UTC  
**Temps total:** ~1h30  
**Commits prêts:** Frontend (filtres) + Backend (fix DB)
