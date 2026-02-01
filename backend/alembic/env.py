"""
Configuration Alembic pour les migrations
"""
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
import asyncio
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour importer app
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import Base
from app.config import settings
from app.models import *  # Importer tous les modèles

# Configuration Alembic
config = context.config

# Interpréter le fichier de config pour le logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Métadonnées des modèles
target_metadata = Base.metadata

# Récupérer l'URL de la base de données depuis les settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


def run_migrations_offline() -> None:
    """
    Migrations en mode 'offline'
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Exécuter les migrations"""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Migrations en mode 'online' (async)
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
