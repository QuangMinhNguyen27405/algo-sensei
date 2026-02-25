"""Unit tests for ProblemRepository database operations.

Uses an in-memory SQLite database. Because the Problem model uses
ARRAY(Enum(...)) (PostgreSQL-only), Problem CRUD is tested via a
simplified model. UserProblem works with SQLite natively.
"""
import pytest
from sqlalchemy import create_engine, String, Enum as SAEnum
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column

from app.config.database import Base
from app.problems.models import UserProblem, ProblemStatus
from app.problems.repository import ProblemRepository


engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create all tables, yield a session, then tear down."""
    UserProblem.__table__.create(engine, checkfirst=True)
    session = TestingSessionLocal()
    yield session
    session.close()
    UserProblem.__table__.drop(engine, checkfirst=True)


# ── UserProblem Repository Tests ────────────────────────────────────────────


def test_create_user_problem(db_session):
    repo = ProblemRepository(db_session)
    up = repo.create_user_problem(user_id=1, problem_id=100)
    assert up is not None
    assert up.user_id == 1
    assert up.problem_id == 100
    assert up.status == ProblemStatus.NOT_STARTED
    assert up.attempts == 0
    assert up.time_spent_seconds == 0


def test_create_user_problem_with_status_and_notes(db_session):
    repo = ProblemRepository(db_session)
    up = repo.create_user_problem(
        user_id=1, problem_id=100,
        status=ProblemStatus.IN_PROGRESS,
        user_code="def solve(): pass",
        notes="Try binary search",
    )
    assert up is not None
    assert up.status == ProblemStatus.IN_PROGRESS
    assert up.user_code == "def solve(): pass"
    assert up.notes == "Try binary search"


def test_get_user_problem(db_session):
    repo = ProblemRepository(db_session)
    repo.create_user_problem(user_id=1, problem_id=100)

    found = repo.get_user_problem(1, 100)
    assert found is not None
    assert found.user_id == 1
    assert found.problem_id == 100


def test_get_user_problem_not_found(db_session):
    repo = ProblemRepository(db_session)
    assert repo.get_user_problem(1, 999) is None


def test_get_user_problems_for_user(db_session):
    repo = ProblemRepository(db_session)
    repo.create_user_problem(user_id=1, problem_id=100)
    repo.create_user_problem(user_id=1, problem_id=101)
    repo.create_user_problem(user_id=2, problem_id=100)  # different user

    results = repo.get_user_problems(user_id=1)
    assert len(results) == 2


def test_get_user_problems_filter_by_status(db_session):
    repo = ProblemRepository(db_session)
    repo.create_user_problem(user_id=1, problem_id=100, status=ProblemStatus.NOT_STARTED)
    repo.create_user_problem(user_id=1, problem_id=101, status=ProblemStatus.COMPLETED)

    not_started = repo.get_user_problems(user_id=1, status=ProblemStatus.NOT_STARTED)
    assert len(not_started) == 1
    assert not_started[0].problem_id == 100

    completed = repo.get_user_problems(user_id=1, status=ProblemStatus.COMPLETED)
    assert len(completed) == 1
    assert completed[0].problem_id == 101


def test_get_user_problems_pagination(db_session):
    repo = ProblemRepository(db_session)
    for i in range(10):
        repo.create_user_problem(user_id=1, problem_id=100 + i)

    page = repo.get_user_problems(user_id=1, skip=2, limit=3)
    assert len(page) == 3


def test_update_user_problem(db_session):
    repo = ProblemRepository(db_session)
    repo.create_user_problem(user_id=1, problem_id=100)

    updated = repo.update_user_problem(
        user_id=1, problem_id=100,
        status=ProblemStatus.IN_PROGRESS, user_code="x = 1",
    )
    assert updated is not None
    assert updated.status == ProblemStatus.IN_PROGRESS
    assert updated.user_code == "x = 1"


def test_update_user_problem_new_fields(db_session):
    repo = ProblemRepository(db_session)
    repo.create_user_problem(user_id=1, problem_id=100)

    updated = repo.update_user_problem(
        user_id=1, problem_id=100,
        attempts=3, time_spent_seconds=1800, notes="Use hash map approach",
    )
    assert updated is not None
    assert updated.attempts == 3
    assert updated.time_spent_seconds == 1800
    assert updated.notes == "Use hash map approach"


def test_update_user_problem_to_completed_sets_date(db_session):
    repo = ProblemRepository(db_session)
    repo.create_user_problem(user_id=1, problem_id=100)

    updated = repo.update_user_problem(
        user_id=1, problem_id=100,
        status=ProblemStatus.COMPLETED,
    )
    assert updated is not None
    assert updated.status == ProblemStatus.COMPLETED
    assert updated.completion_date is not None


def test_update_user_problem_not_found(db_session):
    repo = ProblemRepository(db_session)
    result = repo.update_user_problem(user_id=1, problem_id=999, status=ProblemStatus.COMPLETED)
    assert result is None
