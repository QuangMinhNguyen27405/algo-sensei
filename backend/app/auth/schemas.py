"""Request and response schemas for authentication routes."""
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreateRequestSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    
class UserLoginRequestSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str
    
class UserChangePasswordRequestSchema(BaseModel):
    old_password: str
    new_password: str

class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    

    

    