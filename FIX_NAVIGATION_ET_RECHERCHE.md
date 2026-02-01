# 🔧 FIX: Navigation et Scénario de Recherche

## 🐛 Problèmes Identifiés

### 1. Route Incorrecte dans le Sidebar ❌

**Problème**: Le lien "Recherche" dans le sidebar pointe vers `/jobs/search` qui **n'existe pas**.

**Fichier**: `frontend/src/components/layout/Sidebar.tsx` ligne 10
```tsx
{ href: '/jobs/search', label: 'Recherche', icon: Search },
```

**La vraie route**: `/jobs`

**Impact**: 
- Quand vous cliquez sur "Recherche" dans le menu, vous arrivez sur une page vide (404)
- Next.js crée une page vide au lieu de montrer une erreur

---

### 2. Page d'Accueil vs Dashboard 🏠

**Problème**: Confusion entre landing page et dashboard.

**Actuellement**:
- `/` (localhost:3000) → Landing page marketing (pour visiteurs non connectés)
- `/dashboard` → Dashboard authentifié

**Le bug**: Quand vous êtes connecté et que vous allez sur `/`, vous voyez la landing page DANS le layout authentifié (avec sidebar).

**Cause**: `AppShell.tsx` affiche le layout authentifié partout si `isAuthenticated = true`.

---

### 3. Scénario de Recherche Non Implémenté ⚠️

**Scénario demandé**:
1. Frontend envoie requête → Backend reçoit
2. Backend dit "J'ai reçu, je commence"  
3. Frontend affiche spinner
4. Backend traite (scraping)
5. Backend signale "offres trouvées, traitement en cours"
6. Backend envoie résultats
7. Frontend affiche les offres

**Ce qui est actuellement implémenté**:
1. Frontend envoie requête
2. Frontend affiche "Recherche en cours..." (spinner bleu)
3. Backend fait la recherche **synchrone** (attend la fin)
4. Backend renvoie les résultats
5. Frontend affiche "X offres trouvées" (message vert)

**Architecture async existe mais Celery ne fonctionne pas** (worker crash).

---

## 🛠️ Corrections

### Correction 1: Fixer le lien Sidebar

**Fichier**: `frontend/src/components/layout/Sidebar.tsx`

**AVANT** (ligne 10):
```tsx
{ href: '/jobs/search', label: 'Recherche', icon: Search },
```

**APRÈS**:
```tsx
{ href: '/jobs', label: 'Recherche', icon: Search },
```

---

### Correction 2: Redirection de la Page d'Accueil

**Fichier**: `frontend/src/app/page.tsx`

**Ajouter une redirection automatique si connecté**:

```tsx
"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/lib/auth";
import Link from 'next/link';
// ... (imports existants)

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // Rediriger vers dashboard si déjà connecté
    if (authService.isAuthenticated()) {
      router.push("/dashboard");
    }
  }, [router]);

  // ... (reste du code)
}
```

---

### Correction 3: Améliorer le Feedback de Recherche

**Problème**: Le code actuel montre juste un spinner, mais pas de détails de progression.

**Solution temporaire (sans Celery)**:

**Fichier**: `frontend/src/app/jobs/page.tsx`

Modifier `loadJobs()` pour donner plus de feedback:

```tsx
const loadJobs = async (params: JobOfferSearchParams = {}) => {
  setLoading(true);
  setSearchStatus("searching");
  setSearchMessage("🔄 Recherche en cours... Le backend traite votre demande.");
  
  try {
    // Appel API
    const data = await jobOfferService.searchJobOffers(params);
    
    // Feedback intermédiaire
    setSearchMessage(`✅ Backend a trouvé ${data.length} offre(s). Affichage en cours...`);
    
    // Petite pause pour que l'utilisateur voie le message
    await new Promise(resolve => setTimeout(resolve, 500));
    
    setJobs(data);
    setSearchParams(params);
    
    if (data.length === 0) {
      setSearchStatus("idle");
      setSearchMessage("Aucune offre trouvée. Essayez d'autres mots-clés.");
    } else {
      setSearchStatus("success");
      setSearchMessage(`${data.length} offre(s) trouvée(s) et affichée(s) !`);
      // Clear après 3s
      setTimeout(() => {
        setSearchStatus("idle");
        setSearchMessage("");
      }, 3000);
    }
  } catch (error: any) {
    console.error("Erreur:", error);
    setSearchStatus("error");
    
    // Messages d'erreur plus descriptifs
    if (error.response?.status === 401) {
      setSearchMessage("❌ Session expirée. Reconnectez-vous.");
    } else if (error.response?.status === 404) {
      setSearchMessage("❌ Endpoint introuvable. Vérifiez que le backend est démarré.");
    } else {
      setSearchMessage(error.response?.data?.detail || "❌ Erreur lors de la recherche.");
    }
  } finally {
    setLoading(false);
  }
};
```

---

## 📝 Plan d'Implémentation Complète (Futur)

Pour implémenter le vrai scénario async avec Celery:

### Phase 1: Fixer Celery Worker
```bash
# Ajouter pgvector à requirements.txt
echo "pgvector==0.2.4" >> backend/requirements.txt

# Rebuild
docker-compose down
docker-compose up -d --build
```

### Phase 2: Utiliser l'API Async

**Frontend** (`jobs/page.tsx`):
```tsx
const loadJobs = async (params: JobOfferSearchParams = {}) => {
  setLoading(true);
  setSearchStatus("searching");
  setSearchMessage("🔄 Lancement de la recherche...");
  
  try {
    // 1. Lancer la recherche async
    const { task_id } = await jobOfferService.searchJobsAsync(params);
    setSearchMessage(`✅ Backend a reçu la demande (ID: ${task_id}). Scraping en cours...`);
    
    // 2. Polling toutes les 2 secondes
    const interval = setInterval(async () => {
      const status = await jobOfferService.getSearchStatus(task_id);
      
      if (status.state === "PENDING") {
        setSearchMessage("⏳ En attente de traitement...");
      } else if (status.state === "STARTED") {
        setSearchMessage(`🔍 Scraping en cours... ${status.found_count || 0} offres trouvées`);
      } else if (status.state === "SUCCESS") {
        clearInterval(interval);
        setJobs(status.result);
        setSearchStatus("success");
        setSearchMessage(`✅ ${status.result.length} offres trouvées !`);
        setLoading(false);
      } else if (status.state === "FAILURE") {
        clearInterval(interval);
        setSearchStatus("error");
        setSearchMessage(`❌ Erreur: ${status.error}`);
        setLoading(false);
      }
    }, 2000);
    
    // Timeout après 2 minutes
    setTimeout(() => {
      clearInterval(interval);
      if (loading) {
        setSearchStatus("error");
        setSearchMessage("⏱️ Timeout: la recherche prend trop de temps");
        setLoading(false);
      }
    }, 120000);
    
  } catch (error: any) {
    console.error("Erreur:", error);
    setSearchStatus("error");
    setSearchMessage("❌ Impossible de lancer la recherche");
    setLoading(false);
  }
};
```

---

## ✅ Actions Immédiates

### 1. Corriger le Sidebar (URGENT)

```bash
# Ouvrir le fichier
nano frontend/src/components/layout/Sidebar.tsx

# Ligne 10: Changer
# { href: '/jobs/search', ... }
# en
# { href: '/jobs', ... }
```

### 2. Ajouter Redirection sur Page d'Accueil (IMPORTANT)

```bash
# Ouvrir le fichier
nano frontend/src/app/page.tsx

# Ajouter "use client" en haut
# Ajouter useEffect pour rediriger si authentifié
```

### 3. Tester

```
1. Effacer cache navigateur (Ctrl+Shift+R)
2. Se connecter
3. Cliquer sur "Recherche" dans le sidebar
4. Vérifier: vous arrivez sur /jobs avec le formulaire de recherche
5. Chercher "Python + Paris"
6. Vérifier: messages de progression s'affichent
7. Vérifier: offres s'affichent
```

---

## 🎯 Résumé

| Problème | Cause | Solution | Priorité |
|----------|-------|----------|----------|
| Lien "Recherche" va vers `/jobs/search` | Sidebar ligne 10 | Changer en `/jobs` | 🔴 URGENT |
| Landing page dans layout auth | Pas de redirection | Ajouter useEffect | 🟡 Important |
| Pas de feedback détaillé | Messages trop simples | Améliorer messages | 🟢 Nice-to-have |
| Async search non fonctionnel | Celery worker crash | Fixer pgvector | 🔵 Futur |

---

**Date**: 2026-01-31
**Fichiers à modifier**: 
- `frontend/src/components/layout/Sidebar.tsx` (ligne 10)
- `frontend/src/app/page.tsx` (ajouter redirection)
- `frontend/src/app/jobs/page.tsx` (améliorer messages - optionnel)
