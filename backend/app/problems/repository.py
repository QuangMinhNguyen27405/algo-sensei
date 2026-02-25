"""Repository for problem-related database operations."""
from datetime import datetime, timezone
from typing import Any, Optional, List

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.problems.models import Problem, UserProblem, ProblemStatus, DifficultyLevel


class ProblemRepository:
    def __init__(self, db: Session):
        self.db = db

    # ── Problem (read-only, seeded data) ─────────────────────────────────

    def get_problem_by_id(self, problem_id: int) -> Problem | None:
        return self.db.query(Problem).filter(Problem.id == problem_id).first()

    def get_all_problems(
        self,
        difficulty: Optional[DifficultyLevel] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Problem]:
        query = self.db.query(Problem)
        if difficulty:
            query = query.filter(Problem.difficulty == difficulty)
        return query.offset(skip).limit(limit).all()

    # ── UserProblem CRUD ─────────────────────────────────────────────────

    def create_user_problem(
        self,
        user_id: int,
        problem_id: int,
        status: ProblemStatus = ProblemStatus.NOT_STARTED,
        user_code: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> UserProblem | None:
        user_problem = UserProblem(
            user_id=user_id,
            problem_id=problem_id,
            status=status,
            user_code=user_code,
            notes=notes,
        )
        try:
            self.db.add(user_problem)
            self.db.commit()
            self.db.refresh(user_problem)
            return user_problem
        except IntegrityError:
            self.db.rollback()
            return None

    def get_user_problem(self, user_id: int, problem_id: int) -> UserProblem | None:
        return (
            self.db.query(UserProblem)
            .filter(UserProblem.user_id == user_id, UserProblem.problem_id == problem_id)
            .first()
        )

    def get_user_problems(
        self,
        user_id: int,
        status: Optional[ProblemStatus] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[UserProblem]:
        query = self.db.query(UserProblem).filter(UserProblem.user_id == user_id)
        if status:
            query = query.filter(UserProblem.status == status)
        return query.offset(skip).limit(limit).all()

    def update_user_problem(
        self, user_id: int, problem_id: int, **kwargs: Any
    ) -> UserProblem | None:
        user_problem = self.get_user_problem(user_id, problem_id)
        if not user_problem:
            return None

        for key, value in kwargs.items():
            if value is not None:
                setattr(user_problem, key, value)

        # Auto-set completion date when status changes to COMPLETED
        if kwargs.get("status") == ProblemStatus.COMPLETED:
            user_problem.completion_date = datetime.now(timezone.utc).isoformat()

        self.db.commit()
        self.db.refresh(user_problem)
        return user_problem

