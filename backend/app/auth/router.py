"""Router definitions for authentication-related endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.service import AuthService 
from app.schemas.auth_schemas import UserCreateRequestSchema
from app.auth.user import User
from app.config.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

"""Dependency to get AuthService instance with a Database Session."""
def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    authService = AuthService(db)
    return authService

router = APIRouter(
    prefix="/users", 
    tags=["auth"]
)

"""Get current authenticated user information."""
@router.get("/me", status_code=status.HTTP_200_OK)
async def get_current_user(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await auth_service.get_current_user()

"""Authenticate user and return access token."""
@router.post("/login", status_code=status.HTTP_200_OK)
async def login_with_password(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await auth_service.login_with_password(form_data)

"""Register a new user account."""
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserCreateRequestSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await auth_service.register_user(user_in)

"""Logout current user and invalidate token."""
@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(
    current_user: Annotated[User, Depends(get_current_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    await auth_service.logout_user(current_user)
    return {"msg": "User logged out successfully"}

