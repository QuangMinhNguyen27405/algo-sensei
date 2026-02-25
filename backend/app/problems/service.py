"""Service layer handling business logic for problem-related operations."""
from typing import Optional, List

from app.problems.models import Problem, UserProblem, DifficultyLevel, ProblemStatus
from app.problems.repository import ProblemRepository
from app.utils.exceptions import (
    AlreadyExistsException,
    InternalServerException,
    NotFoundException,
)


class ProblemService:

    def __init__(self, problem_repository: ProblemRepository):
        self.problem_repository = problem_repository

    # ── Problem operations (read-only) ───────────────────────────────────

    async def get_problem_by_id(self, problem_id: int) -> Problem:
        problem = self.problem_repository.get_problem_by_id(problem_id)
        if problem is None:
            raise NotFoundException(f"Problem with id {problem_id} not found.")
        return problem

    async def get_all_problems(
        self,
        difficulty: Optional[DifficultyLevel] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Problem]:
        return self.problem_repository.get_all_problems(
            difficulty=difficulty, skip=skip, limit=limit
        )

    # ── UserProblem operations ───────────────────────────────────────────

    async def create_user_problem(
        self,
        user_id: int,
        problem_id: int,
        status: ProblemStatus = ProblemStatus.NOT_STARTED,
        user_code: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> UserProblem:
        # Validate the problem exists
        problem = self.problem_repository.get_problem_by_id(problem_id)
        if not problem:
            raise NotFoundException(f"Problem with id {problem_id} not found.")

        # Check for duplicate
        existing = self.problem_repository.get_user_problem(user_id, problem_id)
        if existing:
            raise AlreadyExistsException("User has already started this problem.")

        user_problem = self.problem_repository.create_user_problem(
            user_id=user_id,
            problem_id=problem_id,
            status=status,
            user_code=user_code,
            notes=notes,
        )
        if user_problem is None:
            raise InternalServerException("Failed to create user problem.")
        return user_problem

    async def get_user_problems(
        self,
        user_id: int,
        status: Optional[ProblemStatus] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[UserProblem]:
        return self.problem_repository.get_user_problems(
            user_id=user_id, status=status, skip=skip, limit=limit
        )

    async def get_user_problem(self, user_id: int, problem_id: int) -> UserProblem:
        user_problem = self.problem_repository.get_user_problem(user_id, problem_id)
        if user_problem is None:
            raise NotFoundException("User problem entry not found.")
        return user_problem

    async def update_user_problem(
        self,
        user_id: int,
        problem_id: int,
        status: Optional[ProblemStatus] = None,
        user_code: Optional[str] = None,
        notes: Optional[str] = None,
        attempts: Optional[int] = None,
        time_spent_seconds: Optional[int] = None,
    ) -> UserProblem:
        existing = self.problem_repository.get_user_problem(user_id, problem_id)
        if not existing:
            raise NotFoundException("User problem entry not found.")

        updated = self.problem_repository.update_user_problem(
            user_id,
            problem_id,
            status=status,
            user_code=user_code,
            notes=notes,
            attempts=attempts,
            time_spent_seconds=time_spent_seconds,
        )
        if updated is None:
            raise InternalServerException("Failed to update user problem.")
        return updated
