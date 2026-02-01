#!/bin/bash
# Script d'installation infrastructure VPS pour Job Hunter AI
# À exécuter UNE SEULE FOIS sur le VPS

set -e  # Arrêter si erreur

echo "🚀 Installation Infrastructure Job Hunter AI..."

# 1. Mise à jour système
echo "📦 Mise à jour du système..."
sudo apt update && sudo apt upgrade -y

# 2. Installation Docker (si pas déjà fait)
if ! command -v docker &> /dev/null; then
    echo "🐳 Installation Docker..."
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker ubuntu
    echo "✅ Docker installé. Reconnectez-vous pour appliquer les permissions."
fi

# 3. Installation Docker Compose (si pas déjà fait)
if ! command -v docker compose &> /dev/null; then
    echo "🐳 Installation Docker Compose..."
    sudo apt install docker-compose-plugin -y
fi

# 4. Création du réseau Docker global (si pas déjà fait)
if ! docker network inspect web_net &> /dev/null; then
    echo "🌐 Création réseau Docker 'web_net'..."
    docker network create web_net
else
    echo "✅ Réseau 'web_net' existe déjà"
fi

# 5. Création des dossiers de travail
echo "📁 Création dossiers de travail..."
mkdir -p ~/jobhunter
mkdir -p ~/jobhunter/data/postgres
mkdir -p ~/jobhunter/data/redis
mkdir -p ~/proxy

# 6. Configuration Firewall (ports 80/443 uniquement)
echo "🔒 Configuration Firewall..."
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw --force enable

echo ""
echo "✅ Infrastructure installée !"
echo ""
echo "Prochaines étapes :"
echo "1. Configurez Caddy (voir étape 2)"
echo "2. Ajoutez les secrets GitLab (voir étape 3)"
echo "3. Lancez le déploiement (voir étape 4)"
