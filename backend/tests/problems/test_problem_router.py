"""Unit tests for Problems router endpoints."""
from app.problems.dependency import get_problem_service
from app.auth.dependency import authenticate_current_user
from app.utils.exceptions import AlreadyExistsException, NotFoundException
from tests.problems.conftest import FakeProblemService


# ── Problem read-only routes ────────────────────────────────────────────────


def test_get_all_problems_returns_list(make_client):
    svc = FakeProblemService()
    svc._seed_problem("P1", "EASY")

    client = make_client({get_problem_service: lambda: svc})

    resp = client.get("/problems/", params={"skip": 0, "limit": 10})
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, list)
    assert len(body) >= 1


def test_get_all_problems_filter_by_difficulty(make_client):
    svc = FakeProblemService()
    svc._seed_problem("Easy One", "EASY")
    svc._seed_problem("Hard One", "HARD")

    client = make_client({get_problem_service: lambda: svc})

    resp = client.get("/problems/", params={"difficulty": "EASY"})
    assert resp.status_code == 200
    body = resp.json()
    for p in body:
        assert p["difficulty"] == "EASY"


def test_get_all_problems_empty_list(make_client):
    client = make_client()
    resp = client.get("/problems/")
    assert resp.status_code == 200
    assert resp.json() == []


def test_get_problem_by_id_success(make_client):
    svc = FakeProblemService()
    p = svc._seed_problem("Find Me", "MEDIUM")
    pid = p["id"]

    client = make_client({get_problem_service: lambda: svc})

    resp = client.get(f"/problems/{pid}")
    assert resp.status_code == 200
    assert resp.json()["id"] == pid
    assert resp.json()["title"] == "Find Me"


def test_get_problem_by_id_not_found(make_client):
    client = make_client()
    resp = client.get("/problems/999999")
    assert resp.status_code == 404


# ── User Problem CRUD routes ────────────────────────────────────────────────


def test_create_user_problem_success(make_client):
    svc = FakeProblemService()
    svc._seed_problem("Track Me", "EASY")

    client = make_client({get_problem_service: lambda: svc})

    resp = client.post("/problems/user", json={"problem_id": 1, "status": "not_started"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["user_id"] == 1
    assert body["problem_id"] == 1
    assert body["status"] == "not_started"
    assert body["attempts"] == 0
    assert body["time_spent_seconds"] == 0


def test_create_user_problem_with_notes(make_client):
    svc = FakeProblemService()
    svc._seed_problem("Notes Problem", "EASY")

    client = make_client({get_problem_service: lambda: svc})

    resp = client.post("/problems/user", json={
        "problem_id": 1,
        "status": "not_started",
        "notes": "Try dynamic programming",
    })
    assert resp.status_code == 201
    assert resp.json()["notes"] == "Try dynamic programming"


def test_create_user_problem_duplicate_returns_409(make_client):
    class DuplicateService:
        async def create_user_problem(self, **kwargs):
            raise AlreadyExistsException("User has already started this problem.")

    client = make_client({get_problem_service: lambda: DuplicateService()})

    resp = client.post("/problems/user", json={"problem_id": 1, "status": "not_started"})
    assert resp.status_code == 409


def test_get_my_problems_returns_list(make_client):
    svc = FakeProblemService()
    svc._seed_problem("P1", "EASY")
    svc._user_problems[(1, 1)] = {
        "id": 1, "user_id": 1, "problem_id": 1,
        "status": "not_started", "user_code": None, "notes": None,
        "attempts": 0, "time_spent_seconds": 0, "completion_date": None,
    }

    client = make_client({get_problem_service: lambda: svc})

    resp = client.get("/problems/user/me")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, list)
    assert len(body) >= 1


def test_get_my_specific_problem_success(make_client):
    svc = FakeProblemService()
    svc._seed_problem("Specific", "MEDIUM")
    svc._user_problems[(1, 1)] = {
        "id": 1, "user_id": 1, "problem_id": 1,
        "status": "not_started", "user_code": None, "notes": None,
        "attempts": 0, "time_spent_seconds": 0, "completion_date": None,
    }

    client = make_client({get_problem_service: lambda: svc})

    resp = client.get("/problems/user/me/1")
    assert resp.status_code == 200
    assert resp.json()["problem_id"] == 1


def test_get_my_specific_problem_not_found(make_client):
    client = make_client()
    resp = client.get("/problems/user/me/999")
    assert resp.status_code == 404


def test_update_user_problem_mark_completed(make_client):
    svc = FakeProblemService()
    svc._seed_problem("Complete Me", "EASY")
    svc._user_problems[(1, 1)] = {
        "id": 1, "user_id": 1, "problem_id": 1,
        "status": "not_started", "user_code": None, "notes": None,
        "attempts": 0, "time_spent_seconds": 0, "completion_date": None,
    }

    client = make_client({get_problem_service: lambda: svc})

    resp = client.put(
        "/problems/user/me/1",
        json={"status": "completed", "user_code": "def twoSum(): pass"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "completed"
    assert body["user_code"] == "def twoSum(): pass"
    assert body["completion_date"] is not None


def test_update_user_problem_with_new_fields(make_client):
    svc = FakeProblemService()
    svc._seed_problem("Track Fields", "MEDIUM")
    svc._user_problems[(1, 1)] = {
        "id": 1, "user_id": 1, "problem_id": 1,
        "status": "in_progress", "user_code": None, "notes": None,
        "attempts": 0, "time_spent_seconds": 0, "completion_date": None,
    }

    client = make_client({get_problem_service: lambda: svc})

    resp = client.put(
        "/problems/user/me/1",
        json={"attempts": 3, "time_spent_seconds": 1800, "notes": "Use hash map"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["attempts"] == 3
    assert body["time_spent_seconds"] == 1800
    assert body["notes"] == "Use hash map"


def test_update_user_problem_not_found(make_client):
    client = make_client()
    resp = client.put("/problems/user/me/999", json={"status": "completed"})
    assert resp.status_code == 404


def test_unauthenticated_user_problem_routes(make_client):
    """User problem routes should fail when no auth override is provided."""
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from app.problems.router import router as problem_router

    app = FastAPI()
    app.include_router(problem_router)
    app.dependency_overrides[get_problem_service] = lambda: FakeProblemService()
    # Deliberately NOT overriding authenticate_current_user
    client = TestClient(app)

    # All user-problem endpoints should return 401
    assert client.get("/problems/user/me").status_code == 401
    assert client.post("/problems/user", json={"problem_id": 1}).status_code == 401
