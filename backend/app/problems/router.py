"""Router definitions for problem-related endpoints."""
from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Query, status

from app.auth.dependency import authenticate_current_user
from app.problems.dependency import get_problem_service
from app.problems.models import DifficultyLevel, ProblemStatus
from app.problems.schemas import (
    ProblemResponseSchema,
    UserProblemCreateRequestSchema,
    UserProblemResponseSchema,
    UserProblemUpdateRequestSchema,
)
from app.problems.service import ProblemService

router = APIRouter(prefix="/problems", tags=["problems"])


# ── Problem (read-only, seeded data) ─────────────────────────────────────────


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_problems(
    problem_service: Annotated[ProblemService, Depends(get_problem_service)],
    difficulty: Optional[DifficultyLevel] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
) -> List[ProblemResponseSchema]:
    """Get all problems with optional difficulty filter and pagination."""
    return await problem_service.get_all_problems(
        difficulty=difficulty, skip=skip, limit=limit
    )


@router.get("/{problem_id}", status_code=status.HTTP_200_OK)
async def get_problem_by_id(
    problem_id: int,
    problem_service: Annotated[ProblemService, Depends(get_problem_service)],
) -> ProblemResponseSchema:
    """Get a single problem by ID."""
    return await problem_service.get_problem_by_id(problem_id)


# ── UserProblem CRUD ─────────────────────────────────────────────────────────


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user_problem(
    body: UserProblemCreateRequestSchema,
    user_id: Annotated[int, Depends(authenticate_current_user)],
    problem_service: Annotated[ProblemService, Depends(get_problem_service)],
) -> UserProblemResponseSchema:
    """Start tracking a problem for the authenticated user."""
    return await problem_service.create_user_problem(
        user_id=user_id,
        problem_id=body.problem_id,
        status=body.status,
        user_code=body.user_code,
        notes=body.notes,
    )


@router.get("/user/me", status_code=status.HTTP_200_OK)
async def get_my_problems(
    user_id: Annotated[int, Depends(authenticate_current_user)],
    problem_service: Annotated[ProblemService, Depends(get_problem_service)],
    problem_status: Optional[ProblemStatus] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
) -> List[UserProblemResponseSchema]:
    """Get all problems for the authenticated user with optional status filter."""
    return await problem_service.get_user_problems(
        user_id=user_id, status=problem_status, skip=skip, limit=limit
    )


@router.get("/user/me/{problem_id}", status_code=status.HTTP_200_OK)
async def get_my_problem(
    problem_id: int,
    user_id: Annotated[int, Depends(authenticate_current_user)],
    problem_service: Annotated[ProblemService, Depends(get_problem_service)],
) -> UserProblemResponseSchema:
    """Get a specific tracked problem for the authenticated user."""
    return await problem_service.get_user_problem(user_id=user_id, problem_id=problem_id)


@router.put("/user/me/{problem_id}", status_code=status.HTTP_200_OK)
async def update_my_problem(
    problem_id: int,
    body: UserProblemUpdateRequestSchema,
    user_id: Annotated[int, Depends(authenticate_current_user)],
    problem_service: Annotated[ProblemService, Depends(get_problem_service)],
) -> UserProblemResponseSchema:
    """Update a tracked problem for the authenticated user."""
    return await problem_service.update_user_problem(
        user_id=user_id,
        problem_id=problem_id,
        status=body.status,
        user_code=body.user_code,
        notes=body.notes,
        attempts=body.attempts,
        time_spent_seconds=body.time_spent_seconds,
    )
