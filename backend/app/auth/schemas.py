"""Request and response schemas for authentication routes."""
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

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
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    email: EmailStr
    is_active: bool  
    

    

    

    