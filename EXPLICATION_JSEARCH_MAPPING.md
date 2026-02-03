# Explication : Mapping Entreprises → JSearch API 🔍

## Vos Questions ❓

### Question 1: "Est-ce qu'on pourra encore avoir les offres uniquement pour une entreprise choisie ?"

✅ **OUI**, JSearch permet de filtrer par entreprise !

**Comment ça marche** :
```python
# Si vous sélectionnez Capgemini
JSearch.scrape(
    keywords="Python",
    company="Capgemini",  # ← Filtre entreprise
    location="France"
)

# Résultat: Seulement les offres de Capgemini
```

**API JSearch** : `https://jsearch.p.rapidapi.com/search?query=Python&company=Capgemini`

---

### Question 2: "Si je sélectionne 2 entreprises, j'aurais uniquement leurs offres ?"

✅ **OUI**, vous aurez UNIQUEMENT les offres des entreprises sélectionnées !

**Exemple concret** :
```
Sélection utilisateur:
  ☑️ Capgemini
  ☑️ L'Oréal
  ☐ Airbus (pas coché)
  ☐ Thales (pas coché)

Requêtes effectuées:
  → JSearch(company="Capgemini") → 15 offres
  → JSearch(company="L'Oréal")   → 8 offres

Résultat final:
  Total: 23 offres (15 + 8)
  ✅ Capgemini: 15 offres
  ✅ L'Oréal: 8 offres
  ❌ Airbus: 0 offres (non sélectionné)
  ❌ Thales: 0 offres (non sélectionné)
```

**Le code fait** :
```python
enabled_sources = ["capgemini", "loreal"]  # Ce que vous cochez

for source_id in enabled_sources:
    company_name = get_company_name(source_id)  # "Capgemini", "L'Oréal"
    offers = await jsearch.scrape(company=company_name)
    results[source_id] = offers
```

---

### Question 3: "Cela veut dire que tu ne vas plus scraper leur site carrière ?"

⚠️ **OUI et NON** - C'est un **compromis** :

#### Option A: Mapping vers JSearch (CE QUE JE PROPOSE)

**Ce qui se passe** :
```
Vous sélectionnez: Capgemini
    ↓
Backend NE scrape PAS le site Capgemini directement
    ↓
Backend appelle JSearch API: "company=Capgemini"
    ↓
JSearch retourne offres de Capgemini qu'il a indexé
    ↓
Vous voyez les offres
```

**D'où viennent les offres JSearch ?**
- JSearch scrape LinkedIn, Indeed, Glassdoor
- JSearch cherche "company:Capgemini" sur ces sites
- JSearch a déjà indexé les offres

**Avantages** ✅:
- Fonctionne IMMÉDIATEMENT (quelques heures)
- Filtre par entreprise : OUI
- Maintenance : Zéro (JSearch s'en occupe)
- Données structurées et propres
- Coût : Gratuit (100 requêtes/mois) ou $10/mois (1000 req)

**Inconvénients** ⚠️:
- ❌ On ne scrape PAS directement https://www.capgemini.com/fr-fr/carrieres/
- ❌ Dépend de ce que JSearch a indexé
- ❌ Peut manquer des offres très récentes (postées aujourd'hui sur le site Capgemini)
- ❌ Limite de requêtes API

---

#### Option B: Scraper Direct du Site Carrière (IDÉAL MAIS LONG)

**Ce qui se passerait** :
```
Vous sélectionnez: Capgemini
    ↓
Backend VA sur https://www.capgemini.com/fr-fr/carrieres/
    ↓
Backend scrape DIRECTEMENT leur page HTML
    ↓
Backend parse les offres
    ↓
Vous voyez les offres (les plus récentes, les plus complètes)
```

**Avantages** ✅:
- ✅ Scraping DIRECT du site officiel
- ✅ Offres les plus récentes (en temps réel)
- ✅ Aucune limite de requêtes
- ✅ Toutes les offres disponibles

**Inconvénients** ⚠️:
- ❌ Chaque site est différent → 15 scrapers à créer
- ❌ Temps de développement : 3-5 jours
- ❌ Maintenance continue (sites changent)
- ❌ Peut être bloqué par anti-bot
- ❌ Plus complexe

---

## 🎯 Comparaison Concrète

### Scénario: Vous cherchez "Python Developer" chez Capgemini

| Aspect | JSearch API (Option A) | Scraping Direct (Option B) |
|--------|------------------------|---------------------------|
| **Source des offres** | LinkedIn + Indeed + Glassdoor | Site Capgemini.com |
| **Vous sélectionnez** | ☑️ Capgemini | ☑️ Capgemini |
| **Résultat** | Offres de Capgemini trouvées sur LinkedIn/Indeed | Offres de Capgemini trouvées sur leur site |
| **Nombre d'offres** | ~15-30 offres | ~20-50 offres (plus complet) |
| **Fraîcheur** | Indexées il y a quelques jours | Temps réel (aujourd'hui) |
| **Filtrage entreprise** | ✅ OUI (company=Capgemini) | ✅ OUI (scrape que Capgemini) |
| **Temps d'implémentation** | 4-6 heures | 3-5 jours |
| **Maintenance** | Zéro | Continue |
| **Coût** | Gratuit/Payant API | Gratuit |

---

## 💡 MA RECOMMANDATION : Solution HYBRIDE

### Phase 1: DÉBLOCAGE IMMÉDIAT (Aujourd'hui)

**Utiliser JSearch pour les 15 entreprises** :

```python
# backend/app/services/scraping_service.py
mapping = {
    # Agrégateurs (direct)
    "remoteok": "remoteok",  # ✅ Scraping direct
    
    # Entreprises (via JSearch)
    "capgemini": "jsearch",       # → JSearch(company="Capgemini")
    "sopra_steria": "jsearch",    # → JSearch(company="Sopra Steria")
    "dassault_systemes": "jsearch", # → JSearch(company="Dassault Systemes")
    "loreal": "jsearch",          # → JSearch(company="L'Oréal")
    # ... etc pour les 15 entreprises
}
```

**Résultat** :
- ✅ Vous sélectionnez Capgemini → Vous avez des offres Capgemini
- ✅ Vous sélectionnez 2 entreprises → Vous avez LEURS offres uniquement
- ✅ Fonctionne en quelques heures
- ⚠️ Via agrégateurs (pas scraping direct)

---

### Phase 2: SCRAPING DIRECT (Plus tard)

**Implémenter scrapers spécifiques** pour les 5 entreprises les plus demandées :

```python
mapping = {
    # Agrégateurs (direct)
    "remoteok": "remoteok",
    
    # Top 5 entreprises (scraping direct)
    "capgemini": "capgemini_direct",     # ✅ Scrape capgemini.com
    "airbus": "airbus_direct",           # ✅ Scrape airbus.com
    "thales": "thales_direct",           # ✅ Scrape thales.com
    "loreal": "loreal_direct",           # ✅ Scrape loreal.com
    "bnp_paribas": "bnp_direct",         # ✅ Scrape bnpparibas.com
    
    # Autres entreprises (via JSearch en attendant)
    "sopra_steria": "jsearch",
    "dassault_systemes": "jsearch",
    # ... etc
}
```

**Résultat** :
- ✅ Top 5 entreprises → Scraping DIRECT de leur site
- ✅ Autres 10 entreprises → Via JSearch (temporaire)
- ✅ Migration progressive vers scraping direct

---

## 🔍 Test Concret : Ce que VOUS Verrez

### Avec JSearch (Phase 1)

**Vous sélectionnez** :
- ☑️ Capgemini
- ☑️ L'Oréal

**Vous cherchez** : "Python Developer"

**Résultats** :
```
╔═══════════════════════════════════════════╗
║  15 offres trouvées                       ║
╠═══════════════════════════════════════════╣
║                                           ║
║  📋 Capgemini (9 offres)                  ║
║  ────────────────────────────────────────║
║  • Senior Python Developer                ║
║    📍 Paris · Capgemini                   ║
║    🔗 via LinkedIn                        ║
║                                           ║
║  • Python Backend Engineer                ║
║    📍 Lyon · Capgemini                    ║
║    🔗 via Indeed                          ║
║  ...                                      ║
║                                           ║
║  📋 L'Oréal (6 offres)                    ║
║  ────────────────────────────────────────║
║  • Data Scientist Python                  ║
║    📍 Paris · L'Oréal                     ║
║    🔗 via Glassdoor                       ║
║  ...                                      ║
║                                           ║
║  ⚠️ Offres via agrégateurs (JSearch)     ║
╚═══════════════════════════════════════════╝
```

**Note** : "🔗 via LinkedIn/Indeed" signifie que l'offre vient d'un agrégateur

---

### Avec Scraping Direct (Phase 2)

**Vous sélectionnez** :
- ☑️ Capgemini (scraping direct)
- ☑️ L'Oréal (scraping direct)

**Vous cherchez** : "Python Developer"

**Résultats** :
```
╔═══════════════════════════════════════════╗
║  28 offres trouvées                       ║
╠═══════════════════════════════════════════╣
║                                           ║
║  📋 Capgemini (18 offres)                 ║
║  ────────────────────────────────────────║
║  • Senior Python Developer                ║
║    📍 Paris · Capgemini                   ║
║    🔗 Site officiel Capgemini             ║
║    ⚡ Posté aujourd'hui                   ║
║                                           ║
║  • Python Backend Engineer                ║
║    📍 Lyon · Capgemini                    ║
║    🔗 Site officiel Capgemini             ║
║    ⚡ Posté il y a 2 jours                ║
║  ...                                      ║
║                                           ║
║  📋 L'Oréal (10 offres)                   ║
║  ────────────────────────────────────────║
║  • Data Scientist Python                  ║
║    📍 Paris · L'Oréal                     ║
║    🔗 Site officiel L'Oréal               ║
║    ⚡ Posté aujourd'hui                   ║
║  ...                                      ║
║                                           ║
║  ✅ Offres directes depuis sites carrières║
╚═══════════════════════════════════════════╝
```

**Note** : Plus d'offres (28 vs 15) et plus récentes (aujourd'hui)

---

## ✅ Réponses à Vos Questions

### Q1: "On pourra avoir les offres uniquement pour une entreprise choisie ?"
**R:** ✅ **OUI**, avec les 2 options (JSearch ET scraping direct)

### Q2: "Si je sélectionne 2 entreprises, j'aurais uniquement leurs offres ?"
**R:** ✅ **OUI**, exactement. Seulement les entreprises cochées.

### Q3: "Tu ne vas plus scraper leur site carrière ?"
**R:** ⚠️ **Avec JSearch (court terme)** : Non, on passe par agrégateurs  
     ✅ **Avec scrapers directs (moyen terme)** : Oui, scraping direct du site

---

## 🎯 Décision à Prendre

### Option 1: JSearch MAINTENANT (4-6h)
- ✅ Fonctionne aujourd'hui
- ✅ Filtre par entreprise
- ⚠️ Via agrégateurs

### Option 2: Scraping Direct (3-5 jours)
- ✅ Scraping direct des sites
- ✅ Plus d'offres
- ⚠️ Prend du temps

### Option 3: HYBRIDE (Recommandé)
- Phase 1: JSearch (aujourd'hui)
- Phase 2: Scraping direct (semaine prochaine)
- Meilleur des deux mondes

---

## 🚀 Que Voulez-Vous ?

**A) JSearch maintenant** → Vous avez des offres ce soir ⚡  
**B) Scraping direct** → Vous attendez 5 jours mais c'est parfait 🏗️  
**C) Hybride** → JSearch maintenant + Scraping direct plus tard 🎯  

**Votre choix ?** 🤔
