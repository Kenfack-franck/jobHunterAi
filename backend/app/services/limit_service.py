"""
Service de gestion des limites d'utilisation
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, datetime
from typing import Optional, Tuple, Dict
import uuid

from app.models.user_limits import UserLimits, DEFAULT_LIMITS
from app.models.user import User
from app.services.email_service import send_email


class LimitService:
    """Service pour gérer les limites d'utilisation des utilisateurs"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_or_create_limits(self, user_id: uuid.UUID) -> UserLimits:
        """
        Récupère ou crée les limites pour un utilisateur.
        Les limites sont créées automatiquement à la première utilisation.
        """
        limits = self.db.query(UserLimits).filter(
            UserLimits.user_id == user_id
        ).first()
        
        if not limits:
            limits = UserLimits(
                id=uuid.uuid4(),
                user_id=user_id
            )
            self.db.add(limits)
            self.db.commit()
            self.db.refresh(limits)
        
        return limits
    
    def check_limit(self, user_id: uuid.UUID, limit_type: str) -> Tuple[bool, int, int]:
        """
        Vérifie si l'utilisateur peut encore faire une action.
        
        Args:
            user_id: ID de l'utilisateur
            limit_type: Type de limite à vérifier (ex: 'saved_offers', 'searches_today')
        
        Returns:
            Tuple (can_proceed: bool, current: int, max_limit: int)
        """
        limits = self.get_or_create_limits(user_id)
        
        # Reset daily counters if needed
        limits.reset_daily_if_needed()
        self.db.commit()
        
        # Get current count and limit
        current = limits.get_current(limit_type)
        max_limit = limits.get_limit(limit_type)
        
        can_proceed = current < max_limit
        
        return can_proceed, current, max_limit
    
    def increment(self, user_id: uuid.UUID, limit_type: str) -> None:
        """
        Incrémente le compteur après une action réussie.
        
        Args:
            user_id: ID de l'utilisateur
            limit_type: Type de limite à incrémenter
        """
        limits = self.get_or_create_limits(user_id)
        
        # Increment the appropriate counter
        counter_field = f"{limit_type}_count"
        current_value = getattr(limits, counter_field, 0)
        setattr(limits, counter_field, current_value + 1)
        
        # Update metadata for daily limits
        today = date.today()
        if limit_type == 'searches_today':
            limits.last_search_date = today
        elif limit_type == 'generated_cv_today':
            limits.last_cv_generation_date = today
        
        limits.updated_at = datetime.now()
        self.db.commit()
        
        # Check if we need to send alerts
        self.check_and_send_alerts(user_id, limit_type)
    
    def decrement(self, user_id: uuid.UUID, limit_type: str) -> None:
        """
        Décrémente le compteur (ex: quand un utilisateur supprime une offre sauvegardée).
        
        Args:
            user_id: ID de l'utilisateur
            limit_type: Type de limite à décrémenter
        """
        limits = self.get_or_create_limits(user_id)
        
        counter_field = f"{limit_type}_count"
        current_value = getattr(limits, counter_field, 0)
        
        # Don't go below 0
        if current_value > 0:
            setattr(limits, counter_field, current_value - 1)
            limits.updated_at = datetime.now()
            self.db.commit()
    
    def check_and_send_alerts(self, user_id: uuid.UUID, limit_type: str) -> None:
        """
        Vérifie si des alertes doivent être envoyées à l'admin.
        Envoie un email si l'utilisateur atteint 90% ou 100% d'une limite.
        
        Args:
            user_id: ID de l'utilisateur
            limit_type: Type de limite à vérifier
        """
        limits = self.get_or_create_limits(user_id)
        
        current = limits.get_current(limit_type)
        max_limit = limits.get_limit(limit_type)
        
        if max_limit == 0:
            return
        
        percentage = (current / max_limit) * 100
        
        # Send alert if 90% or 100%
        if percentage >= 90:
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                self._send_admin_alert(user, limit_type, percentage, current, max_limit)
    
    def _send_admin_alert(
        self, 
        user: User, 
        limit_type: str, 
        percentage: float, 
        current: int, 
        max_limit: int
    ) -> None:
        """
        Envoie un email d'alerte aux administrateurs.
        
        Args:
            user: Utilisateur concerné
            limit_type: Type de limite
            percentage: Pourcentage d'utilisation
            current: Valeur actuelle
            max_limit: Limite maximale
        """
        # Get all admin users
        admins = self.db.query(User).filter(User.role == 'admin').all()
        
        if not admins:
            return
        
        # Format limit type for display
        limit_names = {
            'saved_offers': 'Offres sauvegardées',
            'searches_today': 'Recherches aujourd\'hui',
            'profiles': 'Profils',
            'applications': 'Candidatures',
            'cv_parsed': 'CV parsés',
            'watched_companies': 'Entreprises surveillées',
            'generated_cv_today': 'CV générés aujourd\'hui'
        }
        
        limit_display = limit_names.get(limit_type, limit_type)
        
        # Determine urgency
        if percentage >= 100:
            subject = f"🚨 LIMITE ATTEINTE - {user.email}"
            urgency = "BLOQUÉ"
            color = "red"
        else:
            subject = f"⚠️ Limite proche - {user.email}"
            urgency = "ATTENTION"
            color = "orange"
        
        # Email body
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="background-color: #{color}; color: white; padding: 20px; border-radius: 10px;">
                <h2>{urgency}</h2>
                <p>L'utilisateur <strong>{user.email}</strong> a atteint <strong>{percentage:.0f}%</strong> de sa limite.</p>
            </div>
            
            <div style="margin-top: 20px; padding: 20px; border: 2px solid #{color}; border-radius: 10px;">
                <h3>Détails</h3>
                <ul>
                    <li><strong>Email:</strong> {user.email}</li>
                    <li><strong>Nom:</strong> {user.full_name or 'N/A'}</li>
                    <li><strong>Limite:</strong> {limit_display}</li>
                    <li><strong>Utilisation:</strong> {current}/{max_limit} ({percentage:.0f}%)</li>
                    <li><strong>Inscrit depuis:</strong> {user.created_at.strftime('%d/%m/%Y')}</li>
                </ul>
            </div>
            
            <div style="margin-top: 20px; padding: 15px; background-color: #f0f0f0; border-radius: 5px;">
                <h4>Actions suggérées :</h4>
                <ol>
                    <li>Contacter l'utilisateur pour proposer un plan PRO</li>
                    <li>Augmenter ses limites manuellement</li>
                    <li>Surveiller son activité</li>
                    <li>Le bloquer si abus détecté</li>
                </ol>
                
                <p style="margin-top: 15px;">
                    <a href="http://localhost:3000/admin/users?email={user.email}" 
                       style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                        Voir l'utilisateur dans le panel admin
                    </a>
                </p>
            </div>
            
            <p style="margin-top: 20px; color: #888; font-size: 12px;">
                Job Hunter AI - Notifications Admin
            </p>
        </body>
        </html>
        """
        
        # Send to all admins
        for admin in admins:
            try:
                send_email(
                    to_email=admin.email,
                    subject=subject,
                    body=body
                )
            except Exception as e:
                print(f"Erreur envoi email admin: {e}")
    
    def get_user_usage_stats(self, user_id: uuid.UUID) -> Dict[str, Dict[str, int]]:
        """
        Récupère toutes les statistiques d'utilisation pour un utilisateur.
        
        Args:
            user_id: ID de l'utilisateur
        
        Returns:
            Dict avec les stats de chaque limite
        """
        limits = self.get_or_create_limits(user_id)
        
        # Reset daily counters if needed
        limits.reset_daily_if_needed()
        self.db.commit()
        
        stats = {}
        
        limit_types = [
            'saved_offers',
            'searches_today',
            'profiles',
            'applications',
            'cv_parsed',
            'watched_companies',
            'generated_cv_today'
        ]
        
        for limit_type in limit_types:
            current = limits.get_current(limit_type)
            max_limit = limits.get_limit(limit_type)
            percentage = int((current / max_limit * 100)) if max_limit > 0 else 0
            
            stats[limit_type] = {
                'current': current,
                'limit': max_limit,
                'percentage': percentage
            }
        
        return stats
    
    def update_custom_limits(
        self, 
        user_id: uuid.UUID, 
        custom_limits: Dict[str, int],
        reason: Optional[str] = None
    ) -> UserLimits:
        """
        Met à jour les limites personnalisées d'un utilisateur.
        Utilisé par les admins pour augmenter les limites.
        
        Args:
            user_id: ID de l'utilisateur
            custom_limits: Dict avec les nouvelles limites (ex: {'max_saved_offers': 100})
            reason: Raison de la modification (pour logs)
        
        Returns:
            UserLimits mis à jour
        """
        limits = self.get_or_create_limits(user_id)
        
        # Update provided limits
        for key, value in custom_limits.items():
            if hasattr(limits, key) and key.startswith('max_'):
                setattr(limits, key, value)
        
        limits.updated_at = datetime.now()
        self.db.commit()
        self.db.refresh(limits)
        
        # TODO: Log this action with reason in admin logs table (future feature)
        
        return limits


def get_limit_service(db: Session) -> LimitService:
    """Factory function pour obtenir une instance de LimitService"""
    return LimitService(db)
