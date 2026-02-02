"""
Service pour parser les CV PDF et extraire les informations structurées
"""
import pdfplumber
from typing import Dict, Any, Optional
from fastapi import UploadFile
from app.services.ai_service import AIService
import logging

logger = logging.getLogger(__name__)


class CVParserService:
    """Service pour parser les CV PDF avec IA"""
    
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
    
    async def parse_cv_pdf(self, pdf_file: UploadFile) -> Dict[str, Any]:
        """
        Parse un CV PDF et extrait les informations structurées
        
        Args:
            pdf_file: Fichier PDF uploadé
            
        Returns:
            Dict avec les données du profil extraites
        """
        try:
            # 1. Extraire le texte du PDF
            logger.info(f"📄 Extraction du texte du PDF: {pdf_file.filename}")
            text = await self._extract_text_from_pdf(pdf_file)
            
            if not text or len(text.strip()) < 50:
                raise ValueError("Le PDF ne contient pas assez de texte lisible")
            
            logger.info(f"✅ Texte extrait: {len(text)} caractères")
            
            # 2. Parser avec IA
            logger.info("🤖 Analyse du CV avec IA...")
            profile_data = await self._parse_with_ai(text)
            
            logger.info("✅ CV parsé avec succès")
            return profile_data
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du parsing du CV: {e}")
            raise
    
    async def _extract_text_from_pdf(self, pdf_file: UploadFile) -> str:
        """Extrait le texte brut d'un fichier PDF"""
        try:
            # Lire le contenu du fichier
            contents = await pdf_file.read()
            
            # Parser avec pdfplumber
            text_parts = []
            with pdfplumber.open(contents) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
            
            # Remettre le curseur au début pour une éventuelle réutilisation
            await pdf_file.seek(0)
            
            return "\n\n".join(text_parts)
            
        except Exception as e:
            logger.error(f"Erreur extraction PDF: {e}")
            raise ValueError(f"Impossible de lire le PDF: {str(e)}")
    
    async def _parse_with_ai(self, cv_text: str) -> Dict[str, Any]:
        """Parse le texte du CV avec IA et retourne un JSON structuré"""
        
        prompt = f"""
Tu es un expert en parsing de CV. Analyse le CV suivant et extrait TOUTES les informations dans un JSON structuré.

FORMAT DE SORTIE (JSON strict):
{{
  "full_name": "Nom complet de la personne",
  "title": "Titre professionnel principal",
  "summary": "Résumé professionnel (3-4 phrases)",
  "phone": "Numéro de téléphone",
  "location": "Ville, Pays",
  "linkedin_url": "URL LinkedIn si disponible",
  "github_url": "URL GitHub si disponible",
  "portfolio_url": "URL portfolio/site web si disponible",
  "experiences": [
    {{
      "title": "Intitulé du poste",
      "company": "Nom de l'entreprise",
      "location": "Ville, Pays",
      "start_date": "YYYY-MM-DD",
      "end_date": "YYYY-MM-DD ou null si poste actuel",
      "current": true/false,
      "description": "Description détaillée des missions et réalisations",
      "technologies": ["tech1", "tech2"]
    }}
  ],
  "educations": [
    {{
      "degree": "Diplôme obtenu",
      "institution": "Nom de l'établissement",
      "field_of_study": "Domaine d'études",
      "location": "Ville, Pays",
      "start_date": "YYYY-MM-DD",
      "end_date": "YYYY-MM-DD",
      "description": "Mention, spécialisation, projets importants"
    }}
  ],
  "skills": [
    {{
      "name": "Nom de la compétence",
      "category": "Technique|Soft Skills|Langues|Outils",
      "level": "Débutant|Intermédiaire|Avancé|Expert"
    }}
  ]
}}

RÈGLES IMPORTANTES:
1. Si une information n'est pas disponible, mets null (pas de string vide)
2. Pour les dates, utilise le format YYYY-MM-DD (exemple: 2023-09-01)
3. Si seulement l'année est mentionnée, utilise YYYY-01-01
4. Pour les postes actuels, end_date = null et current = true
5. Extrait TOUTES les compétences mentionnées (techniques, soft skills, langues, outils)
6. Pour les technologies dans experiences, liste tous les outils/langages mentionnés
7. Le résumé doit être informatif et professionnel (pas juste une liste)
8. Retourne UNIQUEMENT le JSON, rien d'autre

CV À ANALYSER:
{cv_text}
"""
        
        try:
            # Appeler l'IA avec le prompt
            response = await self.ai_service.generate_text(prompt)
            
            # Parser la réponse JSON
            import json
            
            # Nettoyer la réponse (parfois l'IA ajoute des backticks)
            clean_response = response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:]
            if clean_response.startswith("```"):
                clean_response = clean_response[3:]
            if clean_response.endswith("```"):
                clean_response = clean_response[:-3]
            
            profile_data = json.loads(clean_response.strip())
            
            # Valider la structure minimale
            if not isinstance(profile_data, dict):
                raise ValueError("La réponse de l'IA n'est pas un objet JSON valide")
            
            # Assurer que les listes existent
            profile_data.setdefault("experiences", [])
            profile_data.setdefault("educations", [])
            profile_data.setdefault("skills", [])
            
            return profile_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Erreur parsing JSON: {e}")
            logger.error(f"Réponse IA: {response[:500]}")
            raise ValueError("L'IA n'a pas retourné un JSON valide")
        except Exception as e:
            logger.error(f"Erreur analyse IA: {e}")
            raise
