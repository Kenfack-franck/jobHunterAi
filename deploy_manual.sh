#!/bin/bash
set -e

echo "🚀 Déploiement manuel sur VPS..."

# Variables
SSH_USER="ubuntu"
SSH_HOST="vps-c7c7eb59"
DEPLOY_DIR="~/jobhunter"

echo "📦 Envoi des fichiers..."
rsync -avz --exclude 'node_modules' --exclude '.git' --exclude '__pycache__' \
  ./ ${SSH_USER}@${SSH_HOST}:${DEPLOY_DIR}/

echo "🔨 Build et redémarrage sur le VPS..."
ssh ${SSH_USER}@${SSH_HOST} << 'EOF'
cd ~/jobhunter

echo "🛑 Arrêt des services..."
docker compose -f docker-compose.prod.yml down

echo "🔨 Build backend..."
docker compose -f docker-compose.prod.yml build backend

echo "🔨 Build frontend..."
docker compose -f docker-compose.prod.yml build frontend

echo "🚀 Démarrage des services..."
docker compose -f docker-compose.prod.yml up -d

echo "✅ Déploiement terminé !"
docker compose -f docker-compose.prod.yml ps
EOF

echo ""
echo "✅ Déploiement réussi !"
echo "📊 Logs backend : ssh ${SSH_USER}@${SSH_HOST} 'cd ~/jobhunter && docker compose -f docker-compose.prod.yml logs -f backend'"
