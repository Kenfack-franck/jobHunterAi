#!/bin/bash
# Capturer la réponse détaillée du 422

# Utiliser un utilisateur existant (créé dans votre test)
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password123" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)

if [ -z "$TOKEN" ]; then
  echo "❌ Login failed, trying another user"
  # Créer un nouveau
  EMAIL="debug_$(date +%s)@test.com"
  curl -s -X POST "http://localhost:8000/api/v1/auth/register" \
    -H "Content-Type: application/json" \
    -d '{
      "email": "'$EMAIL'",
      "password": "Test123!",
      "full_name": "Debug User"
    }' > /dev/null
    
  TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=$EMAIL&password=Test123!" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)
fi

echo "Token: ${TOKEN:0:50}..."

# Tester avec des données minimales
echo ""
echo "Test 1: Profil minimal (devrait marcher)"
RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/profile" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Test Developer"
  }')

if echo "$RESPONSE" | grep -q '"id"'; then
  echo "✅ Profil minimal créé"
else
  echo "❌ Erreur profil minimal:"
  echo "$RESPONSE" | python3 -m json.tool
fi
