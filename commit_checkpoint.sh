#!/bin/bash
# Script pour commit toutes les modifications du checkpoint

echo "🔖 Création du checkpoint - Fix Build Production Frontend"
echo ""

# Vérifier les modifications
echo "📝 Fichiers modifiés:"
git status --short

echo ""
echo "📊 Statistiques:"
git diff --stat

echo ""
read -p "Voulez-vous commiter ces modifications? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]
then
    # Ajouter tous les fichiers modifiés
    git add frontend/src/app/documents/page.tsx
    git add frontend/src/types/index.ts
    git add frontend/src/app/jobs/\[id\]/page.tsx
    git add frontend/src/components/jobs/AnalysisModal.tsx
    git add frontend/src/components/documents/DocumentGenerator.tsx
    git add frontend/src/components/layout/Navbar.tsx
    git add frontend/src/contexts/AuthContext.tsx
    git add frontend/src/lib/documentsService.ts
    git add frontend/public/.gitkeep
    git add CHECKPOINT_FIX_BUILD_PROD_2026-02-01.md

    # Commit avec message détaillé
    git commit -m "fix(frontend): Correction erreurs TypeScript build production

✅ Build Docker réussi - 11 erreurs corrigées

Modifications:
- app/documents/page.tsx: docId number → string
- types/index.ts: Ajout work_mode, fix User.full_name
- app/jobs/[id]/page.tsx: Fix salary, requirements, keywords
- components/jobs/AnalysisModal.tsx: companyName optionnel
- components/documents/DocumentGenerator.tsx: Ajout token auth
- components/layout/Navbar.tsx: size icon → sm
- contexts/AuthContext.tsx: User.full_name avec null
- lib/documentsService.ts: Retrait filename dupliqué
- public/: Création dossier manquant

Résultat:
✓ Compiled successfully
✓ 16 pages générées
✓ Image Docker créée: jobhunter-frontend:success

Refs: CHECKPOINT_FIX_BUILD_PROD_2026-02-01.md"

    echo ""
    echo "✅ Commit créé avec succès!"
    echo ""
    echo "Pour pusher sur GitLab:"
    echo "  git push origin main"
    echo ""
    echo "Cela déclenchera le pipeline CI/CD automatiquement."
else
    echo "❌ Commit annulé"
fi
