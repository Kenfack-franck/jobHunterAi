"""
Service d'envoi d'emails via SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from app.config import settings

logger = logging.getLogger(__name__)

DEVELOPER_EMAIL = "kenfackfranck08@gmail.com"


async def send_email(
    to_email: str,
    subject: str,
    body_text: str,
    body_html: str = None,
    reply_to: str = None
) -> bool:
    """
    Envoie un email via SMTP si configuré.
    
    Args:
        to_email: Email du destinataire
        subject: Sujet de l'email
        body_text: Corps en texte brut
        body_html: Corps en HTML (optionnel)
        reply_to: Email pour la réponse (optionnel)
    
    Returns:
        True si envoyé avec succès, False sinon
    """
    try:
        smtp_host = getattr(settings, 'SMTP_HOST', None)
        smtp_port = getattr(settings, 'SMTP_PORT', None)
        smtp_user = getattr(settings, 'SMTP_USER', None)
        smtp_password = getattr(settings, 'SMTP_PASSWORD', None)
        
        if not all([smtp_host, smtp_port, smtp_user, smtp_password]):
            logger.warning("Configuration SMTP incomplète, email non envoyé")
            logger.info(f"Email à {to_email}: {subject}")
            logger.info(f"Corps:\n{body_text}")
            return False
        
        # Construction du message
        msg = MIMEMultipart('alternative')
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject
        
        if reply_to:
            msg['Reply-To'] = reply_to
        
        # Ajouter le corps en texte brut
        msg.attach(MIMEText(body_text, 'plain'))
        
        # Ajouter le corps en HTML si fourni
        if body_html:
            msg.attach(MIMEText(body_html, 'html'))
        
        # Connexion et envoi
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        logger.info(f"Email envoyé avec succès à {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email à {to_email}: {e}")
        return False
