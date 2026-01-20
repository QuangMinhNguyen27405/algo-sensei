import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
BACKEND_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from app.auth.router import router as auth_router
from app.auth.dependency import get_auth_service, authenticate_current_user
from app.utils.exceptions import UnauthorizedException


class FakeAuthService:
    async def get_user_by_id(self, user_id: int):
        return {"id": user_id, "username": "testuser", "email": "test@example.com", "is_active": True}

    async def login_with_email_and_password(self, username: str | None, email: str | None, password: str):
        # Simulate successful login
        if password == "correct-password":
            return {"access_token": "test-token", "token_type": "bearer"}
        raise UnauthorizedException("Invalid credentials")

    async def register_user(self, username: str, email: str, password: str):
        # Simulate successful registration
        return {"id": 1, "username": username, "email": email, "is_active": True}

    async def logout_user(self, user_id: int):
        return None

    async def change_password(self, user_id: int, old_password: str, new_password: str):
        # Simulate successful password change
        return {"id": user_id, "username": "testuser", "email": "test@example.com", "is_active": True}

    async def delete_user(self, user_id: int):
        return {"id": user_id, "username": "testuser", "email": "test@example.com", "is_active": False}


def create_test_app():
    app = FastAPI()
    # Include the auth router under /users
    app.include_router(auth_router)

    # Override dependencies with test fakes
    app.dependency_overrides[get_auth_service] = lambda: FakeAuthService()
    app.dependency_overrides[authenticate_current_user] = lambda: 1

    return app

@pytest.fixture
def make_client():
    """Factory fixture to create a TestClient with optional dependency overrides."""
    def _make(overrides: dict | None = None) -> TestClient:
        app = create_test_app()
        if overrides:
            for dep, provider in overrides.items():
                app.dependency_overrides[dep] = provider
        return TestClient(app)

    return _make
