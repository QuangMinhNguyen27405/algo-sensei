"""Service layer that handle logic for authentication-related operations."""
from datetime import datetime, timedelta, timezone

import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash

from app.config import settings
from app.auth.repository import AuthRepository

class AuthService:
    
    def __init__(self, db):
        self.repo = AuthRepository(db)
        self.password_hash = PasswordHash.recommended()
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    async def authenticate_user(self, username: str, password: str):
        user = await self.repo.get_user_by_username(username)
        if not user:
            return False
        # if not verify_password(password, user.hashed_password):
        #     return False
        return user

    async def get_current_user(self, token: str):
        # Decode and validate token, then get user from repository
        # This would use self.repo to fetch the user
        pass

    async def login_with_password(self, form_data: OAuth2PasswordRequestForm):
        user = await self.authenticate_user(form_data.username, form_data.password)
        # if not user:
        #     raise HTTPException(status_code=400, detail="Incorrect username or password")
        
        access_token = await self.create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    
    async def register_user(self, user_data):
        hashed_password = self.get_password_hash(user_data.password)
        user = await self.repo.create_user(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        return user
    
    async def logout_user(self, current_user):
        # Invalidate the user's token or perform logout operations
        pass
    
    """
    Helper Functions
    """
    def get_password_hash(self, password: str) -> str: 
        return self.password_hash.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.password_hash.verify(hashed_password, plain_password)
    
    def create_access_token(self, data: dict, expire_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expire_delta:
            expire_delta = datetime.now(timezone.utc) + expire_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt