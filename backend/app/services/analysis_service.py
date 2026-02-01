"""Service d'analyse simplifié"""
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.profile import Profile
from app.models.job_offer import JobOffer
from app.services.embedding_service import EmbeddingService

class AnalysisService:
    @classmethod
    async def calculate_compatibility_score(cls, profile_id: str, job_offer_id: str, db):
        # Load profile
        profile_query = select(Profile).where(Profile.id == profile_id).options(selectinload(Profile.skills))
        profile_result = await db.execute(profile_query)
        profile = profile_result.scalar_one_or_none()
        
        if not profile:
            raise ValueError("Profile not found")
        
        # Load job
        job_query = select(JobOffer).where(JobOffer.id == job_offer_id)
        job_result = await db.execute(job_query)
        job_offer = job_result.scalar_one_or_none()
        
        if not job_offer:
            raise ValueError("Job offer not found")
        
        # Generate/get embeddings
        profile_embedding = profile.embedding
        profile_needs_embedding = (profile_embedding is None)
        
        if profile_needs_embedding:
            profile_text = f"{profile.title or ''} {profile.summary or ''}"
            if profile.skills:
                skills = " ".join([s.name for s in profile.skills])
                profile_text += f" Compétences: {skills}"
            profile_embedding = EmbeddingService.generate_embedding(profile_text)
            profile.embedding = profile_embedding
            await db.commit()
        
        # Convert to list if needed
        if not isinstance(profile_embedding, list):
            profile_embedding = list(profile_embedding)
        
        job_embedding = job_offer.embedding
        job_needs_embedding = (job_embedding is None)
        
        if job_needs_embedding:
            job_text = f"{job_offer.job_title} {job_offer.company_name} {job_offer.description or ''}"
            if job_offer.extracted_keywords:
                job_text += " " + " ".join(job_offer.extracted_keywords[:15])
            job_embedding = EmbeddingService.generate_embedding(job_text)
            job_offer.embedding = job_embedding
            await db.commit()
        
        # Convert to list if needed
        if not isinstance(job_embedding, list):
            job_embedding = list(job_embedding)
        
        # Calculate similarity
        similarity = EmbeddingService.cosine_similarity(profile_embedding, job_embedding)
        score = int(max(0, min(100, (similarity + 1) * 50)))
        
        # Skills analysis
        profile_skills = [s.name.lower() for s in profile.skills] if profile.skills else []
        job_keywords = [k.lower() for k in (job_offer.extracted_keywords or [])]
        
        matching_skills = list(set(profile_skills) & set(job_keywords))
        missing_skills = list(set(job_keywords) - set(profile_skills))
        
        skills_match_ratio = len(matching_skills) / max(1, len(job_keywords)) if job_keywords else 0
        
        # Weighted final score
        skills_score = int(skills_match_ratio * 100)
        final_score = int(0.7 * score + 0.3 * skills_score)
        
        return {
            "score": final_score,
            "similarity_raw": round(similarity, 3),
            "matching_skills": matching_skills[:10],
            "missing_skills": missing_skills[:10],
            "total_profile_skills": len(profile_skills),
            "total_job_keywords": len(job_keywords),
            "skills_match_ratio": round(skills_match_ratio, 2),
            "score_breakdown": {
                "semantic_similarity": score,
                "skills_match": skills_score,
                "final_weighted": final_score
            }
        }
