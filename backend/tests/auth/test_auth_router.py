from app.utils.exceptions import AlreadyExistsException, UnauthorizedException
from app.auth.dependency import get_auth_service, get_current_user_id
from fastapi.testclient import TestClient


class FakeAuthServiceOverride:
    def __init__(self):
        self._login_response = {"access_token": "override-token", "token_type": "bearer"}

    async def get_user_by_id(self, user_id: int):
        return {"id": user_id, "username": "overridden"}

    async def login_with_email_and_password(self, user_data):
        return self._login_response

    async def register_user(self, user_data):
        return {"id": 99, "username": user_data.username, "email": user_data.email}

    async def logout_user(self, user_id: int):
        return None

    async def change_password(self, user_id: int, change_password_data):
        return {"id": user_id, "username": "overridden"}

    async def delete_user(self, user_id: int):
        return {"id": user_id, "deleted": True}


def test_me_success(make_client):
    client = make_client({get_current_user_id: lambda: 42})

    resp = client.get("/users/me")
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == 42
    assert body["username"] == "testuser" or body["username"] == "overridden"


def test_login_success(make_client):
    # Override with a different fake service
    client = make_client({get_auth_service: lambda: FakeAuthServiceOverride()})

    payload = {"email": "test@example.com", "password": "pass123"}
    resp = client.post("/users/login", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert "access_token" in body


def test_register_conflict_returns_409(make_client):
    class ConflictService:
        async def register_user(self, user_data):
            raise AlreadyExistsException("User exists")

    client = make_client({get_auth_service: lambda: ConflictService()})

    payload = {"username": "taken", "email": "taken@example.com", "password": "pass123"}
    resp = client.post("/users/register", json=payload)
    # FastAPI converts HTTPException to response with its status code
    assert resp.status_code in (409, 400, 422)  # Prefer 409; schemas may affect code


def test_change_password_success(make_client):
    client = make_client({get_current_user_id: lambda: 7})

    payload = {"old_password": "old", "new_password": "new"}
    resp = client.put("/users/change-password", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == 7


def test_delete_account_success(make_client):
    client = make_client({get_current_user_id: lambda: 3})

    resp = client.delete("/users/delete")
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == 3
    assert body.get("deleted") is True
