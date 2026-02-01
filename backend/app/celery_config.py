"""
Configuration Celery pour Job Hunter AI

Celery est utilisé pour :
- Scraping périodique des entreprises surveillées
- Scraping des sources custom
- Génération asynchrone de documents
"""
from celery import Celery
from celery.schedules import crontab
from app.config import settings

# Créer l'application Celery
celery_app = Celery(
    "jobhunter",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        'app.tasks.scraping_tasks',
    ]
)

# Configuration Celery
celery_app.conf.update(
    # Timezone
    timezone='Europe/Paris',
    enable_utc=True,
    
    # Sérialisation
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    
    # Résultats
    result_expires=3600,  # 1 heure
    result_backend_transport_options={'master_name': 'mymaster'},
    
    # Worker
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    
    # Task routing
    task_routes={
        'app.tasks.scraping_tasks.*': {'queue': 'scraping'},
        'app.tasks.generation_tasks.*': {'queue': 'generation'},
    },
    
    # Retry policy
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)

# Configuration Celery Beat (tâches périodiques)
celery_app.conf.beat_schedule = {
    # Scraping des entreprises surveillées toutes les 4 heures
    'scrape-watched-companies': {
        'task': 'app.tasks.scraping_tasks.scrape_all_watched_companies',
        'schedule': crontab(minute=0, hour='*/4'),  # Toutes les 4h
        'options': {'queue': 'scraping'}
    },
    
    # Scraping des sources custom toutes les 4 heures (décalé de 30 min)
    'scrape-custom-sources': {
        'task': 'app.tasks.scraping_tasks.scrape_all_custom_sources',
        'schedule': crontab(minute=30, hour='*/4'),  # Toutes les 4h à :30
        'options': {'queue': 'scraping'}
    },
    
    # Nettoyage des vieilles offres (tous les jours à 3h du matin)
    'cleanup-old-offers': {
        'task': 'app.tasks.scraping_tasks.cleanup_old_job_offers',
        'schedule': crontab(minute=0, hour=3),  # Tous les jours à 3h
        'options': {'queue': 'scraping'}
    },
}

# Logging
celery_app.conf.update(
    worker_hijack_root_logger=False,
    worker_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    worker_task_log_format='[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s',
)
