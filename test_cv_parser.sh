#!/bin/bash
# Script pour tester le CV parser

echo "🧪 Test du CV Parser"
echo "===================="
echo ""

# Vérifier que le backend est accessible
echo "1️⃣ Vérification du backend..."
curl -s http://localhost:8000/health > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Backend accessible"
else
    echo "❌ Backend non accessible"
    exit 1
fi

echo ""
echo "2️⃣ Pour tester l'upload de CV:"
echo "   1. Créer un nouveau compte (ou utiliser existant)"
echo "   2. Aller sur http://localhost:3000/profile/create"
echo "   3. Choisir 'Import automatique'"
echo "   4. Upload un CV PDF"
echo ""
echo "3️⃣ Test avec curl (si vous avez un fichier test.pdf):"
echo ""
echo "   TOKEN='votre_token_jwt'"
echo "   curl -X POST http://localhost:8000/api/v1/profile/parse-cv \\"
echo "        -H 'Authorization: Bearer \$TOKEN' \\"
echo "        -F 'file=@/chemin/vers/cv.pdf'"
echo ""
echo "4️⃣ Pour clear le localStorage et revoir l'onboarding:"
echo "   - Ouvrir DevTools (F12)"
echo "   - Console → localStorage.clear()"
echo "   - Rafraîchir la page"
echo ""
echo "✅ Services en cours d'exécution:"
docker compose ps | grep -E "(backend|frontend)" | awk '{print $1, $7}'
