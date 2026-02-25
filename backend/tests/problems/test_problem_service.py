"""Unit tests for ProblemService business logic."""
import pytest
from types import SimpleNamespace

from app.problems.service import ProblemService
from app.problems.models import DifficultyLevel, ProblemStatus, Tag
from app.utils.exceptions import (
    AlreadyExistsException,
    InternalServerException,
    NotFoundException,
)


class FakeRepo:
    """In-memory fake repository for isolated service testing."""

    def __init__(self):
        self._problems = {}
        self._user_problems = {}
        self._next_id = 1
        self._next_up_id = 1

    def seed_problem(self, title, difficulty, description=None, test_cases=None, tags=None):
        """Helper to seed problems for read-only testing."""
        p = SimpleNamespace(
            id=self._next_id, title=title, difficulty=difficulty,
            description=description, test_cases=test_cases, tags=tags,
        )
        self._problems[self._next_id] = p
        self._next_id += 1
        return p

    def get_problem_by_id(self, problem_id):
        return self._problems.get(problem_id)

    def get_all_problems(self, difficulty=None, skip=0, limit=50):
        results = list(self._problems.values())
        if difficulty:
            results = [p for p in results if p.difficulty == difficulty]
        return results[skip : skip + limit]

    def create_user_problem(self, user_id, problem_id, status=ProblemStatus.NOT_STARTED, user_code=None, notes=None):
        up = SimpleNamespace(
            id=self._next_up_id, user_id=user_id, problem_id=problem_id,
            status=status, user_code=user_code, notes=notes,
            attempts=0, time_spent_seconds=0, completion_date=None,
        )
        self._user_problems[(user_id, problem_id)] = up
        self._next_up_id += 1
        return up

    def get_user_problem(self, user_id, problem_id):
        return self._user_problems.get((user_id, problem_id))

    def get_user_problems(self, user_id, status=None, skip=0, limit=50):
        results = [up for up in self._user_problems.values() if up.user_id == user_id]
        if status:
            results = [up for up in results if up.status == status]
        return results[skip : skip + limit]

    def update_user_problem(self, user_id, problem_id, **kwargs):
        up = self._user_problems.get((user_id, problem_id))
        if not up:
            return None
        for k, v in kwargs.items():
            if v is not None:
                setattr(up, k, v)
        return up


def _make_service(repo=None):
    return ProblemService(repo or FakeRepo())  # type: ignore


# ── Problem read-only operations ────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_problem_by_id_success():
    repo = FakeRepo()
    repo.seed_problem("P1", DifficultyLevel.MEDIUM)
    svc = _make_service(repo)

    result = await svc.get_problem_by_id(1)
    assert result.title == "P1"


@pytest.mark.asyncio
async def test_get_problem_by_id_not_found():
    svc = _make_service()
    with pytest.raises(NotFoundException):
        await svc.get_problem_by_id(999)


@pytest.mark.asyncio
async def test_get_all_problems():
    repo = FakeRepo()
    repo.seed_problem("A", DifficultyLevel.EASY)
    repo.seed_problem("B", DifficultyLevel.HARD)
    svc = _make_service(repo)

    all_problems = await svc.get_all_problems()
    assert len(all_problems) == 2

    easy_only = await svc.get_all_problems(difficulty=DifficultyLevel.EASY)
    assert len(easy_only) == 1
    assert easy_only[0].title == "A"


@pytest.mark.asyncio
async def test_get_all_problems_pagination():
    repo = FakeRepo()
    for i in range(10):
        repo.seed_problem(f"P{i}", DifficultyLevel.EASY)
    svc = _make_service(repo)

    page = await svc.get_all_problems(skip=2, limit=3)
    assert len(page) == 3


@pytest.mark.asyncio
async def test_get_all_problems_empty():
    svc = _make_service()
    result = await svc.get_all_problems()
    assert result == []


# ── UserProblem operations ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_create_user_problem_success():
    repo = FakeRepo()
    repo.seed_problem("P1", DifficultyLevel.EASY)
    svc = _make_service(repo)

    up = await svc.create_user_problem(user_id=1, problem_id=1)
    assert up.user_id == 1
    assert up.problem_id == 1
    assert up.status == ProblemStatus.NOT_STARTED
    assert up.attempts == 0


@pytest.mark.asyncio
async def test_create_user_problem_with_notes():
    repo = FakeRepo()
    repo.seed_problem("P1", DifficultyLevel.EASY)
    svc = _make_service(repo)

    up = await svc.create_user_problem(user_id=1, problem_id=1, notes="Use DP approach")
    assert up.notes == "Use DP approach"


@pytest.mark.asyncio
async def test_create_user_problem_nonexistent_problem_raises_404():
    svc = _make_service()
    with pytest.raises(NotFoundException):
        await svc.create_user_problem(user_id=1, problem_id=999)


@pytest.mark.asyncio
async def test_create_user_problem_duplicate_raises_409():
    repo = FakeRepo()
    repo.seed_problem("P1", DifficultyLevel.EASY)
    repo.create_user_problem(user_id=1, problem_id=1)
    svc = _make_service(repo)

    with pytest.raises(AlreadyExistsException):
        await svc.create_user_problem(user_id=1, problem_id=1)


@pytest.mark.asyncio
async def test_create_user_problem_repo_failure_raises_500():
    class FailRepo(FakeRepo):
        def create_user_problem(self, *args, **kwargs):
            return None

    repo = FailRepo()
    repo.seed_problem("P1", DifficultyLevel.EASY)
    svc = _make_service(repo)

    with pytest.raises(InternalServerException):
        await svc.create_user_problem(user_id=1, problem_id=1)


@pytest.mark.asyncio
async def test_get_user_problems():
    repo = FakeRepo()
    repo.seed_problem("P1", DifficultyLevel.EASY)
    repo.seed_problem("P2", DifficultyLevel.HARD)
    repo.create_user_problem(user_id=1, problem_id=1, status=ProblemStatus.NOT_STARTED)
    repo.create_user_problem(user_id=1, problem_id=2, status=ProblemStatus.COMPLETED)
    repo.create_user_problem(user_id=2, problem_id=1)  # different user
    svc = _make_service(repo)

    all_for_user1 = await svc.get_user_problems(user_id=1)
    assert len(all_for_user1) == 2

    completed = await svc.get_user_problems(user_id=1, status=ProblemStatus.COMPLETED)
    assert len(completed) == 1
    assert completed[0].problem_id == 2


@pytest.mark.asyncio
async def test_get_user_problem_success():
    repo = FakeRepo()
    repo.seed_problem("P1", DifficultyLevel.EASY)
    repo.create_user_problem(user_id=1, problem_id=1)
    svc = _make_service(repo)

    up = await svc.get_user_problem(user_id=1, problem_id=1)
    assert up.problem_id == 1


@pytest.mark.asyncio
async def test_get_user_problem_not_found():
    svc = _make_service()
    with pytest.raises(NotFoundException):
        await svc.get_user_problem(user_id=1, problem_id=999)


@pytest.mark.asyncio
async def test_update_user_problem_success():
    repo = FakeRepo()
    repo.seed_problem("P1", DifficultyLevel.EASY)
    repo.create_user_problem(user_id=1, problem_id=1)
    svc = _make_service(repo)

    updated = await svc.update_user_problem(
        user_id=1, problem_id=1,
        status=ProblemStatus.IN_PROGRESS, user_code="print('hi')",
    )
    assert updated.status == ProblemStatus.IN_PROGRESS
    assert updated.user_code == "print('hi')"


@pytest.mark.asyncio
async def test_update_user_problem_with_new_fields():
    repo = FakeRepo()
    repo.seed_problem("P1", DifficultyLevel.EASY)
    repo.create_user_problem(user_id=1, problem_id=1)
    svc = _make_service(repo)

    updated = await svc.update_user_problem(
        user_id=1, problem_id=1,
        attempts=5, time_spent_seconds=3600, notes="Solved with two pointers",
    )
    assert updated.attempts == 5
    assert updated.time_spent_seconds == 3600
    assert updated.notes == "Solved with two pointers"


@pytest.mark.asyncio
async def test_update_user_problem_not_found():
    svc = _make_service()
    with pytest.raises(NotFoundException):
        await svc.update_user_problem(user_id=1, problem_id=999, status=ProblemStatus.COMPLETED)


@pytest.mark.asyncio
async def test_update_user_problem_repo_failure_raises_500():
    class FailRepo(FakeRepo):
        def update_user_problem(self, *args, **kwargs):
            return None

    repo = FailRepo()
    repo.seed_problem("P1", DifficultyLevel.EASY)
    repo.create_user_problem(user_id=1, problem_id=1)
    svc = _make_service(repo)

    with pytest.raises(InternalServerException):
        await svc.update_user_problem(user_id=1, problem_id=1, status=ProblemStatus.COMPLETED)
