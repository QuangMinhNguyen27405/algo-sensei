"""Request and response schemas for problem routes."""
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from app.problems.models import DifficultyLevel, Tag, ProblemStatus


# ── Problem Schemas (read-only) ──────────────────────────────────────────────

class ProblemResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    difficulty: DifficultyLevel
    test_cases: Optional[str] = None
    tags: Optional[List[Tag]] = None


# ── UserProblem Schemas ──────────────────────────────────────────────────────

class UserProblemCreateRequestSchema(BaseModel):
    problem_id: int
    status: ProblemStatus = ProblemStatus.NOT_STARTED
    user_code: Optional[str] = None
    notes: Optional[str] = None

class UserProblemUpdateRequestSchema(BaseModel):
    status: Optional[ProblemStatus] = None
    user_code: Optional[str] = None
    notes: Optional[str] = None
    attempts: Optional[int] = None
    time_spent_seconds: Optional[int] = None

class UserProblemResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    problem_id: int
    status: ProblemStatus
    user_code: Optional[str] = None
    notes: Optional[str] = None
    attempts: int = 0
    time_spent_seconds: int = 0
    completion_date: Optional[str] = None
