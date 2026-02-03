"""
Schémas Pydantic pour l'authentification
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
import uuid


# ============================================
# SCHÉMAS D'AUTHENTIFICATION
# ============================================

class UserRegister(BaseModel):
    """Schéma pour l'inscription d'un utilisateur"""
    email: EmailStr = Field(..., description="Email de l'utilisateur")
    password: str = Field(..., min_length=8, max_length=72, description="Mot de passe (8-72 caractères)")
    full_name: Optional[str] = Field(None, max_length=255, description="Nom complet")
    language: str = Field(default="fr", description="Langue préférée (fr/en)")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePassword123!",
                "full_name": "John Doe",
                "language": "fr"
            }
        }
    }


class UserLogin(BaseModel):
    """Schéma pour la connexion d'un utilisateur"""
    email: EmailStr = Field(..., description="Email de l'utilisateur")
    password: str = Field(..., description="Mot de passe")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePassword123!"
            }
        }
    }


class Token(BaseModel):
    """Schéma pour le token JWT"""
    access_token: str = Field(..., description="Token JWT")
    token_type: str = Field(default="bearer", description="Type de token")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    }


class TokenData(BaseModel):
    """Données contenues dans le token"""
    user_id: Optional[str] = None


# ============================================
# SCHÉMAS UTILISATEUR (Responses)
# ============================================

class UserBase(BaseModel):
    """Schéma de base pour un utilisateur"""
    email: EmailStr
    full_name: Optional[str] = None
    language: str = "fr"


class UserResponse(UserBase):
    """Schéma de réponse pour un utilisateur"""
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "language": "fr",
                "is_active": True,
                "created_at": "2024-01-30T10:00:00Z"
            }
        }
    }


class UserUpdate(BaseModel):
    """Schéma pour la mise à jour d'un utilisateur"""
    full_name: Optional[str] = None
    language: Optional[str] = None
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "full_name": "John Updated Doe",
                "language": "en"
            }
        }
    }


class PasswordUpdate(BaseModel):
    """Schéma pour la mise à jour du mot de passe"""
    current_password: str = Field(..., description="Mot de passe actuel")
    new_password: str = Field(..., min_length=8, max_length=72, description="Nouveau mot de passe (8-72 caractères)")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "current_password": "CurrentPassword123!",
                "new_password": "NewSecurePassword456!"
            }
        }
    }
