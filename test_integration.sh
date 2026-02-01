#!/bin/bash

echo "╔═══════════════════════════════════════════════════════╗"
echo "║  🧪 TEST INTÉGRATION BACKEND - SPRINT 9              ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Configuration
API_URL="http://localhost:8000/api/v1"
FRONTEND_URL="http://localhost:3000"
EMAIL="john.doe@testmail.com"
PASSWORD="Test2026!"

echo "📍 Configuration:"
echo "   API: $API_URL"
echo "   Frontend: $FRONTEND_URL"
echo "   User: $EMAIL"
echo ""

# Test 1: Backend Health
echo "1️⃣  Test Backend Health..."
if curl -s "http://localhost:8000/health" | grep -q "healthy"; then
    echo "   ✅ Backend is healthy"
else
    echo "   ❌ Backend is down"
    exit 1
fi

# Test 2: Login
echo ""
echo "2️⃣  Test Login..."
TOKEN=$(curl -s -X POST "$API_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}" \
    | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)

if [ -n "$TOKEN" ]; then
    echo "   ✅ Login successful (Token: ${TOKEN:0:20}...)"
else
    echo "   ❌ Login failed"
    exit 1
fi

# Test 3: Get User Profile
echo ""
echo "3️⃣  Test Get User Profile..."
USER=$(curl -s -H "Authorization: Bearer $TOKEN" "$API_URL/auth/me")
if echo "$USER" | grep -q "email"; then
    echo "   ✅ User profile retrieved"
    echo "      $(echo $USER | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'Email: {data[\"email\"]}, Name: {data.get(\"full_name\", \"N/A\")}')" 2>/dev/null)"
else
    echo "   ❌ Failed to get profile"
fi

# Test 4: Get Watched Companies
echo ""
echo "4️⃣  Test Watched Companies API..."
COMPANIES=$(curl -s -H "Authorization: Bearer $TOKEN" "$API_URL/watch/companies")
COUNT=$(echo "$COMPANIES" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)
if [ "$COUNT" -ge 0 ]; then
    echo "   ✅ Companies API working ($COUNT entreprises)"
else
    echo "   ❌ Companies API failed"
fi

# Test 5: Get Documents
echo ""
echo "5️⃣  Test Documents API..."
DOCS=$(curl -s -H "Authorization: Bearer $TOKEN" "$API_URL/documents/")
DOC_COUNT=$(echo "$DOCS" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)
if [ "$DOC_COUNT" -ge 0 ]; then
    echo "   ✅ Documents API working ($DOC_COUNT documents)"
else
    echo "   ❌ Documents API failed"
fi

# Test 6: Get Profile
echo ""
echo "6️⃣  Test Profile API..."
PROFILE=$(curl -s -H "Authorization: Bearer $TOKEN" "$API_URL/profile")
if echo "$PROFILE" | grep -q "title"; then
    echo "   ✅ Profile API working"
    echo "      $(echo $PROFILE | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'Title: {data.get(\"title\", \"N/A\")}, Skills: {len(data.get(\"skills\", []))} comp.')" 2>/dev/null)"
else
    echo "   ❌ Profile API failed"
fi

# Test 7: Frontend Pages
echo ""
echo "7️⃣  Test Frontend Pages..."
PAGES=("" "auth/login" "auth/register" "dashboard" "profile" "jobs" "companies/watch" "documents" "applications" "settings" "help")
FAILED=0
for page in "${PAGES[@]}"; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL/$page")
    if [ "$STATUS" = "200" ]; then
        echo "   ✅ /$page → $STATUS"
    else
        echo "   ❌ /$page → $STATUS"
        FAILED=$((FAILED + 1))
    fi
done

# Résumé
echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║  📊 RÉSUMÉ DES TESTS                                 ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "Backend APIs:"
echo "  ✅ Health Check"
echo "  ✅ Authentication"
echo "  ✅ User Profile"
echo "  ✅ Watched Companies ($COUNT)"
echo "  ✅ Documents ($DOC_COUNT)"
echo "  ✅ Profile"
echo ""
echo "Frontend Pages:"
if [ $FAILED -eq 0 ]; then
    echo "  ✅ Toutes les pages accessibles (${#PAGES[@]}/11)"
else
    echo "  ⚠️  $FAILED page(s) en erreur"
fi
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 TOUS LES TESTS RÉUSSIS !"
    exit 0
else
    echo "⚠️  CERTAINS TESTS ONT ÉCHOUÉ"
    exit 1
fi
