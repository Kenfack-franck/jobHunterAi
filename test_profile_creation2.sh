#!/bin/bash

API_URL="http://localhost:8000/api/v1"
TEST_EMAIL="test_profile_$(date +%s)@test.com"
TEST_PASSWORD="TestPassword123!"

echo "1️⃣  Création utilisateur: $TEST_EMAIL"
REGISTER_RESPONSE=$(curl -s -X POST "$API_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "'"$TEST_EMAIL"'",
    "password": "'"$TEST_PASSWORD"'",
    "full_name": "Test Profile User"
  }')

echo "Response: $REGISTER_RESPONSE"

# Login pour obtenir le token
echo ""
echo "2️⃣  Login"
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$TEST_EMAIL&password=$TEST_PASSWORD")

TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)

if [ -z "$TOKEN" ]; then
  echo "❌ Échec login"
  exit 1
fi

echo "✅ Token obtenu"

# Créer profil
echo ""
echo "3️⃣  Création profil avec relations"

PROFILE_DATA='{
  "title": "Développeur Full Stack",
  "summary": "Passionné par le développement",
  "phone": "+33612345678",
  "location": "Paris",
  "experiences": [
    {
      "title": "Lead Developer",
      "company": "Tech Corp",
      "location": "Paris",
      "start_date": "2020-01-15",
      "end_date": "2023-12-31",
      "current": false,
      "description": "Dev web"
    },
    {
      "title": "Junior Dev",
      "company": "Startup",
      "location": "Lyon",
      "start_date": "2018-06-01",
      "end_date": "2019-12-31",
      "current": false,
      "description": "Premier poste"
    }
  ],
  "educations": [
    {
      "degree": "Master Info",
      "institution": "Univ Paris",
      "field_of_study": "GL",
      "location": "Paris",
      "start_date": "2016-09-01",
      "end_date": "2018-06-30"
    }
  ],
  "skills": [
    {"name": "Python", "category": "language", "level": "expert"},
    {"name": "React", "category": "framework", "level": "advanced"},
    {"name": "Docker", "category": "tool", "level": "intermediate"}
  ]
}'

CREATE_RESPONSE=$(curl -s -X POST "$API_URL/profile" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "$PROFILE_DATA")

echo "Réponse création:"
echo "$CREATE_RESPONSE" | python3 -m json.tool

# Récupérer pour vérifier
echo ""
echo "4️⃣  Vérification"
GET_RESPONSE=$(curl -s -X GET "$API_URL/profile" \
  -H "Authorization: Bearer $TOKEN")

EXP=$(echo "$GET_RESPONSE" | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('experiences', [])))")
EDU=$(echo "$GET_RESPONSE" | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('educations', [])))")
SKL=$(echo "$GET_RESPONSE" | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('skills', [])))")

echo "✅ Expériences: $EXP (attendu: 2)"
echo "✅ Formations: $EDU (attendu: 1)"
echo "✅ Compétences: $SKL (attendu: 3)"

if [ "$EXP" = "2" ] && [ "$EDU" = "1" ] && [ "$SKL" = "3" ]; then
  echo ""
  echo "🎉 TEST RÉUSSI !"
else
  echo "❌ Problème détecté"
fi
