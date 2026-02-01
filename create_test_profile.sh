#!/bin/bash

# Script de création du profil de test complet
# Email: kenfackfranck08@gmail.com

set -e

echo "🚀 Création du profil de test complet pour Job Hunter AI"
echo "=========================================================="
echo ""

API_URL="http://localhost:8000/api/v1"
EMAIL="kenfackfranck08@gmail.com"
PASSWORD="TestJobHunter2026!"
FULL_NAME="Franck Kenfack"

echo "📝 Étape 1/5 : Création du compte utilisateur..."

# Créer le compte
SIGNUP_RESPONSE=$(curl -s -X POST "$API_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMAIL\",
    \"password\": \"$PASSWORD\",
    \"full_name\": \"$FULL_NAME\"
  }")

echo "$SIGNUP_RESPONSE" | jq '.'

if echo "$SIGNUP_RESPONSE" | grep -q "error\|detail"; then
  echo "⚠️  Le compte existe peut-être déjà. Tentative de connexion..."
fi

echo ""
echo "🔑 Étape 2/5 : Connexion et récupération du token..."

# Se connecter
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMAIL\",
    \"password\": \"$PASSWORD\"
  }")

TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.access_token')

if [ "$TOKEN" == "null" ] || [ -z "$TOKEN" ]; then
  echo "❌ Erreur de connexion:"
  echo "$LOGIN_RESPONSE" | jq '.'
  exit 1
fi

echo "✅ Token obtenu: ${TOKEN:0:20}..."

echo ""
echo "👤 Étape 3/5 : Mise à jour des informations utilisateur..."

# Mettre à jour le profil utilisateur
USER_UPDATE=$(curl -s -X PUT "$API_URL/auth/me" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"full_name\": \"$FULL_NAME\",
    \"phone\": \"+33 6 12 34 56 78\",
    \"location\": \"Paris, France\"
  }")

echo "$USER_UPDATE" | jq '.'

echo ""
echo "📄 Étape 4/5 : Création du profil Backend Python..."

# Créer le profil Backend Python
PROFILE_RESPONSE=$(curl -s -X POST "$API_URL/profiles" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Développeur Backend Python Senior",
    "summary": "Développeur Backend Python avec 5+ ans d'\''expérience dans la conception et le développement d'\''APIs REST et microservices scalables. Expert en FastAPI, Django, et PostgreSQL. Passionné par l'\''architecture logicielle et les bonnes pratiques DevOps. Capable de travailler en équipe agile et de mentorer des développeurs juniors.",
    "phone": "+33 6 12 34 56 78",
    "location": "Paris, France",
    "skills": [
      {"name": "Python", "level": "expert"},
      {"name": "FastAPI", "level": "expert"},
      {"name": "Django", "level": "advanced"},
      {"name": "PostgreSQL", "level": "advanced"},
      {"name": "Docker", "level": "advanced"},
      {"name": "Redis", "level": "intermediate"},
      {"name": "Celery", "level": "intermediate"},
      {"name": "SQLAlchemy", "level": "advanced"},
      {"name": "REST API", "level": "expert"},
      {"name": "Microservices", "level": "advanced"},
      {"name": "AWS", "level": "intermediate"},
      {"name": "CI/CD", "level": "intermediate"},
      {"name": "Git", "level": "advanced"},
      {"name": "pytest", "level": "advanced"},
      {"name": "Async/Await", "level": "advanced"},
      {"name": "Alembic", "level": "intermediate"},
      {"name": "Pydantic", "level": "advanced"},
      {"name": "OAuth2", "level": "intermediate"},
      {"name": "JWT", "level": "intermediate"}
    ],
    "experiences": [
      {
        "company": "Tech Innovators SAS",
        "position": "Senior Backend Developer",
        "location": "Paris",
        "start_date": "2021-03-01",
        "end_date": null,
        "is_current": true,
        "description": "• Conception et développement d'\''APIs REST avec FastAPI pour des applications SaaS\n• Mise en place d'\''une architecture microservices avec Docker et Kubernetes\n• Optimisation des performances des requêtes SQL (réduction de 60% du temps de réponse)\n• Mentoring de 3 développeurs juniors\n• Mise en place de CI/CD avec GitLab et AWS"
      },
      {
        "company": "Digital Solutions",
        "position": "Backend Developer",
        "location": "Lyon",
        "start_date": "2019-01-01",
        "end_date": "2021-02-28",
        "is_current": false,
        "description": "• Développement d'\''APIs Django pour une plateforme e-commerce\n• Intégration de services de paiement (Stripe, PayPal)\n• Gestion de files d'\''attente avec Celery et Redis\n• Tests unitaires et d'\''intégration avec pytest"
      }
    ],
    "educations": [
      {
        "institution": "École Supérieure d'\''Informatique",
        "degree": "Master Informatique",
        "field_of_study": "Génie Logiciel",
        "location": "Paris",
        "start_date": "2016-09-01",
        "end_date": "2018-06-30",
        "description": "Spécialisation en architecture logicielle et systèmes distribués"
      }
    ]
  }')

PROFILE_ID=$(echo "$PROFILE_RESPONSE" | jq -r '.id // .profile.id')
echo "✅ Profil créé avec ID: $PROFILE_ID"
echo "$PROFILE_RESPONSE" | jq '.'

echo ""
echo "🔄 Étape 5/5 : Création d'une variante Full-Stack..."

# Créer le profil Full-Stack
PROFILE2_RESPONSE=$(curl -s -X POST "$API_URL/profiles" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Développeur Full-Stack Python/React",
    "summary": "Développeur Full-Stack spécialisé en Python backend (FastAPI) et React frontend. Capable de gérer des projets de A à Z avec une architecture moderne et scalable. Expérience en Next.js, TypeScript, et TailwindCSS pour créer des interfaces utilisateur performantes et élégantes.",
    "phone": "+33 6 12 34 56 78",
    "location": "Paris, France",
    "skills": [
      {"name": "Python", "level": "expert"},
      {"name": "FastAPI", "level": "expert"},
      {"name": "React", "level": "advanced"},
      {"name": "Next.js", "level": "advanced"},
      {"name": "TypeScript", "level": "advanced"},
      {"name": "JavaScript", "level": "expert"},
      {"name": "TailwindCSS", "level": "advanced"},
      {"name": "PostgreSQL", "level": "advanced"},
      {"name": "Docker", "level": "advanced"},
      {"name": "REST API", "level": "expert"},
      {"name": "GraphQL", "level": "intermediate"},
      {"name": "Git", "level": "advanced"},
      {"name": "Redux", "level": "intermediate"},
      {"name": "Zustand", "level": "intermediate"},
      {"name": "Vercel", "level": "intermediate"}
    ],
    "experiences": [
      {
        "company": "Tech Innovators SAS",
        "position": "Full-Stack Developer",
        "location": "Paris",
        "start_date": "2021-03-01",
        "end_date": null,
        "is_current": true,
        "description": "• Développement Full-Stack avec FastAPI et Next.js\n• Création d'\''interfaces utilisateur modernes avec React et TailwindCSS\n• Intégration d'\''APIs REST et gestion d'\''état avec Zustand\n• Optimisation SEO et performance des applications Next.js"
      }
    ],
    "educations": [
      {
        "institution": "École Supérieure d'\''Informatique",
        "degree": "Master Informatique",
        "field_of_study": "Génie Logiciel",
        "location": "Paris",
        "start_date": "2016-09-01",
        "end_date": "2018-06-30",
        "description": "Spécialisation en développement web et mobile"
      }
    ]
  }')

PROFILE2_ID=$(echo "$PROFILE2_RESPONSE" | jq -r '.id // .profile.id')
echo "✅ Variante créée avec ID: $PROFILE2_ID"
echo "$PROFILE2_RESPONSE" | jq '.'

echo ""
echo "✅ CONFIGURATION TERMINÉE!"
echo "========================="
echo ""
echo "📧 Email: $EMAIL"
echo "🔐 Mot de passe: $PASSWORD"
echo "👤 Nom: $FULL_NAME"
echo "📱 Téléphone: +33 6 12 34 56 78"
echo "📍 Localisation: Paris, France"
echo ""
echo "📝 Profils créés:"
echo "  1. Développeur Backend Python Senior (ID: $PROFILE_ID)"
echo "  2. Développeur Full-Stack Python/React (ID: $PROFILE2_ID)"
echo ""
echo "🎯 Vous pouvez maintenant:"
echo "  1. Se connecter sur http://localhost:3000"
echo "  2. Naviguer vers 'Recherche d'emplois'"
echo "  3. Rechercher: 'Python Developer' à 'Paris'"
echo "  4. Analyser une offre"
echo "  5. Générer CV + Lettre de motivation"
echo ""
echo "📖 Guide complet: ~/.copilot/session-state/*/files/TEST_GUIDE_COMPLET.md"
