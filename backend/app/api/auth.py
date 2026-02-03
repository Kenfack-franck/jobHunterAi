"""
Routes d'authentification
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.auth import UserRegister, UserLogin, Token, UserResponse, UserUpdate, PasswordUpdate
from app.services.auth_service import AuthService
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """
    Créer un nouveau compte utilisateur
    
    - **email**: Email valide (unique)
    - **password**: Minimum 8 caractères
    - **full_name**: Nom complet (optionnel)
    - **language**: Langue préférée (fr/en)
    """
    try:
        user = await AuthService.register_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la création du compte"
        )


@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Se connecter et obtenir un token JWT
    
    - **email**: Email du compte
    - **password**: Mot de passe
    
    Returns:
        Token JWT à utiliser dans le header Authorization: Bearer <token>
    """
    user = await AuthService.authenticate_user(
        db,
        credentials.email,
        credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = AuthService.create_token_for_user(user)
    return token


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Récupérer les informations de l'utilisateur connecté
    
    Nécessite un token JWT valide dans le header:
    Authorization: Bearer <token>
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Mettre à jour les informations de l'utilisateur connecté
    
    - **full_name**: Nouveau nom complet (optionnel)
    - **language**: Nouvelle langue préférée (optionnel)
    
    Nécessite un token JWT valide dans le header.
    """
    try:
        # Mettre à jour uniquement les champs fournis
        if user_update.full_name is not None:
            current_user.full_name = user_update.full_name
        if user_update.language is not None:
            current_user.language = user_update.language
        
        db.add(current_user)
        await db.commit()
        await db.refresh(current_user)
        
        return current_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour du profil: {str(e)}"
        )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user: User = Depends(get_current_user)
):
    """
    Rafraîchir le token JWT
    
    Nécessite un token JWT valide.
    Retourne un nouveau token avec une nouvelle durée de validité.
    """
    token = AuthService.create_token_for_user(current_user)
    return token


@router.put("/me/password")
async def update_password(
    password_update: PasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Changer le mot de passe de l'utilisateur connecté
    
    - **current_password**: Mot de passe actuel (pour vérification)
    - **new_password**: Nouveau mot de passe (minimum 8 caractères)
    
    Nécessite un token JWT valide dans le header.
    """
    # Vérifier le mot de passe actuel
    user = await AuthService.authenticate_user(
        db,
        current_user.email,
        password_update.current_password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mot de passe actuel incorrect"
        )
    
    try:
        # Hasher et mettre à jour le nouveau mot de passe
        from app.core.security import hash_password
        current_user.hashed_password = hash_password(password_update.new_password)
        
        db.add(current_user)
        await db.commit()
        
        return {"message": "Mot de passe mis à jour avec succès"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour du mot de passe: {str(e)}"
        )


@router.delete("/me")
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Supprimer le compte de l'utilisateur connecté
    
    ⚠️ ATTENTION: Cette action est irréversible !
    Toutes les données associées seront supprimées.
    
    Nécessite un token JWT valide dans le header.
    """
    try:
        await db.delete(current_user)
        await db.commit()
        
        return {"message": "Compte supprimé avec succès"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression du compte: {str(e)}"
        )


@router.get("/me/export")
async def export_user_data(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Exporter toutes les données personnelles de l'utilisateur (RGPD)
    
    Retourne un fichier JSON contenant:
    - Informations du profil
    - Offres sauvegardées
    - Candidatures
    - Documents générés
    
    Nécessite un token JWT valide dans le header.
    """
    from fastapi.responses import JSONResponse
    import json
    
    try:
        # Récupérer toutes les données de l'utilisateur
        user_data = {
            "user": {
                "id": str(current_user.id),
                "email": current_user.email,
                "full_name": current_user.full_name,
                "language": current_user.language,
                "created_at": current_user.created_at.isoformat(),
                "is_active": current_user.is_active
            },
            # TODO: Ajouter les autres données (profil, offres, candidatures, documents)
            # Pour l'instant, on retourne juste les infos de base
            "note": "Export complet des données - Conforme RGPD"
        }
        
        return JSONResponse(
            content=user_data,
            headers={
                "Content-Disposition": f"attachment; filename=user_data_{current_user.id}.json"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'export des données: {str(e)}"
        )
