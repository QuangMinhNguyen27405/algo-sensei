import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
BACKEND_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from app.problems.router import router as problem_router
from app.problems.dependency import get_problem_service
from app.auth.dependency import authenticate_current_user
from app.problems.models import DifficultyLevel, ProblemStatus, Tag


class FakeProblemService:
    """Default fake that provides happy-path responses for every endpoint."""

    def __init__(self):
        self._problems = {}
        self._user_problems = {}
        self._next_id = 1
        self._next_up_id = 1

    # ── Problem (read-only helpers) ──────────────────────────────────────

    def _seed_problem(self, title, difficulty, description=None, test_cases=None, tags=None):
        """Helper to seed a problem into the fake store for test setup."""
        pid = self._next_id
        self._next_id += 1
        problem = {
            "id": pid,
            "title": title,
            "description": description,
            "difficulty": difficulty.value if isinstance(difficulty, DifficultyLevel) else difficulty,
            "test_cases": test_cases,
            "tags": [t.value if isinstance(t, Tag) else t for t in tags] if tags else None,
        }
        self._problems[pid] = problem
        return problem

    async def get_problem_by_id(self, problem_id):
        from app.utils.exceptions import NotFoundException
        if problem_id not in self._problems:
            raise NotFoundException(f"Problem with id {problem_id} not found.")
        return self._problems[problem_id]

    async def get_all_problems(self, difficulty=None, skip=0, limit=50):
        results = list(self._problems.values())
        if difficulty:
            val = difficulty.value if isinstance(difficulty, DifficultyLevel) else difficulty
            results = [p for p in results if p["difficulty"] == val]
        return results[skip : skip + limit]

    # ── UserProblem operations ───────────────────────────────────────────

    async def create_user_problem(self, user_id, problem_id, status=ProblemStatus.NOT_STARTED, user_code=None, notes=None):
        upid = self._next_up_id
        self._next_up_id += 1
        up = {
            "id": upid,
            "user_id": user_id,
            "problem_id": problem_id,
            "status": status.value if isinstance(status, ProblemStatus) else status,
            "user_code": user_code,
            "notes": notes,
            "attempts": 0,
            "time_spent_seconds": 0,
            "completion_date": None,
        }
        self._user_problems[(user_id, problem_id)] = up
        return up

    async def get_user_problems(self, user_id, status=None, skip=0, limit=50):
        results = [up for up in self._user_problems.values() if up["user_id"] == user_id]
        if status:
            val = status.value if isinstance(status, ProblemStatus) else status
            results = [up for up in results if up["status"] == val]
        return results[skip : skip + limit]

    async def get_user_problem(self, user_id, problem_id):
        from app.utils.exceptions import NotFoundException
        key = (user_id, problem_id)
        if key not in self._user_problems:
            raise NotFoundException("User problem entry not found.")
        return self._user_problems[key]

    async def update_user_problem(self, user_id, problem_id, status=None, user_code=None, notes=None, attempts=None, time_spent_seconds=None):
        from app.utils.exceptions import NotFoundException
        key = (user_id, problem_id)
        if key not in self._user_problems:
            raise NotFoundException("User problem entry not found.")
        up = self._user_problems[key]
        if status is not None:
            up["status"] = status.value if isinstance(status, ProblemStatus) else status
            if status == ProblemStatus.COMPLETED:
                up["completion_date"] = "2026-02-12T00:00:00+00:00"
        if user_code is not None:
            up["user_code"] = user_code
        if notes is not None:
            up["notes"] = notes
        if attempts is not None:
            up["attempts"] = attempts
        if time_spent_seconds is not None:
            up["time_spent_seconds"] = time_spent_seconds
        return up


_shared_service = FakeProblemService()


def create_test_app():
    app = FastAPI()
    app.include_router(problem_router)

    app.dependency_overrides[get_problem_service] = lambda: _shared_service
    app.dependency_overrides[authenticate_current_user] = lambda: 1

    return app


@pytest.fixture(autouse=True)
def reset_shared_service():
    """Reset fake service state before each test."""
    global _shared_service
    _shared_service = FakeProblemService()


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
