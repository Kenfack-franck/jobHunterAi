"""
Script pour générer les embeddings des profils et offres existants
À exécuter après l'ajout de la colonne embedding
"""
import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine
from app.models.profile import Profile
from app.models.job_offer import JobOffer
from app.services.embedding_service import EmbeddingService


async def generate_all_embeddings():
    """Génère les embeddings pour tous les profils et offres existants"""
    
    print("=" * 70)
    print("🔄 GÉNÉRATION DES EMBEDDINGS POUR LES DONNÉES EXISTANTES")
    print("=" * 70)
    
    async with engine.begin() as conn:
        # Pour PostgreSQL avec asyncpg
        from sqlalchemy.ext.asyncio import AsyncSession
        session = AsyncSession(bind=conn, expire_on_commit=False)
        
        # 1. Profils
        print("\n1️⃣ Génération des embeddings pour les profils...")
        result = await session.execute(
            select(Profile).where(Profile.embedding == None)
        )
        profiles = result.scalars().all()
        
        print(f"   Trouvé {len(profiles)} profils sans embedding")
        
        for i, profile in enumerate(profiles, 1):
            try:
                # Charger les relations
                await session.refresh(profile, ['experiences', 'skills'])
                
                # Générer l'embedding
                embedding = EmbeddingService.generate_profile_embedding(profile)
                profile.embedding = embedding
                
                print(f"   ✅ [{i}/{len(profiles)}] Profil {profile.id} - {profile.title}")
            except Exception as e:
                print(f"   ❌ [{i}/{len(profiles)}] Erreur pour profil {profile.id}: {e}")
        
        await session.commit()
        print(f"   ✅ {len(profiles)} profils mis à jour")
        
        # 2. Offres d'emploi
        print("\n2️⃣ Génération des embeddings pour les offres...")
        result = await session.execute(
            select(JobOffer).where(JobOffer.embedding == None)
        )
        job_offers = result.scalars().all()
        
        print(f"   Trouvé {len(job_offers)} offres sans embedding")
        
        for i, job_offer in enumerate(job_offers, 1):
            try:
                # Générer l'embedding
                embedding = EmbeddingService.generate_job_offer_embedding(job_offer)
                job_offer.embedding = embedding
                
                print(f"   ✅ [{i}/{len(job_offers)}] Offre {job_offer.id} - {job_offer.job_title}")
            except Exception as e:
                print(f"   ❌ [{i}/{len(job_offers)}] Erreur pour offre {job_offer.id}: {e}")
        
        await session.commit()
        print(f"   ✅ {len(job_offers)} offres mises à jour")
    
    print("\n" + "=" * 70)
    print("✅ GÉNÉRATION TERMINÉE")
    print("=" * 70)


async def test_similarity_search():
    """Teste la recherche par similarité"""
    
    print("\n" + "=" * 70)
    print("🔍 TEST DE RECHERCHE PAR SIMILARITÉ")
    print("=" * 70)
    
    async with engine.begin() as conn:
        from sqlalchemy.ext.asyncio import AsyncSession
        session = AsyncSession(bind=conn, expire_on_commit=False)
        
        # Récupérer un profil
        result = await session.execute(
            select(Profile).where(Profile.embedding != None).limit(1)
        )
        profile = result.scalar_one_or_none()
        
        if not profile:
            print("❌ Aucun profil avec embedding trouvé")
            return
        
        print(f"\n📋 Profil: {profile.title}")
        
        # Rechercher les offres les plus compatibles
        from sqlalchemy import func
        
        # Calcul de la similarité (1 - distance cosinus)
        similarity = (1 - JobOffer.embedding.cosine_distance(profile.embedding)).label('similarity')
        
        query = (
            select(JobOffer, similarity)
            .where(JobOffer.embedding != None)
            .order_by(similarity.desc())
            .limit(5)
        )
        
        result = await session.execute(query)
        matches = result.all()
        
        print(f"\n🎯 Top 5 offres compatibles:\n")
        for job_offer, sim in matches:
            score = sim * 100
            print(f"   {'🟢' if score >= 70 else '🟡' if score >= 50 else '🔴'} {score:.1f}% - {job_offer.job_title} @ {job_offer.company_name}")
    
    print("\n" + "=" * 70)
    print("✅ TEST TERMINÉ")
    print("=" * 70)


if __name__ == "__main__":
    print("\n🚀 Démarrage...\n")
    
    # Générer les embeddings
    asyncio.run(generate_all_embeddings())
    
    # Tester la recherche
    asyncio.run(test_similarity_search())
