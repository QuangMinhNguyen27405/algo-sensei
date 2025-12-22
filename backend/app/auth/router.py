"""Router definitions for authentication-related endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.auth.service import AuthService 
from app.auth.schemas import UserCreateRequestSchema, UserLoginRequestSchema, UserChangePasswordRequestSchema
from app.auth.dependency import get_auth_service, get_current_user_id

router = APIRouter(
    prefix="/users", 
    tags=["auth"]
)

"""Get current authenticated user information."""
@router.get("/me", status_code=status.HTTP_200_OK)
async def get_current_user(
    user_id: Annotated[int, Depends(get_current_user_id)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await auth_service.get_user_by_id(user_id)

"""Authenticate user and return access token."""
@router.post("/login", status_code=status.HTTP_200_OK)
async def login_with_email_and_password(
    user_data: UserLoginRequestSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await auth_service.login_with_email_and_password(user_data)

"""Register a new user account."""
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreateRequestSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await auth_service.register_user(user_data)

"""Logout current user and invalidate token."""
@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(
    user_id: Annotated[int, Depends(get_current_user_id)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    await auth_service.logout_user(user_id)
    return {"msg": "User logged out successfully"}

@router.put("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    change_password_data: UserChangePasswordRequestSchema,
    user_id: Annotated[int, Depends(get_current_user_id)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await auth_service.change_password(user_id, change_password_data)

@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_account(
    user_id: Annotated[int, Depends(get_current_user_id)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await auth_service.delete_user(user_id)

