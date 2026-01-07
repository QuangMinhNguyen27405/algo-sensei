"""Service layer that handle logic for authentication-related operations."""
from datetime import datetime, timedelta, timezone

import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from app.config.settings import settings
from app.utils.exceptions import AlreadyExistsException, UnauthorizedException, InternalServerException
from app.auth.schemas import UserCreateRequestSchema, UserLoginRequestSchema, UserChangePasswordRequestSchema
from app.auth.repository import AuthRepository


class AuthService:
    
    def __init__(self, db):
        self.authRepository = AuthRepository(db)
        self.password_hash = PasswordHash.recommended()
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        
    async def authenticate_user(self, token: str):
        user = await self.get_current_user(token)
        return user.id

    async def get_current_user(self, token: str):
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            user_id: str = payload.get("sub")
            
            if user_id is None:
                raise UnauthorizedException("Could not validate credentials")
            
            user = self.authRepository.get_user_by_id(int(user_id))   
            if user is None:
                raise UnauthorizedException("Could not validate credentials")
             
            return user
        
        except ExpiredSignatureError:
            raise UnauthorizedException("Token has expired")
        
        except InvalidTokenError:
            raise UnauthorizedException("Invalid token")

    async def login_with_email_and_password(self, user_data: UserLoginRequestSchema):
        # Find user by email and/or username
        user_by_email = None
        user_by_username = None
        
        if user_data.email:
            user_by_email = self.authRepository.get_user_by_email(user_data.email)
        
        if user_data.username:
            user_by_username = self.authRepository.get_user_by_username(user_data.username)
        
        # If both provided, they must match the same user
        if user_by_email and user_by_username:
            if user_by_email.id != user_by_username.id:
                raise UnauthorizedException("Email and username do not match the same account")
            user = user_by_email
        else:
            user = user_by_email or user_by_username
        
        # Check if user exists and password is correct
        if not user or not self.verify_password(user_data.password, user.password):
            raise UnauthorizedException("Incorrect email/username or password")
         
        access_token = self.create_access_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}
    
    async def register_user(self, user_data: UserCreateRequestSchema):
        hashed_password = self.get_password_hash(user_data.password)
        if self.authRepository.get_user_by_username(user_data.username) or self.authRepository.get_user_by_email(user_data.email):
            raise AlreadyExistsException("User with given username or email already exists.") 
        
        user = self.authRepository.create_user(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        
        if user is None:
            raise InternalServerException("Failed to create user.")
        
        del user.password
        return user
    
    async def logout_user(self, user_id):
        pass
    
    async def change_password(self, user_id, change_password_data: UserChangePasswordRequestSchema):
        user = self.authRepository.get_user_by_id(user_id)
                
        if not self.verify_password(change_password_data.old_password, user.password):
            raise UnauthorizedException("Old password is incorrect")
        
        new_hashed_password = self.get_password_hash(change_password_data.new_password)
        updated_user = self.authRepository.update_user(user_id, password=new_hashed_password)
        
        if updated_user is None:
            raise InternalServerException("Failed to update password.")
        
        del updated_user.password
        return updated_user
    
    async def delete_user(self, user_id):
        user = self.authRepository.delete_user(user_id)
        return user
    
    """
    Helper Functions
    """
    def get_password_hash(self, password: str) -> str: 
        return self.password_hash.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.password_hash.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: dict, expire_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expire_delta:
            expire = datetime.now(timezone.utc) + expire_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
