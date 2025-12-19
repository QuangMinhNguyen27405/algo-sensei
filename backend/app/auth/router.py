from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.main import app

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]): 
    return current_user

@app.post("/users/login")
async def login_with_password(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return form_data

@app.post("/users/register")
async def register_user(user: str):
    pass

