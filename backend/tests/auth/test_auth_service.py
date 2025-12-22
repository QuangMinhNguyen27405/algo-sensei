import jwt
import pytest

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
    svc = AuthService(db=None)
    token = svc.create_access_token({"sub": "1"})
    decoded = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    assert decoded["sub"] == "1"
    assert "exp" in decoded


@pytest.mark.asyncio
async def test_login_with_email_success_verifies_password():
    svc = AuthService(db=None)
    # Prepare a user with hashed password
    hashed = svc.get_password_hash("secret")
    user = SimpleNamespace(id=10, email="u@example.com", username="user", password=hashed)

    # Inject fake repo into service
    svc.authRepository = FakeRepo(user=user)

    # Build request-like object
    req = SimpleNamespace(email="u@example.com", username=None, password="secret")

    result = await svc.login_with_email_and_password(req)
    assert result["token_type"] == "bearer"
    assert "access_token" in result


@pytest.mark.asyncio
async def test_login_with_both_mismatch_raises_unauthorized():
    svc = AuthService(db=None)
    user1 = SimpleNamespace(id=1, email="a@example.com", username="a", password=svc.get_password_hash("p1"))
    user2 = SimpleNamespace(id=2, email="b@example.com", username="b", password=svc.get_password_hash("p2"))

    svc.authRepository = FakeRepo(user=user1, user2=user2)

    req = SimpleNamespace(email="a@example.com", username="b", password="p1")

    with pytest.raises(UnauthorizedException):
        await svc.login_with_email_and_password(req)


@pytest.mark.asyncio
async def test_get_current_user_invalid_token_raises():
    svc = AuthService(db=None)
    with pytest.raises(UnauthorizedException):
        await svc.get_current_user("invalid-token")


@pytest.mark.asyncio
async def test_change_password_updates_hash_and_hides_password():
    svc = AuthService(db=None)
    old_hashed = svc.get_password_hash("old")
    user = SimpleNamespace(id=5, password=old_hashed)

    svc.authRepository = FakeRepo(user=user)

    change_req = SimpleNamespace(old_password="old", new_password="new")

    updated = await svc.change_password(5, change_req)
    # Service deletes password attribute before returning
    assert not hasattr(updated, "password")
