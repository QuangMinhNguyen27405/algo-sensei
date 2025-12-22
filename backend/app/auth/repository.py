"""Repository for authentication-related database operations."""

from sqlalchemy.exc import IntegrityError
from app.auth.user import User

class AuthRepository:
    def __init__(self, db):
        self.db = db

    def create_user(self, username, email, hashed_password):
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
    
    def update_user(self, user_id: str, **kwargs):
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete_user(self, id: str):        
        user = self.update_user(id, is_active=False)
        return user
        

    