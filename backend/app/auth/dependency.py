from typing import Annotated
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.service import AuthService 
from app.auth.user import User
from app.config.database import get_db
from app.utils.exceptions import UnauthorizedException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

"""Dependency to get AuthService instance with a Database Session."""
def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    authService = AuthService(db)
    return authService

"""Dependency to get current user_id from middleware."""
def get_current_user_id(request: Request) -> int:
    user_id = getattr(request.state, "user_id", None)
    if user_id is None:
        raise UnauthorizedException("Not authenticated")
    return user_id