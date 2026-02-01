"""
Script de création d'utilisateur de test complet
"""
import asyncio
import sys
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

sys.path.insert(0, '/app')

from app.models import User, Profile, Experience, Education, Skill, JobOffer

DATABASE_URL = "postgresql+asyncpg://jobhunter:jobhunter_secure_password_2024@postgres:5432/jobhunter_db"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

TEST_USER = {
    "email": "john.doe@testmail.com",
    "password": "Test2026!",
    "full_name": "John Doe"
}

async def create_test_data():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            # 1. Créer utilisateur
            print("📝 Création de l'utilisateur...")
            user = User(
                email=TEST_USER["email"],
                hashed_password=pwd_context.hash(TEST_USER["password"]),
                full_name=TEST_USER["full_name"],
                language="fr",
                is_active=True
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            print(f"✅ Utilisateur créé : {user.email} (ID: {user.id})")
            
            # 2. Créer profil
            print("\n👤 Création du profil...")
            profile = Profile(
                user_id=user.id,
                title="Senior Full Stack Developer",
                summary="Développeur passionné avec 5 ans d'expérience en Python/React. Expert en architecture microservices et IA générative. Recherche opportunités remote en CDI.",
                location="Paris, France",
                phone="+33 6 12 34 56 78",
                linkedin_url="https://linkedin.com/in/johndoe",
                github_url="https://github.com/johndoe",
                portfolio_url="https://johndoe.dev"
            )
            session.add(profile)
            await session.commit()
            await session.refresh(profile)
            print(f"✅ Profil créé (ID: {profile.id})")
            
            # 3. Expériences
            print("\n💼 Ajout des expériences...")
            experiences = [
                Experience(
                    profile_id=profile.id,
                    title="Senior Full Stack Developer",
                    company="TechCorp France",
                    location="Paris, France",
                    start_date=datetime(2021, 3, 1).date(),
                    current=True,
                    description="• Développement plateforme SaaS (Next.js + FastAPI)\n• Architecture microservices (Docker/Kubernetes)\n• Intégration IA (GPT-4, Claude)\n• Lead technique équipe 4 devs\n• -60% temps chargement"
                ),
                Experience(
                    profile_id=profile.id,
                    title="Full Stack Developer",
                    company="StartupLab",
                    location="Lyon, France",
                    start_date=datetime(2019, 6, 1).date(),
                    end_date=datetime(2021, 2, 28).date(),
                    current=False,
                    description="• MVP e-commerce (React + Django)\n• Intégration Stripe\n• CI/CD GitHub Actions\n• Tests (Jest, Pytest)"
                ),
                Experience(
                    profile_id=profile.id,
                    title="Junior Developer",
                    company="WebAgency Pro",
                    location="Marseille, France",
                    start_date=datetime(2018, 9, 1).date(),
                    end_date=datetime(2019, 5, 31).date(),
                    current=False,
                    description="• Sites WordPress\n• APIs REST\n• Support clients"
                )
            ]
            for exp in experiences:
                session.add(exp)
            await session.commit()
            print(f"✅ {len(experiences)} expériences ajoutées")
            
            # 4. Formations
            print("\n🎓 Ajout des formations...")
            educations = [
                Education(
                    profile_id=profile.id,
                    degree="Master Informatique",
                    field_of_study="Intelligence Artificielle et Data Science",
                    institution="Université Paris-Saclay",
                    location="Paris, France",
                    start_date=datetime(2016, 9, 1).date(),
                    end_date=datetime(2018, 6, 30).date(),
                    description="Spécialisation ML, Deep Learning, NLP"
                ),
                Education(
                    profile_id=profile.id,
                    degree="Licence Informatique",
                    field_of_study="Développement Logiciel",
                    institution="Université Lyon 1",
                    location="Lyon, France",
                    start_date=datetime(2013, 9, 1).date(),
                    end_date=datetime(2016, 6, 30).date()
                )
            ]
            for edu in educations:
                session.add(edu)
            await session.commit()
            print(f"✅ {len(educations)} formations ajoutées")
            
            # 5. Compétences
            print("\n🛠️ Ajout des compétences...")
            skills_data = [
                ("Python", "expert", "backend"),
                ("FastAPI", "expert", "backend"),
                ("Django", "advanced", "backend"),
                ("Node.js", "advanced", "backend"),
                ("PostgreSQL", "advanced", "database"),
                ("Redis", "intermediate", "database"),
                ("React", "expert", "frontend"),
                ("Next.js", "expert", "frontend"),
                ("TypeScript", "expert", "frontend"),
                ("TailwindCSS", "advanced", "frontend"),
                ("Docker", "advanced", "devops"),
                ("Kubernetes", "intermediate", "devops"),
                ("CI/CD", "advanced", "devops"),
                ("AWS", "intermediate", "cloud"),
                ("OpenAI API", "advanced", "ai"),
                ("Langchain", "intermediate", "ai"),
                ("Machine Learning", "intermediate", "ai"),
                ("Git", "expert", "tools"),
                ("Agile/Scrum", "advanced", "methodology"),
            ]
            for skill_name, level, category in skills_data:
                skill = Skill(
                    profile_id=profile.id,
                    name=skill_name,
                    level=level,
                    category=category
                )
                session.add(skill)
            await session.commit()
            print(f"✅ {len(skills_data)} compétences ajoutées")
            
            # 6. Offres d'emploi
            print("\n📋 Ajout d'offres d'emploi...")
            job_offers = [
                JobOffer(
                    user_id=user.id,
                    job_title="Senior Full Stack Developer",
                    company_name="Google France",
                    location="Paris, France",
                    job_type="CDI",
                    work_mode="Remote",
                    description="Rejoignez Google Cloud pour développer des solutions innovantes.\n\nMissions:\n- Développement features Cloud Console\n- Architecture microservices\n- Mentorat équipe\n\nStack: React, TypeScript, Go, Kubernetes",
                    source_platform="LinkedIn",
                    source_url="https://linkedin.com/jobs/google-senior-fullstack",
                ),
                JobOffer(
                    user_id=user.id,
                    job_title="Lead Developer Python",
                    company_name="Datadog",
                    location="Paris, France",
                    job_type="CDI",
                    work_mode="Hybrid",
                    description="Lead Developer pour notre équipe monitoring.\n\nResponsabilités:\n- Architecture systèmes distribués\n- Développement agents monitoring\n- Performance optimization\n\nStack: Python, Go, PostgreSQL, Kafka",
                    source_platform="Welcome to the Jungle",
                    source_url="https://wttj.com/datadog-lead-python",
                ),
                JobOffer(
                    user_id=user.id,
                    job_title="Full Stack Engineer (Remote)",
                    company_name="Stripe",
                    location="Remote Europe",
                    job_type="CDI",
                    work_mode="Remote",
                    description="Build the financial infrastructure of the internet.\n\nWhat you'll do:\n- Develop payment APIs\n- Build developer tools\n- Scale global infrastructure\n\nStack: Ruby, React, TypeScript, PostgreSQL",
                    source_platform="Stripe Careers",
                    source_url="https://stripe.com/jobs/fullstack-remote",
                ),
                JobOffer(
                    user_id=user.id,
                    job_title="Senior Backend Developer",
                    company_name="OVHcloud",
                    location="Roubaix, France",
                    job_type="CDI",
                    work_mode="Hybrid",
                    description="Développez l'infrastructure cloud européenne.\n\nMissions:\n- APIs microservices\n- Infrastructure as Code\n- Performance & scalabilité\n\nStack: Python, FastAPI, Kubernetes, Terraform",
                    source_platform="OVHcloud Careers",
                    source_url="https://ovhcloud.com/careers/backend-senior",
                ),
                JobOffer(
                    user_id=user.id,
                    job_title="AI/ML Engineer",
                    company_name="Hugging Face",
                    location="Paris, France",
                    job_type="CDI",
                    work_mode="Remote",
                    description="Join the AI community hub!\n\nWhat you'll build:\n- ML model optimization\n- Inference APIs\n- Developer tools\n\nStack: Python, PyTorch, FastAPI, Kubernetes",
                    source_platform="Hugging Face Jobs",
                    source_url="https://huggingface.co/jobs/ml-engineer",
                ),
            ]
            for job in job_offers:
                session.add(job)
            await session.commit()
            print(f"✅ {len(job_offers)} offres d'emploi ajoutées")
            
            print("\n" + "="*70)
            print("🎉 UTILISATEUR DE TEST CRÉÉ AVEC SUCCÈS !")
            print("="*70)
            print(f"\n📧 Email    : {TEST_USER['email']}")
            print(f"🔑 Password : {TEST_USER['password']}")
            print(f"👤 Nom      : {TEST_USER['full_name']}")
            print(f"\n📊 Données créées:")
            print(f"   • 1 profil complet (95% complétion)")
            print(f"   • 3 expériences professionnelles (5 ans)")
            print(f"   • 2 formations universitaires")
            print(f"   • {len(skills_data)} compétences techniques")
            print(f"   • {len(job_offers)} offres d'emploi (Google, Datadog, Stripe, etc.)")
            print(f"\n🌐 Connexion : http://localhost:3000")
            print(f"📖 Scénario de test : TEST_SCENARIO.md")
            print("="*70 + "\n")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
            await session.rollback()
        finally:
            await engine.dispose()

if __name__ == "__main__":
    print("🚀 Démarrage création utilisateur de test...\n")
    asyncio.run(create_test_data())
