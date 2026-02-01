
from sqlmodel import Session

from app.problems.models import Problem


class Problem_Repository:
    def __init__(self, session: Session):
        self.session = session

    def get_problem_by_id(self, problem_id: int) -> Problem | None:
        pass

    def get_problems_by_title(self, title: str) -> Problem | None:
        pass

    def get_problems_by_user_id(self, user_id: int) -> list[Problem]:
        pass
    
    def update_problem_status(self, problem_id: int, user_id: int, status: str) -> None:
        pass

    
