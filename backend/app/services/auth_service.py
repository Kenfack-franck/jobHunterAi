"""
Service d'authentification
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
from typing import Optional

from app.models.user import User
from app.schemas.auth import UserRegister, Token
from app.core.security import hash_password, verify_password, create_access_token
from app.config import settings


class AuthService:
    """Service pour gérer l'authentification"""
    
    @staticmethod
    async def register_user(db: AsyncSession, user_data: UserRegister) -> User:
        """
        Créer un nouveau compte utilisateur
        
        Args:
            db: Session de base de données
            user_data: Données d'inscription
            
        Returns:
            User: L'utilisateur créé
            
        Raises:
            ValueError: Si l'email existe déjà
        """
        # Vérifier si l'email existe déjà
        result = await db.execute(
            select(User).filter(User.email == user_data.email)
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise ValueError("Un compte avec cet email existe déjà")
        
        # Créer le nouvel utilisateur
        hashed_pwd = hash_password(user_data.password)
        
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_pwd,
            full_name=user_data.full_name,
            language=user_data.language,
            is_active=True
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        return new_user
    
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
        """
        Authentifier un utilisateur
        
        Args:
            db: Session de base de données
            email: Email de l'utilisateur
            password: Mot de passe en clair
            
        Returns:
            User si authentification réussie, None sinon
        """
        # Récupérer l'utilisateur
        result = await db.execute(
            select(User).filter(User.email == email)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        
        # Vérifier le mot de passe
        if not verify_password(password, user.hashed_password):
            return None
        
        # Vérifier que le compte est actif
        if not user.is_active:
            return None
        
        return user
    
    
    @staticmethod
    def create_token_for_user(user: User) -> Token:
        """
        Créer un token JWT pour un utilisateur
        
        Args:
            user: L'utilisateur pour lequel créer le token
            
        Returns:
            Token: Le token JWT
        """
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")
    
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
        """
        Récupérer un utilisateur par son ID
        
        Args:
            db: Session de base de données
            user_id: UUID de l'utilisateur
            
        Returns:
            User si trouvé, None sinon
        """
        result = await db.execute(
            select(User).filter(User.id == user_id)
        )
        return result.scalar_one_or_none()
