from typing import Annotated
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.repository import AuthRepository
from app.auth.service import AuthService 
from app.config.database import get_db
from app.config.settings import Settings, get_settings
from app.utils.exceptions import UnauthorizedException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_auth_repository(db: Annotated[Session, Depends(get_db)]):
    """Dependency to get AuthRepository instance with a Database Session."""
    return AuthRepository(db)

def get_auth_service(settings: Annotated[Settings, Depends(get_settings)], authRepository: Annotated[AuthRepository, Depends(get_auth_repository)]) -> AuthService:
    """Dependency to get AuthService instance with a Database Session."""
    authService = AuthService(settings, authRepository)
    return authService

def get_current_user_id(request: Request) -> int:
    """Dependency to get current user_id from middleware."""
    user_id = getattr(request.state, "user_id", None)
    if user_id is None:
        raise UnauthorizedException("Not authenticated")
    return user_id