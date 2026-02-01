"""
Service de génération d'embeddings avec sentence-transformers.
Utilisé pour le matching sémantique entre profils et offres.
"""
from typing import List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service pour générer des embeddings avec sentence-transformers"""
    
    _model: Optional[SentenceTransformer] = None
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # 384 dimensions
    EMBEDDING_DIM = 384
    
    @classmethod
    def get_model(cls) -> SentenceTransformer:
        """Lazy loading du modèle (charge une seule fois)"""
        if cls._model is None:
            logger.info(f"Loading embedding model: {cls.MODEL_NAME}")
            cls._model = SentenceTransformer(cls.MODEL_NAME)
            logger.info("Embedding model loaded successfully")
        return cls._model
    
    @classmethod
    def generate_embedding(cls, text: str) -> List[float]:
        """
        Génère un embedding pour un texte donné.
        
        Args:
            text: Texte à encoder
            
        Returns:
            Liste de 384 floats (embedding vector)
        """
        if not text or not text.strip():
            # Retourner un vecteur nul si texte vide
            return [0.0] * cls.EMBEDDING_DIM
        
        model = cls.get_model()
        embedding = model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    @classmethod
    def generate_embeddings_batch(cls, texts: List[str]) -> List[List[float]]:
        """
        Génère des embeddings pour plusieurs textes (plus efficace).
        
        Args:
            texts: Liste de textes à encoder
            
        Returns:
            Liste d'embeddings
        """
        if not texts:
            return []
        
        model = cls.get_model()
        embeddings = model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
    
    @classmethod
    def cosine_similarity(cls, vec1: List[float], vec2: List[float]) -> float:
        """
        Calcule la similarité cosinus entre deux vecteurs.
        
        Args:
            vec1: Premier vecteur
            vec2: Deuxième vecteur
            
        Returns:
            Score entre -1 et 1 (1 = identique, 0 = orthogonal, -1 = opposé)
        """
        if not vec1 or not vec2:
            return 0.0
        
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        
        # Normaliser les vecteurs
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Cosine similarity
        similarity = np.dot(v1, v2) / (norm1 * norm2)
        return float(similarity)
    
    @classmethod
    def profile_to_text(cls, profile: dict) -> str:
        """
        Convertit un profil en texte pour l'embedding.
        
        Args:
            profile: Dict avec title, summary, experiences, skills
            
        Returns:
            Texte représentant le profil
        """
        parts = []
        
        # Titre du profil
        if profile.get('title'):
            parts.append(f"Profil: {profile['title']}")
        
        # Résumé
        if profile.get('summary'):
            parts.append(profile['summary'])
        
        # Expériences (3 dernières)
        experiences = profile.get('experiences', [])
        for exp in experiences[:3]:
            parts.append(f"{exp.get('position', '')} chez {exp.get('company', '')}")
            if exp.get('description'):
                parts.append(exp['description'])
        
        # Compétences (top 20)
        skills = profile.get('skills', [])
        if skills:
            skill_names = [s.get('name', '') for s in skills[:20]]
            parts.append(f"Compétences: {', '.join(skill_names)}")
        
        # Éducation
        educations = profile.get('educations', [])
        for edu in educations[:2]:
            parts.append(f"{edu.get('degree', '')} en {edu.get('field_of_study', '')}")
        
        return " ".join(parts)
    
    @classmethod
    def job_offer_to_text(cls, job_offer: dict) -> str:
        """
        Convertit une offre d'emploi en texte pour l'embedding.
        
        Args:
            job_offer: Dict avec job_title, description, requirements, etc.
            
        Returns:
            Texte représentant l'offre
        """
        parts = []
        
        # Titre du poste
        if job_offer.get('job_title'):
            parts.append(f"Poste: {job_offer['job_title']}")
        
        # Entreprise
        if job_offer.get('company_name'):
            parts.append(f"Entreprise: {job_offer['company_name']}")
        
        # Description
        if job_offer.get('description'):
            parts.append(job_offer['description'])
        
        # Exigences
        if job_offer.get('requirements'):
            parts.append(f"Exigences: {job_offer['requirements']}")
        
        # Technologies extraites
        keywords = job_offer.get('extracted_keywords', [])
        if keywords:
            parts.append(f"Technologies: {', '.join(keywords[:15])}")
        
        return " ".join(parts)
