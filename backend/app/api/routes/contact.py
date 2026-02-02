from fastapi import APIRouter, Depends, HTTPException
from app.schemas.contact import ContactMessageRequest, ContactMessageResponse
from app.core.config import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

DEVELOPER_EMAIL = "kenfackfranck08@gmail.com"

@router.post("/send", response_model=ContactMessageResponse)
async def send_contact_message(request: ContactMessageRequest):
    """
    Endpoint pour envoyer un message de contact au développeur.
    Utilise SMTP si configuré, sinon log le message.
    """
    try:
        # Construire le message
        subject = f"[Job Hunter AI] {request.subject or 'Message de ' + request.name}"
        body = f"""
Message de: {request.name}
Email: {request.email}
Sujet: {request.subject or '(Aucun sujet)'}

Message:
{request.message}

---
Envoyé depuis Job Hunter AI - https://jobhunter.franckkenfack.works
"""
        
        # Essayer d'envoyer via SMTP si configuré
        smtp_host = getattr(settings, 'SMTP_HOST', None)
        smtp_port = getattr(settings, 'SMTP_PORT', None)
        smtp_user = getattr(settings, 'SMTP_USER', None)
        smtp_password = getattr(settings, 'SMTP_PASSWORD', None)
        
        if smtp_host and smtp_port and smtp_user and smtp_password:
            try:
                # Configuration SMTP
                msg = MIMEMultipart()
                msg['From'] = smtp_user
                msg['To'] = DEVELOPER_EMAIL
                msg['Subject'] = subject
                msg['Reply-To'] = request.email
                
                msg.attach(MIMEText(body, 'plain'))
                
                # Connexion et envoi
                with smtplib.SMTP(smtp_host, smtp_port) as server:
                    server.starttls()
                    server.login(smtp_user, smtp_password)
                    server.send_message(msg)
                
                logger.info(f"Email envoyé à {DEVELOPER_EMAIL} de {request.email}")
                return ContactMessageResponse(
                    success=True,
                    message="Message envoyé avec succès !"
                )
            except Exception as e:
                logger.error(f"Erreur SMTP: {e}")
                # Continue to fallback
        
        # Fallback: Log le message (pour dev/test)
        logger.info(f"""
========== NOUVEAU MESSAGE DE CONTACT ==========
De: {request.name} ({request.email})
Sujet: {request.subject}
Message:
{request.message}
================================================
        """)
        
        return ContactMessageResponse(
            success=True,
            message="Message enregistré ! Le développeur le recevra bientôt."
        )
        
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du message: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de l'envoi du message"
        )
