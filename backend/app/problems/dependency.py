"""Dependency injection for problem services."""
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.problems.repository import ProblemRepository
from app.problems.service import ProblemService


def get_problem_repository(db: Annotated[Session, Depends(get_db)]) -> ProblemRepository:
    """Dependency to get ProblemRepository instance with a Database Session."""
    return ProblemRepository(db)


def get_problem_service(
    problem_repository: Annotated[ProblemRepository, Depends(get_problem_repository)],
) -> ProblemService:
    """Dependency to get ProblemService instance."""
    return ProblemService(problem_repository)
