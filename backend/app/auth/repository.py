"""Repository for authentication-related database operations."""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Any
from app.auth.models import User

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, username: str, email: str, hashed_password: str):
        # If user exists but inactive, reactivate instead of creating new
        user_by_username = self.get_user_all_by_username(username)
        user_by_email = self.get_user_all_by_email(email)
        
        existing = user_by_username if user_by_username else user_by_email
        
        if existing:
            if not existing.is_active:
                # Reactivate the inactive user with new password
                existing.is_active = True
                existing.password = hashed_password
                self.db.commit()
                self.db.refresh(existing)
                return existing
            else:
                # User exists and is active - cannot create duplicate
                return None

        # Otherwise, create new user
        new_user = User(username=username, email=email, password=hashed_password)
        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except IntegrityError:
            self.db.rollback()
            return None
    
    def get_user_by_id(self, id: int):
        return self.db.query(User).filter(User.id == id, User.is_active).first()
    
    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username, User.is_active).first()
    
    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email, User.is_active).first()
    
    def get_user_all_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_all_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    
    def update_user(self, user_id: int, **kwargs: Any):
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete_user(self, id: int):        
        user = self.update_user(id, is_active=False)
        return user
        

    