#!/bin/bash

echo "🔧 Force New Admin Login"
echo "======================="
echo ""

# Get new token
echo "1️⃣  Getting new token..."
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"kenfackfranck08@gmail.com","password":"noumedem"}' | jq -r '.access_token')

if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
    echo "❌ Failed to get token"
    exit 1
fi

echo "✅ Token obtained"
echo ""

# Decode token
echo "2️⃣  Token payload:"
echo "$TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null | jq .
echo ""

# Test admin endpoint
echo "3️⃣  Testing admin stats endpoint..."
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" http://localhost:8000/api/v1/admin/stats \
  -H "Authorization: Bearer $TOKEN")

HTTP_STATUS=$(echo "$RESPONSE" | grep "HTTP_STATUS:" | cut -d: -f2)
BODY=$(echo "$RESPONSE" | sed '/HTTP_STATUS:/d')

if [ "$HTTP_STATUS" = "200" ]; then
    echo "✅ Admin endpoint works! (HTTP $HTTP_STATUS)"
    echo ""
    echo "📊 Stats:"
    echo "$BODY" | jq .
    echo ""
    echo "=========================================="
    echo "✅ Backend is working correctly!"
    echo ""
    echo "📝 To fix the frontend:"
    echo "   1. Open browser console (F12)"
    echo "   2. Run: localStorage.clear()"
    echo "   3. Reload page and login again"
    echo "=========================================="
else
    echo "❌ Admin endpoint failed (HTTP $HTTP_STATUS)"
    echo "Response: $BODY"
fi
