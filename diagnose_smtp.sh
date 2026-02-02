#!/bin/bash
# Script de diagnostic pour vérifier la configuration SMTP

echo "🔍 Diagnostic configuration SMTP - Job Hunter AI"
echo "================================================"
echo ""

# 1. Vérifier si les variables existent dans .env
echo "1️⃣ Variables dans le fichier .env:"
echo "-----------------------------------"
if [ -f .env ]; then
    echo "✅ Fichier .env trouvé"
    grep -E "SMTP_" .env | sed 's/SMTP_PASSWORD=.*/SMTP_PASSWORD=***MASQUÉ***/'
else
    echo "❌ Fichier .env non trouvé"
fi
echo ""

# 2. Vérifier dans le conteneur backend
echo "2️⃣ Variables dans le conteneur backend:"
echo "----------------------------------------"
docker compose -f docker-compose.prod.yml exec -T backend printenv | grep SMTP | sed 's/SMTP_PASSWORD=.*/SMTP_PASSWORD=***MASQUÉ***/' || echo "❌ Aucune variable SMTP trouvée dans le conteneur"
echo ""

# 3. Vérifier si le backend tourne
echo "3️⃣ État du conteneur backend:"
echo "------------------------------"
docker compose -f docker-compose.prod.yml ps backend
echo ""

# 4. Tester la connexion SMTP depuis le conteneur
echo "4️⃣ Test de connexion SMTP:"
echo "---------------------------"
cat > /tmp/test_smtp.py << 'EOF'
import os
import smtplib

smtp_host = os.getenv('SMTP_HOST')
smtp_port = int(os.getenv('SMTP_PORT', 587))
smtp_user = os.getenv('SMTP_USER')
smtp_password = os.getenv('SMTP_PASSWORD')

print(f"SMTP_HOST: {smtp_host}")
print(f"SMTP_PORT: {smtp_port}")
print(f"SMTP_USER: {smtp_user}")
print(f"SMTP_PASSWORD: {'***' if smtp_password else 'NON DÉFINI'}")
print()

if all([smtp_host, smtp_port, smtp_user, smtp_password]):
    try:
        print(f"🔌 Connexion à {smtp_host}:{smtp_port}...")
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
        print("✅ Connexion établie")
        
        print("🔒 Démarrage TLS...")
        server.starttls()
        print("✅ TLS activé")
        
        print("🔑 Authentification...")
        server.login(smtp_user, smtp_password)
        print("✅ Authentification réussie")
        
        server.quit()
        print()
        print("🎉 Configuration SMTP VALIDE !")
    except Exception as e:
        print(f"❌ ERREUR: {e}")
else:
    print("❌ Configuration SMTP incomplète")
    if not smtp_host: print("   - SMTP_HOST manquant")
    if not smtp_port: print("   - SMTP_PORT manquant")
    if not smtp_user: print("   - SMTP_USER manquant")
    if not smtp_password: print("   - SMTP_PASSWORD manquant")
EOF

docker compose -f docker-compose.prod.yml exec -T backend python /tmp/test_smtp.py 2>&1 || echo "❌ Impossible d'exécuter le test"
echo ""

# 5. Derniers logs du backend
echo "5️⃣ Derniers logs backend (SMTP/EMAIL):"
echo "---------------------------------------"
docker compose -f docker-compose.prod.yml logs backend --tail 50 | grep -i -E "(smtp|email|mail)" || echo "Aucun log SMTP trouvé"
echo ""

echo "================================================"
echo "✅ Diagnostic terminé"
echo ""
echo "💡 Actions suggérées:"
echo "   1. Si les variables manquent dans le conteneur → Redémarrer: docker compose -f docker-compose.prod.yml restart backend"
echo "   2. Si erreur d'authentification → Vérifier le mot de passe d'application Gmail"
echo "   3. Si timeout → Vérifier firewall/port 587 ouvert"
