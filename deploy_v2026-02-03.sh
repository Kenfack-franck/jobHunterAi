#!/bin/bash
# 🚀 Script de Déploiement Rapide - Version 2026-02-03
# Responsive Design + Settings Fixes + New Endpoints

set -e  # Stop on error

echo "🎯 Déploiement Job Hunter AI - Version 2026-02-03"
echo "=================================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Vérifier qu'on est sur main
echo -e "${YELLOW}[1/7] Vérification de la branche...${NC}"
BRANCH=$(git branch --show-current)
if [ "$BRANCH" != "main" ]; then
    echo -e "${RED}❌ Vous devez être sur la branche 'main'${NC}"
    echo "Commande: git checkout main"
    exit 1
fi
echo -e "${GREEN}✅ Sur la branche main${NC}"
echo ""

# 2. Vérifier qu'il n'y a pas de changements non commités
echo -e "${YELLOW}[2/7] Vérification des changements non commités...${NC}"
if [[ -n $(git status -s) ]]; then
    echo -e "${RED}❌ Vous avez des changements non commités${NC}"
    echo "Commandez: git status"
    echo "Puis: git add . && git commit -m 'votre message'"
    exit 1
fi
echo -e "${GREEN}✅ Aucun changement non commité${NC}"
echo ""

# 3. Pousser sur GitLab
echo -e "${YELLOW}[3/7] Push vers GitLab...${NC}"
read -p "Voulez-vous pousser sur GitLab maintenant ? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push gitlab main
    echo -e "${GREEN}✅ Code poussé sur GitLab${NC}"
else
    echo -e "${YELLOW}⚠️  Push annulé - vous devrez le faire manuellement${NC}"
fi
echo ""

# 4. Attendre que le pipeline se termine
echo -e "${YELLOW}[4/7] Pipeline GitLab...${NC}"
echo "🔗 Ouvrez: https://gitlab.com/VOTRE_USERNAME/job-hunter-ai/-/pipelines"
echo ""
echo "⏱️  Le pipeline prend environ 8-12 minutes"
echo "   - Build Frontend (2-3 min)"
echo "   - Build Backend (2-3 min)"
echo "   - Deploy Frontend (1-2 min)"
echo "   - Deploy Backend (1-2 min)"
echo ""
read -p "Appuyez sur Entrée quand le pipeline est ✅ SUCCESS..." 
echo -e "${GREEN}✅ Pipeline terminé${NC}"
echo ""

# 5. Migrations DB
echo -e "${YELLOW}[5/7] Migrations de la base de données...${NC}"
echo "📡 Connexion au VPS..."
SSH_COMMAND="ssh ubuntu@152.228.128.95"

echo "Exécution des migrations..."
$SSH_COMMAND << 'EOF'
cd ~/jobhunter
docker compose -f docker-compose.prod.yml exec -T backend alembic upgrade head
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Migrations appliquées${NC}"
else
    echo -e "${RED}❌ Erreur lors des migrations${NC}"
    exit 1
fi
echo ""

# 6. Vérifier les conteneurs
echo -e "${YELLOW}[6/7] Vérification des conteneurs...${NC}"
$SSH_COMMAND << 'EOF'
cd ~/jobhunter
echo "État des conteneurs:"
docker compose -f docker-compose.prod.yml ps
EOF
echo -e "${GREEN}✅ Conteneurs vérifiés${NC}"
echo ""

# 7. Tests de santé
echo -e "${YELLOW}[7/7] Tests de santé...${NC}"

# Test Backend
echo -n "Backend API... "
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://api.jobhunter.franckkenfack.works/health)
if [ "$BACKEND_STATUS" = "200" ]; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ ERREUR (HTTP $BACKEND_STATUS)${NC}"
fi

# Test Frontend
echo -n "Frontend... "
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://jobhunter.franckkenfack.works)
if [ "$FRONTEND_STATUS" = "200" ]; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ ERREUR (HTTP $FRONTEND_STATUS)${NC}"
fi

echo ""
echo "=================================================="
echo -e "${GREEN}🎉 DÉPLOIEMENT TERMINÉ !${NC}"
echo "=================================================="
echo ""
echo "🌐 Accès:"
echo "   Frontend: https://jobhunter.franckkenfack.works"
echo "   Backend:  https://api.jobhunter.franckkenfack.works/docs"
echo ""
echo "📋 Tests à faire manuellement:"
echo "   - [ ] Responsive design (mobile/tablet/desktop)"
echo "   - [ ] Sidebar fixe (ne bouge pas entre pages)"
echo "   - [ ] Footer défile avec le contenu"
echo "   - [ ] Settings → Modifier nom → Enregistrer → Recharger ✅"
echo "   - [ ] Settings → Changer mot de passe ✅"
echo "   - [ ] Sources page (/settings/sources)"
echo "   - [ ] Menu hamburger mobile"
echo "   - [ ] Feedback button (bas droite)"
echo ""
echo "📊 Commandes utiles:"
echo "   Logs:     ssh ubuntu@152.228.128.95 'cd ~/jobhunter && docker compose -f docker-compose.prod.yml logs -f'"
echo "   Restart:  ssh ubuntu@152.228.128.95 'cd ~/jobhunter && docker compose -f docker-compose.prod.yml restart'"
echo ""
echo "✅ Guide complet: DEPLOY_SESSION_2026-02-03.md"
