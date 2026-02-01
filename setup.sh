#!/bin/bash
# Script d'installation et de démarrage - Job Hunter AI

set -e

echo "🚀 Job Hunter AI - Installation et Démarrage"
echo "============================================="
echo ""

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Déterminer la commande Docker Compose à utiliser
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Vérifier que le fichier .env existe
if [ ! -f .env ]; then
    echo "❌ Fichier .env manquant. Copie de .env.example..."
    cp .env.example .env
    echo "⚠️  ATTENTION: Veuillez éditer le fichier .env et remplir:"
    echo "   - OPENAI_API_KEY (obligatoire pour la génération de LM)"
    echo "   - SECRET_KEY (peut être généré avec: openssl rand -hex 32)"
    echo ""
    read -p "Appuyez sur Entrée une fois le fichier .env configuré..."
fi

echo "📦 Construction des images Docker..."
$COMPOSE_CMD build

echo ""
echo "🗄️  Démarrage des services..."
$COMPOSE_CMD up -d postgres redis

echo "⏳ Attente du démarrage de PostgreSQL (15 secondes)..."
sleep 15

echo ""
echo "🔧 Exécution des migrations de base de données..."
$COMPOSE_CMD run --rm backend alembic upgrade head

echo ""
echo "🚀 Démarrage de tous les services..."
$COMPOSE_CMD up -d

echo ""
echo "✅ Installation terminée avec succès!"
echo ""
echo "📍 Services disponibles:"
echo "   - Frontend:        http://localhost:3000"
echo "   - Backend API:     http://localhost:8000"
echo "   - Documentation:   http://localhost:8000/docs"
echo "   - PostgreSQL:      localhost:5432"
echo "   - Redis:           localhost:6379"
echo ""
echo "📊 Voir les logs:"
echo "   docker compose logs -f"
echo ""
echo "🛑 Arrêter les services:"
echo "   docker compose down"
echo ""
