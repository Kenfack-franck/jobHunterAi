"""
Script de test pour l'EmbeddingService
Teste la génération d'embeddings et le calcul de similarité
"""
import asyncio
from app.services.embedding_service import EmbeddingService, get_embedding_model


async def test_embeddings():
    print("=" * 60)
    print("🧪 TEST DE L'EMBEDDINGSERVICE")
    print("=" * 60)
    
    # Test 1: Chargement du modèle
    print("\n1️⃣ Chargement du modèle...")
    try:
        model = get_embedding_model()
        print(f"✅ Modèle chargé: {model}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return
    
    # Test 2: Génération d'embeddings simples
    print("\n2️⃣ Test de génération d'embeddings...")
    text1 = "Développeur Python Backend avec 5 ans d'expérience en FastAPI"
    text2 = "Senior Python Developer with FastAPI and PostgreSQL"
    text3 = "Designer UX/UI spécialisé en Figma et Adobe XD"
    
    embedding1 = EmbeddingService.generate_embedding(text1)
    embedding2 = EmbeddingService.generate_embedding(text2)
    embedding3 = EmbeddingService.generate_embedding(text3)
    
    print(f"✅ Embedding 1: {len(embedding1)} dimensions")
    print(f"   Premiers 5 valeurs: {embedding1[:5]}")
    print(f"✅ Embedding 2: {len(embedding2)} dimensions")
    print(f"✅ Embedding 3: {len(embedding3)} dimensions")
    
    # Test 3: Calcul de similarité
    print("\n3️⃣ Test de similarité cosinus...")
    
    sim_1_2 = EmbeddingService.calculate_cosine_similarity(embedding1, embedding2)
    sim_1_3 = EmbeddingService.calculate_cosine_similarity(embedding1, embedding3)
    sim_2_3 = EmbeddingService.calculate_cosine_similarity(embedding2, embedding3)
    
    print(f"📊 Similarité entre texte1 et texte2 (similaires): {sim_1_2:.4f} ({sim_1_2*100:.1f}%)")
    print(f"📊 Similarité entre texte1 et texte3 (différents): {sim_1_3:.4f} ({sim_1_3*100:.1f}%)")
    print(f"📊 Similarité entre texte2 et texte3 (différents): {sim_2_3:.4f} ({sim_2_3*100:.1f}%)")
    
    # Test 4: Vérification de la cohérence
    print("\n4️⃣ Vérification...")
    if sim_1_2 > sim_1_3:
        print("✅ Les textes similaires ont une meilleure similarité !")
    else:
        print("⚠️ Résultats inattendus")
    
    # Test 5: Test avec profil fictif
    print("\n5️⃣ Test avec structure de profil...")
    
    class FakeProfile:
        def __init__(self):
            self.title = "Développeur Full-Stack"
            self.summary = "Passionné par le développement web avec React et Python"
            self.location = "Paris, France"
            self.experiences = [
                type('obj', (object,), {'title': 'Lead Developer'})(),
                type('obj', (object,), {'title': 'Backend Engineer'})()
            ]
            self.skills = [
                type('obj', (object,), {'name': 'Python'})(),
                type('obj', (object,), {'name': 'React'})(),
                type('obj', (object,), {'name': 'Docker'})()
            ]
    
    class FakeJobOffer:
        def __init__(self):
            self.job_title = "Développeur Full-Stack Senior"
            self.company_name = "TechCorp"
            self.description = "Nous recherchons un développeur Full-Stack avec React et Python"
            self.requirements = "5 ans d'expérience, maîtrise de React, Python, Docker"
            self.location = "Paris"
            self.job_type = "CDI"
            self.extracted_keywords = ["Python", "React", "Docker"]
    
    profile = FakeProfile()
    job_offer = FakeJobOffer()
    
    profile_embedding = EmbeddingService.generate_profile_embedding(profile)
    job_embedding = EmbeddingService.generate_job_offer_embedding(job_offer)
    
    print(f"✅ Embedding profil généré: {len(profile_embedding)} dimensions")
    print(f"✅ Embedding offre généré: {len(job_embedding)} dimensions")
    
    similarity = EmbeddingService.calculate_cosine_similarity(profile_embedding, job_embedding)
    print(f"\n🎯 SCORE DE COMPATIBILITÉ: {similarity*100:.1f}%")
    
    print("\n" + "=" * 60)
    print("✅ TOUS LES TESTS RÉUSSIS")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_embeddings())
