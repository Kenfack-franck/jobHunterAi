"""
Dependency pour vérifier que l'utilisateur est admin
"""
from fastapi import HTTPException, status, Depends

from app.models.user import User
from app.core.dependencies import get_current_user


def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Vérifie que l'utilisateur courant est un administrateur.
    Lève une exception 403 Forbidden si ce n'est pas le cas.
    
    Args:
        current_user: Utilisateur authentifié (via get_current_user)
    
    Returns:
        User si admin
    
    Raises:
        HTTPException 403 si pas admin
    """
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux administrateurs"
        )
    
    return current_user
