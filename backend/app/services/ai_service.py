"""
Service IA pour la génération de documents (CV, Lettres de Motivation)
Utilise OpenAI GPT puis Gemini en fallback, et templates statiques en dernier recours
"""
import os
from typing import Optional, Literal
from openai import AsyncOpenAI
import google.generativeai as genai
from app.models.profile import Profile
from app.models.job_offer import JobOffer


class AIService:
    """Service pour générer du contenu IA avec fallback OpenAI → Gemini → Templates"""
    
    def __init__(self):
        # Configuration OpenAI
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.openai_client = None
        if self.openai_key:
            try:
                self.openai_client = AsyncOpenAI(api_key=self.openai_key)
                print("✅ OpenAI configuré (priorité 1)")
            except Exception as e:
                print(f"⚠️  OpenAI non disponible: {e}")
        
        # Configuration Gemini
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.gemini_model = None
        if self.gemini_key:
            try:
                genai.configure(api_key=self.gemini_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
                print("✅ Gemini configuré (priorité 2)")
            except Exception as e:
                print(f"⚠️  Gemini non disponible: {e}")
        
        # Fallback mode (templates)
        if not self.openai_client and not self.gemini_model:
            print("⚠️  Mode TEMPLATES uniquement (aucune API IA disponible)")
    
    async def generate_text(self, prompt: str, max_tokens: int = 2000) -> str:
        """
        Génère du texte avec IA (OpenAI ou Gemini)
        Utilisé pour le parsing de CV et autres tâches génériques
        """
        # Essayer OpenAI d'abord
        if self.openai_client:
            try:
                response = await self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=0.3
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"❌ OpenAI failed: {e}")
        
        # Fallback Gemini
        if self.gemini_model:
            try:
                response = self.gemini_model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"❌ Gemini failed: {e}")
        
        raise Exception("Aucun service IA disponible pour générer du texte")
    
    async def generate_resume(
        self,
        profile: Profile,
        job_offer: JobOffer,
        tone: Literal["professional", "creative", "dynamic"] = "professional",
        language: Literal["fr", "en"] = "fr"
    ) -> str:
        """
        Génère un CV personnalisé avec fallback intelligent
        Essaie: OpenAI → Gemini → Templates
        
        Args:
            profile: Profil utilisateur avec expériences/compétences
            job_offer: Offre d'emploi ciblée
            tone: Ton du CV (professional/creative/dynamic)
            language: Langue (fr/en)
            
        Returns:
            CV en format Markdown
        """
        # Construire les contextes
        profile_context = self._build_profile_context(profile)
        job_context = self._build_job_context(job_offer)
        system_prompt = self._get_resume_system_prompt(tone, language)
        
        user_prompt = f"""
Génère un CV optimisé pour cette offre d'emploi.

# PROFIL DU CANDIDAT
{profile_context}

# OFFRE D'EMPLOI CIBLÉE
{job_context}

# INSTRUCTIONS
- Réorganise les expériences pour mettre en avant celles pertinentes pour ce poste
- Adapte la description de chaque expérience pour montrer les compétences demandées
- Mets en avant les compétences qui correspondent aux mots-clés de l'offre
- Utilise des verbes d'action et des résultats quantifiables
- Format Markdown avec sections: En-tête, Résumé, Compétences, Expériences, Formation
- Longueur: 1 page maximum (environ 400-500 mots)
"""
        
        # Essayer OpenAI en priorité
        if self.openai_client:
            try:
                print("🔄 Tentative génération CV avec OpenAI...")
                response = await self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                print("✅ CV généré avec OpenAI")
                return response.choices[0].message.content
            except Exception as e:
                print(f"❌ OpenAI échec: {e}")
        
        # Fallback vers Gemini
        if self.gemini_model:
            try:
                print("🔄 Tentative génération CV avec Gemini...")
                # Gemini n'a pas de messages système, on combine tout
                full_prompt = f"{system_prompt}\n\n{user_prompt}"
                response = self.gemini_model.generate_content(full_prompt)
                print("✅ CV généré avec Gemini")
                return response.text
            except Exception as e:
                print(f"❌ Gemini échec: {e}")
        
        # Dernier recours: Templates
        print("⚠️  Fallback vers templates statiques")
        return self._generate_resume_template(profile, job_offer, language)
    
    async def generate_cover_letter(
        self,
        profile: Profile,
        job_offer: JobOffer,
        tone: Literal["professional", "enthusiastic", "confident"] = "professional",
        length: Literal["short", "medium", "long"] = "medium",
        language: Literal["fr", "en"] = "fr"
    ) -> str:
        """
        Génère une lettre de motivation personnalisée avec fallback
        Essaie: OpenAI → Gemini → Templates
        
        Args:
            profile: Profil utilisateur
            job_offer: Offre d'emploi ciblée
            tone: Ton de la lettre
            length: Longueur (short=150 mots, medium=250, long=350)
            language: Langue (fr/en)
            
        Returns:
            Lettre de motivation en texte brut
        """
        profile_context = self._build_profile_context(profile)
        job_context = self._build_job_context(job_offer)
        system_prompt = self._get_cover_letter_system_prompt(tone, language)
        
        length_guide = {
            "short": "150 mots maximum (3 paragraphes courts)",
            "medium": "250 mots (4-5 paragraphes)",
            "long": "350 mots (5-6 paragraphes détaillés)"
        }
        
        user_prompt = f"""
Génère une lettre de motivation convaincante pour cette candidature.

# PROFIL DU CANDIDAT
{profile_context}

# OFFRE D'EMPLOI
{job_context}

# INSTRUCTIONS
- Longueur: {length_guide[length]}
- Structure: Introduction (pourquoi ce poste), Corps (mes atouts), Conclusion (call to action)
- Montre l'adéquation entre mon profil et les besoins de l'entreprise
- Utilise des exemples concrets tirés de mes expériences
- Explique pourquoi je suis motivé par ce poste spécifique
- Ne répète pas le CV, apporte un éclairage complémentaire
- Termine par une phrase d'ouverture pour un entretien
"""
        
        # Essayer OpenAI en priorité
        if self.openai_client:
            try:
                print("🔄 Tentative génération LM avec OpenAI...")
                response = await self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.8,  # Plus de créativité pour les lettres
                    max_tokens=1500
                )
                print("✅ Lettre générée avec OpenAI")
                return response.choices[0].message.content
            except Exception as e:
                print(f"❌ OpenAI échec: {e}")
        
        # Fallback vers Gemini
        if self.gemini_model:
            try:
                print("🔄 Tentative génération LM avec Gemini...")
                full_prompt = f"{system_prompt}\n\n{user_prompt}"
                response = self.gemini_model.generate_content(full_prompt)
                print("✅ Lettre générée avec Gemini")
                return response.text
            except Exception as e:
                print(f"❌ Gemini échec: {e}")
        
        # Dernier recours: Templates
        print("⚠️  Fallback vers templates statiques")
        return self._generate_cover_letter_template(profile, job_offer, language, tone, length)
    
    def _build_profile_context(self, profile: Profile) -> str:
        """Construit le contexte du profil pour les prompts"""
        context_parts = [
            f"**Titre**: {profile.title}",
        ]
        
        if profile.summary:
            context_parts.append(f"**Résumé**: {profile.summary}")
        
        # Compétences
        if hasattr(profile, 'skills') and profile.skills:
            skills_text = ", ".join([
                f"{skill.name} ({skill.level})" 
                for skill in profile.skills
            ])
            context_parts.append(f"**Compétences**: {skills_text}")
        
        # Expériences
        if hasattr(profile, 'experiences') and profile.experiences:
            context_parts.append("\n**Expériences professionnelles**:")
            for exp in profile.experiences:
                exp_text = f"- {exp.title} chez {exp.company}"
                if exp.start_date:
                    exp_text += f" ({exp.start_date.strftime('%Y')} - "
                    exp_text += f"{exp.end_date.strftime('%Y') if exp.end_date else 'Présent'})"
                if exp.description:
                    exp_text += f"\n  {exp.description[:200]}"
                if exp.technologies:
                    exp_text += f"\n  Technologies: {', '.join(exp.technologies)}"
                context_parts.append(exp_text)
        
        # Formation
        if hasattr(profile, 'educations') and profile.educations:
            context_parts.append("\n**Formation**:")
            for edu in profile.educations:
                edu_text = f"- {edu.degree} - {edu.institution}"
                if edu.start_date:
                    edu_text += f" ({edu.start_date.strftime('%Y')})"
                context_parts.append(edu_text)
        
        return "\n".join(context_parts)
    
    def _build_job_context(self, job_offer: JobOffer) -> str:
        """Construit le contexte de l'offre pour les prompts"""
        context_parts = [
            f"**Poste**: {job_offer.job_title}",
            f"**Entreprise**: {job_offer.company_name or 'Non spécifiée'}",
        ]
        
        if job_offer.location:
            context_parts.append(f"**Lieu**: {job_offer.location}")
        
        if job_offer.description:
            context_parts.append(f"\n**Description**:\n{job_offer.description[:500]}")
        
        if job_offer.requirements:
            context_parts.append(f"\n**Exigences**:\n{job_offer.requirements[:500]}")
        
        if job_offer.extracted_keywords:
            keywords = ", ".join(job_offer.extracted_keywords[:10])
            context_parts.append(f"\n**Mots-clés importants**: {keywords}")
        
        return "\n".join(context_parts)
    
    def _get_resume_system_prompt(self, tone: str, language: str) -> str:
        """Génère le prompt système pour le CV"""
        tone_descriptions = {
            "professional": "formel, concis, orienté résultats",
            "creative": "original, storytelling, mise en valeur de la personnalité",
            "dynamic": "énergique, impact immédiat, verbes d'action puissants"
        }
        
        language_instruction = {
            "fr": "Réponds UNIQUEMENT en français.",
            "en": "Respond ONLY in English."
        }
        
        return f"""Tu es un expert en rédaction de CV professionnel avec 15 ans d'expérience en recrutement.
Ton rôle est de créer des CV optimisés pour les ATS (Applicant Tracking Systems) et qui attirent l'œil des recruteurs.

Ton style doit être {tone_descriptions[tone]}.
{language_instruction[language]}

Règles strictes:
1. Format Markdown uniquement (pas de HTML)
2. Structure claire avec titres ## et ###
3. Utilise des bullet points (-)
4. Quantifie les résultats (ex: "Augmenté les performances de 30%")
5. Adapte CHAQUE phrase pour correspondre à l'offre ciblée
6. Ne mentionne JAMAIS que c'est généré par IA
7. Reste factuel, pas de mensonges sur les compétences"""
    
    def _get_cover_letter_system_prompt(self, tone: str, language: str) -> str:
        """Génère le prompt système pour la lettre de motivation"""
        tone_descriptions = {
            "professional": "courtois, respectueux, sérieux mais chaleureux",
            "enthusiastic": "passionné, énergique, montrant un fort intérêt",
            "confident": "assuré, affirmé, montrant leadership et initiative"
        }
        
        language_instruction = {
            "fr": "Réponds UNIQUEMENT en français avec vouvoiement.",
            "en": "Respond ONLY in English."
        }
        
        return f"""Tu es un expert en rédaction de lettres de motivation.
Tu sais créer des lettres qui captivent l'attention et donnent envie de rencontrer le candidat.

Ton style doit être {tone_descriptions[tone]}.
{language_instruction[language]}

Règles strictes:
1. Texte brut uniquement (pas de Markdown)
2. Paragraphes courts et percutants
3. Raconte une histoire, ne liste pas des compétences
4. Montre la motivation SPÉCIFIQUE pour CETTE entreprise et CE poste
5. Utilise le "je" avec parcimonie, parle surtout de ce que TU apportes à L'ENTREPRISE
6. Ne mentionne JAMAIS que c'est généré par IA
7. Termine par une ouverture pour un entretien"""
    
    # ===== MÉTHODES TEMPLATES POUR MODE TEST =====
    
    def _generate_resume_template(self, profile: Profile, job_offer: JobOffer, language: str) -> str:
        """Génère un CV avec un template (mode TEST sans OpenAI)"""
        
        # Récupérer les compétences
        skills_list = []
        if hasattr(profile, 'skills') and profile.skills:
            skills_list = [f"{skill.name} ({skill.level})" for skill in profile.skills[:8]]
        skills_text = " • ".join(skills_list) if skills_list else "Python, JavaScript, SQL"
        
        # Récupérer les expériences
        experiences_text = ""
        if hasattr(profile, 'experiences') and profile.experiences:
            for exp in profile.experiences[:3]:
                experiences_text += f"\n\n### {exp.title} — {exp.company}\n"
                if exp.start_date:
                    experiences_text += f"*{exp.start_date.strftime('%Y')} - "
                    experiences_text += f"{exp.end_date.strftime('%Y') if exp.end_date else 'Présent'}*\n\n"
                if exp.description:
                    experiences_text += f"{exp.description[:200]}...\n"
                if exp.technologies:
                    experiences_text += f"\n**Technologies**: {', '.join(exp.technologies[:5])}"
        else:
            experiences_text = "\n\n### Développeur Backend — Entreprise Tech\n*2020 - Présent*\n\nDéveloppement d'APIs REST performantes et scalables."
        
        # Récupérer la formation
        education_text = ""
        if hasattr(profile, 'educations') and profile.educations:
            for edu in profile.educations[:2]:
                education_text += f"\n- **{edu.degree}** — {edu.institution}"
                if edu.start_date:
                    education_text += f" ({edu.start_date.strftime('%Y')})"
        else:
            education_text = "\n- **Master Informatique** — Université (2020)"
        
        template_fr = f"""# {profile.title}

## 📧 Contact
Email: contact@example.com | Téléphone: +33 6 XX XX XX XX  
LinkedIn: linkedin.com/in/profile | GitHub: github.com/profile

## 💼 Résumé Professionnel

{profile.summary or 'Développeur passionné avec une forte expertise en développement backend et une solide maîtrise des technologies modernes. Capacité démontrée à concevoir et implémenter des solutions scalables et performantes.'}

## 🛠️ Compétences Clés

{skills_text}

## 💻 Expérience Professionnelle
{experiences_text}

## 🎓 Formation
{education_text}

---

*CV optimisé pour le poste de {job_offer.job_title} chez {job_offer.company_name or 'votre entreprise'}*
"""
        
        template_en = f"""# {profile.title}

## 📧 Contact
Email: contact@example.com | Phone: +1 XXX XXX XXXX  
LinkedIn: linkedin.com/in/profile | GitHub: github.com/profile

## 💼 Professional Summary

{profile.summary or 'Passionate developer with strong expertise in backend development and solid mastery of modern technologies. Demonstrated ability to design and implement scalable, high-performance solutions.'}

## 🛠️ Key Skills

{skills_text}

## 💻 Professional Experience
{experiences_text}

## 🎓 Education
{education_text}

---

*Resume optimized for {job_offer.job_title} position at {job_offer.company_name or 'your company'}*
"""
        
        return template_fr if language == "fr" else template_en
    
    def _generate_cover_letter_template(
        self, 
        profile: Profile, 
        job_offer: JobOffer, 
        language: str,
        tone: str,
        length: str
    ) -> str:
        """Génère une lettre de motivation avec un template (mode TEST)"""
        
        company = job_offer.company_name or "votre entreprise"
        position = job_offer.job_title
        
        # Adapter la longueur
        if length == "short":
            paragraphs = 3
        elif length == "long":
            paragraphs = 5
        else:
            paragraphs = 4
        
        if language == "fr":
            intro = f"Madame, Monsieur,\n\nC'est avec un vif intérêt que je vous soumets ma candidature pour le poste de {position} au sein de {company}."
            
            body1 = f"\nFort(e) de mon expérience en tant que {profile.title}, j'ai développé une expertise solide dans les domaines qui correspondent parfaitement aux exigences de ce poste. Ma maîtrise des technologies modernes et ma capacité à m'adapter rapidement aux nouveaux défis me permettent de contribuer efficacement dès le premier jour."
            
            body2 = f"\nCe qui m'attire particulièrement chez {company}, c'est votre approche innovante et votre engagement envers l'excellence technique. Je suis convaincu(e) que mes compétences techniques et ma passion pour le développement de solutions performantes seront des atouts précieux pour votre équipe."
            
            body3 = "\nAu cours de mes expériences précédentes, j'ai eu l'occasion de travailler sur des projets complexes nécessitant rigueur, créativité et esprit d'équipe. Ces expériences m'ont permis de développer une approche pragmatique de la résolution de problèmes et une forte orientation vers les résultats."
            
            conclusion = f"\nJe serais ravi(e) de pouvoir échanger avec vous sur la manière dont je pourrais contribuer au succès de {company}. Je me tiens à votre disposition pour un entretien à votre convenance.\n\nDans l'attente de votre retour, je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées."
            
            parts = [intro, body1]
            if paragraphs >= 4:
                parts.append(body2)
            if paragraphs >= 5:
                parts.append(body3)
            parts.append(conclusion)
            
            return "\n".join(parts)
        
        else:  # English
            intro = f"Dear Hiring Manager,\n\nI am writing to express my strong interest in the {position} position at {company}."
            
            body1 = f"\nWith my experience as a {profile.title}, I have developed solid expertise in areas that align perfectly with the requirements of this role. My mastery of modern technologies and my ability to quickly adapt to new challenges enable me to contribute effectively from day one."
            
            body2 = f"\nWhat particularly attracts me to {company} is your innovative approach and commitment to technical excellence. I am confident that my technical skills and passion for developing high-performance solutions will be valuable assets to your team."
            
            conclusion = f"\nI would be delighted to discuss how I could contribute to {company}'s success. I am available for an interview at your convenience.\n\nThank you for considering my application. I look forward to hearing from you."
            
            parts = [intro, body1]
            if paragraphs >= 4:
                parts.append(body2)
            parts.append(conclusion)
            
            return "\n".join(parts)


# Instance globale du service
ai_service = AIService()
