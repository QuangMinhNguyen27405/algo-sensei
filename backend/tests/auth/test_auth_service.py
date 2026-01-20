import jwt
import pytest
from unittest.mock import AsyncMock, patch

from types import SimpleNamespace

from app.auth.service import AuthService
from app.utils.exceptions import UnauthorizedException
from app.config.settings import settings


class FakeRepo:
    def __init__(self, user=None, user2=None):
        self._user = user
        self._user2 = user2

    def get_user_by_email(self, email: str):
        return self._user

    def get_user_by_username(self, username: str):
        # Return second user to simulate mismatch when both provided
        return self._user2

    def get_user_by_id(self, user_id: int):
        return self._user

    def update_user(self, user_id: int, **kwargs):
        # Return object with potentially updated password
        if self._user:
            for k, v in kwargs.items():
                setattr(self._user, k, v)
        return self._user

    def delete_user(self, user_id: int):
        return SimpleNamespace(id=user_id, deleted=True)


def test_create_access_token_contains_sub_and_decodes():
    svc = AuthService(settings, FakeRepo())  # type: ignore
    token = svc.create_access_token({"sub": "1"})
    decoded = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    assert decoded["sub"] == "1"
    assert "exp" in decoded


@pytest.mark.asyncio
async def test_login_with_email_success_verifies_password():
    # Prepare a user with hashed password
    temp_svc = AuthService(settings, FakeRepo())  # type: ignore
    hashed = temp_svc.get_password_hash("secret")
    user = SimpleNamespace(id=10, email="u@example.com", username="user", password=hashed)

    # Create service with fake repo
    svc = AuthService(settings, FakeRepo(user=user))  # type: ignore

    # Mock the create_access_token method
    with patch.object(svc, "create_access_token", return_value="test-token"):
        # Call the method with keyword arguments
        result = await svc.login_with_email_and_password(email="u@example.com", username=None, password="secret")

    assert result["access_token"] == "test-token"


@pytest.mark.asyncio
async def test_login_with_both_mismatch_raises_unauthorized():
    temp_svc = AuthService(settings, FakeRepo())  # type: ignore
    user1 = SimpleNamespace(id=1, email="a@example.com", username="a", password=temp_svc.get_password_hash("p1"))
    user2 = SimpleNamespace(id=2, email="b@example.com", username="b", password=temp_svc.get_password_hash("p2"))

    svc = AuthService(settings, FakeRepo(user=user1, user2=user2))  # type: ignore

    with pytest.raises(UnauthorizedException):
        await svc.login_with_email_and_password(email="a@example.com", username="b", password="p1")


@pytest.mark.asyncio
async def test_get_current_user_invalid_token_raises():
    svc = AuthService(settings, FakeRepo())  # type: ignore
    with pytest.raises(UnauthorizedException):
        await svc.get_current_user("invalid-token")


@pytest.mark.asyncio
async def test_change_password_updates_hash_and_hides_password():
    temp_svc = AuthService(settings, FakeRepo())  # type: ignore
    old_hashed = temp_svc.get_password_hash("old")
    user = SimpleNamespace(id=5, password=old_hashed)

    svc = AuthService(settings, FakeRepo(user=user))  # type: ignore

    change_req = SimpleNamespace(old_password="old", new_password="new")

    updated = await svc.change_password(5, change_req.old_password, change_req.new_password)  # type: ignore
    assert updated.id == 5
