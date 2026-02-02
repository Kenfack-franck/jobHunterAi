#!/bin/bash

# Test de création complète d'un profil avec expériences, formations et compétences

API_URL="http://localhost:8000/api/v1"

echo "========================================="
echo "TEST: Création profil avec relations"
echo "========================================="

# Créer un utilisateur test
TEST_EMAIL="test_profile_$(date +%s)@test.com"
TEST_PASSWORD="TestPassword123!"

echo ""
echo "1️⃣  Création utilisateur: $TEST_EMAIL"
REGISTER_RESPONSE=$(curl -s -X POST "$API_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "'"$TEST_EMAIL"'",
    "password": "'"$TEST_PASSWORD"'",
    "full_name": "Test Profile User"
  }')

# Extraire le token
TOKEN=$(echo "$REGISTER_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "❌ Échec création utilisateur"
  echo "$REGISTER_RESPONSE"
  exit 1
fi

echo "✅ Utilisateur créé, token obtenu"

# Créer un profil complet
echo ""
echo "2️⃣  Création profil avec 2 expériences, 2 formations, 3 compétences"

PROFILE_DATA='{
  "title": "Développeur Full Stack",
  "summary": "Passionné par le développement web",
  "phone": "+33612345678",
  "location": "Paris, France",
  "linkedin_url": "https://linkedin.com/in/test",
  "github_url": "https://github.com/test",
  "experiences": [
    {
      "title": "Lead Developer",
      "company": "Tech Corp",
      "location": "Paris",
      "start_date": "2020-01-15",
      "end_date": "2023-12-31",
      "current": false,
      "description": "Développement applications web"
    },
    {
      "title": "Junior Developer", 
      "company": "StartupXYZ",
      "location": "Lyon",
      "start_date": "2018-06-01",
      "end_date": "2019-12-31",
      "current": false,
      "description": "Premier poste"
    }
  ],
  "educations": [
    {
      "degree": "Master Informatique",
      "institution": "Université Paris",
      "field_of_study": "Génie Logiciel",
      "location": "Paris",
      "start_date": "2016-09-01",
      "end_date": "2018-06-30",
      "description": "Spécialisation développement web"
    },
    {
      "degree": "Licence Informatique",
      "institution": "Université Lyon",
      "field_of_study": "Informatique",
      "location": "Lyon",
      "start_date": "2013-09-01",
      "end_date": "2016-06-30"
    }
  ],
  "skills": [
    {
      "name": "Python",
      "category": "language",
      "level": "expert"
    },
    {
      "name": "React",
      "category": "framework",
      "level": "advanced"
    },
    {
      "name": "Docker",
      "category": "tool",
      "level": "intermediate"
    }
  ]
}'

CREATE_RESPONSE=$(curl -s -X POST "$API_URL/profile" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "$PROFILE_DATA")

# Vérifier la création
if echo "$CREATE_RESPONSE" | grep -q '"id"'; then
  echo "✅ Profil créé avec succès"
  
  # Compter les relations
  EXP_COUNT=$(echo "$CREATE_RESPONSE" | grep -o '"experiences":\[' | wc -l)
  EDU_COUNT=$(echo "$CREATE_RESPONSE" | grep -o '"educations":\[' | wc -l)
  SKILL_COUNT=$(echo "$CREATE_RESPONSE" | grep -o '"skills":\[' | wc -l)
  
  echo ""
  echo "📊 Vérification des relations créées:"
  echo "$CREATE_RESPONSE" | python3 -m json.tool | grep -A 5 '"experiences"'
  echo "$CREATE_RESPONSE" | python3 -m json.tool | grep -A 5 '"educations"'
  echo "$CREATE_RESPONSE" | python3 -m json.tool | grep -A 5 '"skills"'
else
  echo "❌ Échec création profil"
  echo "$CREATE_RESPONSE" | python3 -m json.tool
  exit 1
fi

# Récupérer le profil pour vérifier
echo ""
echo "3️⃣  Récupération du profil pour vérifier"

GET_RESPONSE=$(curl -s -X GET "$API_URL/profile" \
  -H "Authorization: Bearer $TOKEN")

EXP_LENGTH=$(echo "$GET_RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(len(data.get('experiences', [])))" 2>/dev/null || echo "0")
EDU_LENGTH=$(echo "$GET_RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(len(data.get('educations', [])))" 2>/dev/null || echo "0")
SKILL_LENGTH=$(echo "$GET_RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(len(data.get('skills', [])))" 2>/dev/null || echo "0")

echo "✅ Profil récupéré:"
echo "   - Expériences: $EXP_LENGTH (attendu: 2)"
echo "   - Formations: $EDU_LENGTH (attendu: 2)"
echo "   - Compétences: $SKILL_LENGTH (attendu: 3)"

if [ "$EXP_LENGTH" = "2" ] && [ "$EDU_LENGTH" = "2" ] && [ "$SKILL_LENGTH" = "3" ]; then
  echo ""
  echo "🎉 TEST RÉUSSI ! Toutes les relations sont sauvegardées !"
else
  echo ""
  echo "❌ TEST ÉCHOUÉ ! Les relations ne sont pas toutes sauvegardées"
  echo ""
  echo "Réponse complète:"
  echo "$GET_RESPONSE" | python3 -m json.tool
fi

echo ""
echo "========================================="
