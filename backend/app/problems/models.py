import enum
from typing import List
from sqlalchemy import ARRAY, Float, String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.config.database import Base

class DifficultyLevel(enum.Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class Tag(enum.Enum):
    HASH_FUNCTION = "HASH_FUNCTION"
    BREADTH_FIRST_SEARCH = "BREADTH-FIRST_SEARCH"
    STACK = "STACK"
    QUICKSELECT = "QUICKSELECT"
    LINE_SWEEP = "LINE_SWEEP"
    QUEUE = "QUEUE"
    GEOMETRY = "GEOMETRY"
    TWO_POINTERS = "TWO_POINTERS"
    UNION_FIND = "UNION_FIND"
    MERGE_SORT = "MERGE_SORT"
    BICONNECTED_COMPONENT = "BICONNECTED_COMPONENT"
    STRING_MATCHING = "STRING_MATCHING"
    CONCURRENCY = "CONCURRENCY"
    MATRIX = "MATRIX"
    MONOTONIC_STACK = "MONOTONIC_STACK"
    SEGMENT_TREE = "SEGMENT_TREE"
    MATH = "MATH"
    COUNTING = "COUNTING"
    RECURSION = "RECURSION"
    MONOTONIC_QUEUE = "MONOTONIC_QUEUE"
    MINIMUM_SPANNING_TREE = "MINIMUM_SPANNING_TREE"
    BINARY_TREE = "BINARY_TREE"
    ENUMERATION = "ENUMERATION"
    DYNAMIC_PROGRAMMING = "DYNAMIC_PROGRAMMING"
    GREEDY = "GREEDY"
    NUMBER_THEORY = "NUMBER_THEORY"
    STRONGLY_CONNECTED_COMPONENT = "STRONGLY_CONNECTED_COMPONENT"
    TOPOLOGICAL_SORT = "TOPOLOGICAL_SORT"
    ROLLING_HASH = "ROLLING_HASH"
    EULERIAN_CIRCUIT = "EULERIAN_CIRCUIT"
    DEPTH_FIRST_SEARCH = "DEPTH-FIRST_SEARCH"
    BINARY_SEARCH = "BINARY_SEARCH"
    BRAINTEASER = "BRAINTEASER"
    ARRAY = "ARRAY"
    RANDOMIZED = "RANDOMIZED"
    SHORTEST_PATH = "SHORTEST_PATH"
    TRIE = "TRIE"
    SLIDING_WINDOW = "SLIDING_WINDOW"
    COUNTING_SORT = "COUNTING_SORT"
    BIT_MANIPULATION = "BIT_MANIPULATION"
    SIMULATION = "SIMULATION"
    GRAPH = "GRAPH"
    MEMOIZATION = "MEMOIZATION"
    SUFFIX_ARRAY = "SUFFIX_ARRAY"
    ORDERED_SET = "ORDERED_SET"
    STRING = "STRING"
    BINARY_SEARCH_TREE = "BINARY_SEARCH_TREE"
    LINKED_LIST = "LINKED_LIST"
    DIVIDE_AND_CONQUER = "DIVIDE_AND_CONQUER"
    BACKTRACKING = "BACKTRACKING"
    HEAP_PRIORITY_QUEUE = "HEAP_(PRIORITY_QUEUE)"
    PREFIX_SUM = "PREFIX_SUM"
    HASH_TABLE = "HASH_TABLE"
    SORTING = "SORTING"
    COMBINATORICS = "COMBINATORICS"
    BUCKET_SORT = "BUCKET_SORT"
    PROBABILITY_AND_STATISTICS = "PROBABILITY_AND_STATISTICS"
    GAME_THEORY = "GAME_THEORY"
    BINARY_INDEXED_TREE = "BINARY_INDEXED_TREE"
    TREE = "TREE"
    INTERACTIVE = "INTERACTIVE"
    RADIX_SORT = "RADIX_SORT"
    BITMASK = "BITMASK"

class Problem(Base):
    __tablename__ = "problems"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    difficulty: Mapped[DifficultyLevel] = mapped_column(Enum(DifficultyLevel))
    test_cases: Mapped[List[str]] = mapped_column(String, nullable=True) 
    tags: Mapped[List[Tag]] = mapped_column(ARRAY(Enum(Tag, native_enum=True)), nullable=True)
    
    def __repr__(self) -> str:
        return f"<Problem(id={self.id}, title={self.title}, difficulty={self.difficulty})>"
    
class ProblemStatus(enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    
class UserProblem(Base):
    __tablename__ = "user_problems"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(index=True)
    problem_id: Mapped[int] = mapped_column(index=True)
    status: Mapped[ProblemStatus] = mapped_column(Enum(ProblemStatus), nullable=False, default=ProblemStatus.NOT_STARTED)
    user_code: Mapped[str] = mapped_column(String, nullable=True)
    completion_date: Mapped[str] = mapped_column(String, nullable=True)
    
    def __repr__(self) -> str:
        return f"<UserProblem(id={self.id}, user_id={self.user_id}, problem_id={self.problem_id}, status={self.status})>"
    
