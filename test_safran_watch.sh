#!/bin/bash

echo "🔐 Login..."
LOGIN_RESP=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=safran_test@test.com&password=Test1234!")

TOKEN=$(echo "$LOGIN_RESP" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)

if [ -z "$TOKEN" ]; then
  echo "❌ Erreur login. Création compte..."
  curl -s -X POST http://localhost:8000/api/v1/auth/register \
    -H "Content-Type: application/json" \
    -d '{"email":"safran_test@test.com","password":"Test1234!","full_name":"Test Safran"}' | jq '.'
  
  LOGIN_RESP=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=safran_test@test.com&password=Test1234!")
  TOKEN=$(echo "$LOGIN_RESP" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
fi

echo "✅ Token: ${TOKEN:0:30}..."
echo ""

echo "🔍 Test ajout Safran..."
curl -s -X POST http://localhost:8000/api/v1/watch/company \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"company_name":"Safran","careers_url":"https://www.safran-group.com/fr/offres"}' | jq '.'

echo ""
echo "📋 Liste veilles:"
curl -s http://localhost:8000/api/v1/watch/companies \
  -H "Authorization: Bearer $TOKEN" | jq '.watches[] | {company: .company_name, offers: .total_offers_found, last_scraped: .last_scraped_at}'

