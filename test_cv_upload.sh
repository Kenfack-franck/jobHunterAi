#!/bin/bash
# Test complet du CV Parser avec le CV de Franck

set -e

echo "🧪 Test CV Parser avec CV_kenfack_franck.pdf"
echo "=============================================="
echo ""

# Vérifier que le fichier existe
CV_FILE="CV_kenfack_franck.pdf"
if [ ! -f "$CV_FILE" ]; then
    echo "❌ Fichier $CV_FILE non trouvé"
    exit 1
fi
echo "✅ Fichier CV trouvé: $CV_FILE"

# Vérifier que le backend est accessible
echo ""
echo "🔍 Vérification du backend..."
curl -s http://localhost:8000/health > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Backend accessible"
else
    echo "❌ Backend non accessible"
    exit 1
fi

# Créer/Login un utilisateur de test
echo ""
echo "🔐 Connexion utilisateur test..."

# Essayer de se connecter avec un utilisateur existant
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test.cvparser@example.com",
    "password": "TestPassword123!"
  }')

# Vérifier si la connexion a réussi
TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "👤 Utilisateur n'existe pas, création..."
    
    # Créer l'utilisateur
    REGISTER_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/register \
      -H "Content-Type: application/json" \
      -d '{
        "email": "test.cvparser@example.com",
        "password": "TestPassword123!",
        "full_name": "Test CV Parser"
      }')
    
    echo "✅ Utilisateur créé"
    
    # Se connecter maintenant
    LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
      -H "Content-Type: application/json" \
      -d '{
        "email": "test.cvparser@example.com",
        "password": "TestPassword123!"
      }')
    
    # Récupérer le token
    TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
    
    if [ -z "$TOKEN" ]; then
        echo "❌ Impossible de récupérer le token"
        echo "Login Response: $LOGIN_RESPONSE"
        exit 1
    fi
fi

echo "✅ Token obtenu: ${TOKEN:0:20}..."

# Tester l'upload du CV
echo ""
echo "📤 Upload du CV vers /api/v1/profile/parse-cv..."
echo ""

PARSE_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/profile/parse-cv \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@$CV_FILE" \
  -w "\nHTTP_CODE:%{http_code}")

HTTP_CODE=$(echo "$PARSE_RESPONSE" | grep "HTTP_CODE" | cut -d: -f2)
RESPONSE_BODY=$(echo "$PARSE_RESPONSE" | sed '/HTTP_CODE/d')

echo "📊 Code HTTP: $HTTP_CODE"
echo ""

if [ "$HTTP_CODE" == "200" ]; then
    echo "✅ SUCCESS! CV parsé avec succès"
    echo ""
    echo "📋 Données extraites:"
    echo "$RESPONSE_BODY" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE_BODY"
else
    echo "❌ ERREUR lors du parsing"
    echo ""
    echo "Réponse:"
    echo "$RESPONSE_BODY"
    echo ""
    echo "Logs backend:"
    docker compose logs backend --tail 30 | grep -E "parse-cv|Error|Traceback" || docker compose logs backend --tail 10
fi

echo ""
echo "=============================================="
echo "Test terminé"
