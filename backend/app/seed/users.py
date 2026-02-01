from app.auth.models import User
from app.config import settings
from app.config.database import engine
from sqlmodel import Session
from app.auth.repository import AuthRepository

from app.auth.service import AuthService
from app.auth.dependency import get_auth_service

def seed_users():
    with Session(engine) as session:
        try: 
            auth_repository = AuthRepository(session)
            authService: AuthService = get_auth_service(settings.settings, auth_repository)            
            admin_password = "adminpass"
            user_password = "12345"

            hashed_admin_password = authService.get_password_hash(admin_password)
            hashed_user_password = authService.get_password_hash(user_password)

            users = [
                User(username="admin", email="admin@gmail.com", password=hashed_admin_password),
                User(username="user1", email="user1@gmail.com", password=hashed_user_password),
                User(username="user2", email="user2@gmail.com", password=hashed_user_password),
                User(username="user3", email="user3@gmail.com", password=hashed_user_password),
                User(username="user4", email="user4@gmail.com", password=hashed_user_password),
                User(username="user5", email="user5@gmail.com", password=hashed_user_password),
                User(username="user6", email="user6@gmail.com", password=hashed_user_password),
            ]

            session.add_all(users)
            session.commit()

        except Exception as e:
            session.rollback()
            print(f"Error seeding users: {e}")


    

