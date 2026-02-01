-- Initialisation de la base de données Job Hunter AI
-- Créé automatiquement au premier démarrage de PostgreSQL

-- Activer l'extension pgvector (pour V2.0)
CREATE EXTENSION IF NOT EXISTS vector;

-- Créer l'extension pour UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Message de confirmation
DO $$
BEGIN
    RAISE NOTICE 'Base de données Job Hunter AI initialisée avec succès';
END $$;
