"""
Routes d'authentification
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.auth import UserRegister, UserLogin, Token, UserResponse
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
