# Configuration SMTP pour l'envoi d'emails

## 📧 Pourquoi configurer SMTP ?

Actuellement, l'application **log les messages** dans les logs Docker sans les envoyer réellement. Pour que les emails (suggestions, alertes de veille) soient envoyés, vous devez configurer SMTP.

## 🔧 Options SMTP recommandées

### Option 1 : Gmail (Gratuit, facile)

1. **Créer un mot de passe d'application Gmail** :
   - Aller sur https://myaccount.google.com/security
   - Activer la validation en 2 étapes
   - Créer un "Mot de passe d'application"

2. **Ajouter dans `.env.prod`** :
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=kenfackfranck08@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx  # Mot de passe d'application
SMTP_FROM_EMAIL=kenfackfranck08@gmail.com
SMTP_FROM_NAME=Job Hunter AI
```

### Option 2 : SendGrid (500 emails/jour gratuits)

1. **Créer un compte** : https://sendgrid.com/
2. **Obtenir une API Key**
3. **Configuration** :
```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG.xxxxxxxxxxxxx  # Votre API key
SMTP_FROM_EMAIL=kenfackfranck08@gmail.com
SMTP_FROM_NAME=Job Hunter AI
```

### Option 3 : Brevo (ex-Sendinblue) (300 emails/jour gratuits)

1. **Créer un compte** : https://www.brevo.com/
2. **Obtenir SMTP credentials**
3. **Configuration** :
```bash
SMTP_HOST=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=votre-email@exemple.com
SMTP_PASSWORD=xxxxxxxxxxx
SMTP_FROM_EMAIL=kenfackfranck08@gmail.com
SMTP_FROM_NAME=Job Hunter AI
```

### Option 4 : Mailgun (100 emails/jour gratuits)

1. **Créer un compte** : https://www.mailgun.com/
2. **Configuration** :
```bash
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USER=postmaster@votre-domaine.mailgun.org
SMTP_PASSWORD=xxxxxxxxxxxxx
SMTP_FROM_EMAIL=kenfackfranck08@gmail.com
SMTP_FROM_NAME=Job Hunter AI
```

## 🚀 Déploiement avec SMTP

### Sur le VPS

1. **Éditer `.env.prod`** :
```bash
ssh ubuntu@vps-c7c7eb59
cd ~/jobhunter
nano .env  # ou vim .env
```

2. **Ajouter les variables SMTP** (voir options ci-dessus)

3. **Redémarrer le backend** :
```bash
docker compose -f docker-compose.prod.yml restart backend
```

4. **Tester** :
- Aller sur https://jobhunter.franckkenfack.works/contact
- Envoyer un message de test
- Vérifier votre boîte mail kenfackfranck08@gmail.com

## 🧪 Test sans SMTP

Si SMTP n'est **pas configuré**, l'application fonctionne quand même :
- Les messages sont **loggés** dans les logs Docker
- Vous les verrez avec : `docker compose -f docker-compose.prod.yml logs backend | grep "NOUVEAU MESSAGE"`

## 📊 Ce qui sera envoyé par email

Une fois SMTP configuré, vous recevrez des emails pour :

1. **Messages de contact** (`/contact`) :
   - De : utilisateur
   - À : kenfackfranck08@gmail.com
   - Contenu : Nom, email, sujet, message

2. **Alertes de veille d'entreprise** (future fonctionnalité) :
   - Quand une offre avec score élevé est trouvée
   - Notification automatique par Celery

## 🔒 Sécurité

- ⚠️ **Ne jamais commiter** `.env` ou `.env.prod` dans Git
- ✅ Les mots de passe SMTP sont déjà dans `.gitignore`
- 🔐 Utiliser des "App Passwords" plutôt que vos vrais mots de passe

## 💡 Recommandation

Pour commencer, je recommande **Gmail** car :
- ✅ Gratuit
- ✅ Vous avez déjà un compte
- ✅ Facile à configurer (5 minutes)
- ✅ Fiable

**Limite** : Gmail limite à ~500 emails/jour, largement suffisant pour votre usage.

---

## 🎯 Résumé rapide

**Sans SMTP** : Messages loggés (mode actuel) ✅  
**Avec SMTP** : Emails réellement envoyés à kenfackfranck08@gmail.com 📧

**Action minimale** : Rien à faire ! L'app fonctionne déjà sans SMTP.  
**Action recommandée** : Configurer Gmail SMTP en 5 minutes pour recevoir les emails.
