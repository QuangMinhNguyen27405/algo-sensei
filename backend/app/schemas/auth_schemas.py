"""Request and response schemas for authentication routes."""
from pydantic import BaseModel, EmailStr

class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

class UserCreateRequestSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    

    