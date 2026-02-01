FROM node:20-alpine

# Répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY package.json package-lock.json* ./

# Installer les dépendances
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

# Copier le reste du code
COPY . .

# Exposer le port
EXPOSE 3000

# Commande par défaut (dev mode)
CMD ["npm", "run", "dev"]
