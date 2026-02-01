"""
Test manuel des tâches Celery
"""
import asyncio
from app.tasks.scraping_tasks import scrape_all_watched_companies, scrape_single_company


def test_celery_import():
    """Test import Celery"""
    try:
        from app.celery_config import celery_app
        print("✅ Celery app importée avec succès")
        print(f"   Broker: {celery_app.conf.broker_url}")
        print(f"   Backend: {celery_app.conf.result_backend}")
        print(f"   Tasks enregistrées: {len(celery_app.tasks)}")
        for task_name in list(celery_app.tasks.keys())[:10]:
            print(f"      - {task_name}")
        return True
    except Exception as e:
        print(f"❌ Erreur import Celery: {e}")
        return False


def test_task_registration():
    """Test enregistrement des tâches"""
    from app.celery_config import celery_app
    
    expected_tasks = [
        'app.tasks.scraping_tasks.scrape_all_watched_companies',
        'app.tasks.scraping_tasks.scrape_all_custom_sources',
        'app.tasks.scraping_tasks.cleanup_old_job_offers',
        'app.tasks.scraping_tasks.scrape_single_company',
    ]
    
    print("\n📋 Vérification enregistrement des tâches:")
    for task_name in expected_tasks:
        if task_name in celery_app.tasks:
            print(f"   ✅ {task_name}")
        else:
            print(f"   ❌ {task_name} NOT FOUND")


def test_beat_schedule():
    """Test configuration Celery Beat"""
    from app.celery_config import celery_app
    
    print("\n⏰ Configuration Celery Beat:")
    for name, config in celery_app.conf.beat_schedule.items():
        print(f"   📅 {name}")
        print(f"      Task: {config['task']}")
        print(f"      Schedule: {config['schedule']}")


def test_manual_task_execution():
    """Test exécution manuelle d'une tâche (sans Celery worker)"""
    print("\n🧪 Test exécution manuelle:")
    try:
        # Test la tâche directement (appel synchrone car la task wrap asyncio.run)
        result = scrape_all_watched_companies()
        print(f"   ✅ Task exécutée manuellement")
        print(f"      Résultat: {result}")
        return True
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Exécute tous les tests"""
    print("=" * 60)
    print("TEST CELERY CONFIGURATION")
    print("=" * 60)
    
    # Test 1: Import
    if not test_celery_import():
        print("\n❌ Tests arrêtés (erreur import)")
        return
    
    # Test 2: Enregistrement tâches
    test_task_registration()
    
    # Test 3: Beat schedule
    test_beat_schedule()
    
    # Test 4: Exécution manuelle
    print("\n⚠️  Test exécution manuelle (peut prendre du temps)...")
    test_manual_task_execution()  # Pas await, c'est sync
    
    print("\n" + "=" * 60)
    print("✅ TESTS TERMINÉS")
    print("=" * 60)


if __name__ == "__main__":
    main()
