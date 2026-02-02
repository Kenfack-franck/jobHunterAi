#!/bin/bash
set -e

API_URL="http://localhost:8000/api/v1"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  TEST COMPLET: Upload CV → Parse → Create Profile"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Créer un utilisateur
EMAIL="test_cv_$(date +%s)@test.com"
PASSWORD="Test123!"

echo ""
echo "1️⃣  Création utilisateur: $EMAIL"
REGISTER=$(curl -s -X POST "$API_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "'"$EMAIL"'",
    "password": "'"$PASSWORD"'",
    "full_name": "Test CV Upload"
  }')

echo "   Réponse: $(echo $REGISTER | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"ID: {d.get('id', 'N/A')}, Email: {d.get('email', 'N/A')}\")" 2>/dev/null || echo "ERREUR")"

# 2. Login
echo ""
echo "2️⃣  Login"
TOKEN=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d "{"email":"$EMAIL","password":"$PASSWORD"}" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)

if [ -z "$TOKEN" ]; then
  echo "   ❌ Échec login"
  exit 1
fi

echo "   ✅ Token obtenu: ${TOKEN:0:30}..."

# 3. Parser le CV
echo ""
echo "3️⃣  Upload et parsing CV_kenfack_franck.pdf"
PARSE_RESPONSE=$(curl -s -X POST "$API_URL/profile/parse-cv" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@CV_kenfack_franck.pdf")

echo ""
echo "   📊 Résultat du parsing:"
echo "$PARSE_RESPONSE" | python3 -m json.tool > /tmp/parsed_cv.json

# Compter les éléments
EXP_COUNT=$(echo "$PARSE_RESPONSE" | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('experiences', [])))" 2>/dev/null || echo "0")
EDU_COUNT=$(echo "$PARSE_RESPONSE" | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('educations', [])))" 2>/dev/null || echo "0")
SKILL_COUNT=$(echo "$PARSE_RESPONSE" | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('skills', [])))" 2>/dev/null || echo "0")

echo "   - Expériences: $EXP_COUNT"
echo "   - Formations: $EDU_COUNT"
echo "   - Compétences: $SKILL_COUNT"

if [ "$SKILL_COUNT" = "0" ]; then
  echo ""
  echo "   ⚠️  AUCUNE COMPÉTENCE TROUVÉE !"
  echo "   Réponse complète:"
  cat /tmp/parsed_cv.json
  exit 1
fi

# Vérifier un skill
echo ""
echo "   🔍 Premier skill:"
echo "$PARSE_RESPONSE" | python3 -c "import sys, json; s=json.load(sys.stdin).get('skills', [{}])[0]; print(f\"   Name: {s.get('name')}, Category: {s.get('category')}, Level: {s.get('level')}\")" 2>/dev/null

# Vérifier les dates
echo ""
echo "   🔍 Première expérience:"
echo "$PARSE_RESPONSE" | python3 -c "import sys, json; e=json.load(sys.stdin).get('experiences', [{}])[0]; print(f\"   Title: {e.get('title')}, Start: {e.get('start_date')}, End: {e.get('end_date')}\")" 2>/dev/null

# 4. Tenter de créer le profil avec ces données
echo ""
echo "4️⃣  Création du profil avec les données parsées"

CREATE_RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "$API_URL/profile" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "$PARSE_RESPONSE")

HTTP_CODE=$(echo "$CREATE_RESPONSE" | grep "HTTP_CODE:" | cut -d: -f2)
BODY=$(echo "$CREATE_RESPONSE" | sed '/HTTP_CODE:/d')

echo "   HTTP Status: $HTTP_CODE"

if [ "$HTTP_CODE" = "201" ]; then
  echo "   ✅ PROFIL CRÉÉ AVEC SUCCÈS !"
  
  # Vérifier
  PROFILE=$(curl -s -X GET "$API_URL/profile" \
    -H "Authorization: Bearer $TOKEN")
  
  P_EXP=$(echo "$PROFILE" | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('experiences', [])))" 2>/dev/null)
  P_EDU=$(echo "$PROFILE" | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('educations', [])))" 2>/dev/null)
  P_SKL=$(echo "$PROFILE" | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('skills', [])))" 2>/dev/null)
  
  echo ""
  echo "   📊 Profil sauvegardé:"
  echo "   - Expériences: $P_EXP"
  echo "   - Formations: $P_EDU"
  echo "   - Compétences: $P_SKL"
  
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  ✅ TEST RÉUSSI ! Workflow complet fonctionnel !"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
elif [ "$HTTP_CODE" = "422" ]; then
  echo "   ❌ ERREUR 422 - Validation échouée"
  echo ""
  echo "   Détails de l'erreur:"
  echo "$BODY" | python3 -m json.tool
  
  echo ""
  echo "   📄 Payload envoyé (saved to /tmp/failed_payload.json):"
  echo "$PARSE_RESPONSE" | python3 -m json.tool > /tmp/failed_payload.json
  head -100 /tmp/failed_payload.json
  
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  ❌ TEST ÉCHOUÉ - Voir erreurs ci-dessus"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  exit 1
else
  echo "   ❌ ERREUR HTTP $HTTP_CODE"
  echo "$BODY"
  exit 1
fi

