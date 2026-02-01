from sqlmodel import Session

from app.config.database import engine
from app.problems.models import DifficultyLevel, Problem, Tag
from sqlalchemy.exc import SQLAlchemyError

def seed_problems():
    sample_problems = [
        Problem(
            id=1,
            title="two-sum",
            difficulty=DifficultyLevel.EASY,
            tags=[Tag.ARRAY, Tag.HASH_TABLE],
            description="Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\nYou can return the answer in any order.\n \nExample 1:\n\nInput: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: Because nums[0] + nums[1] == 9, we return [0, 1].\n\nExample 2:\n\nInput: nums = [3,2,4], target = 6\nOutput: [1,2]\n\nExample 3:\n\nInput: nums = [3,3], target = 6\nOutput: [0,1]\n\n \nConstraints:\n\n2 <= nums.length <= 104\n-109 <= nums[i] <= 109\n-109 <= target <= 109\nOnly one valid answer exists.\n\n \nFollow-up: Can you come up with an algorithm that is less than O(n2) time complexity?",
            test_cases="[ [2,7,11,15], 9 ] -> [0,1]",
        ),
        Problem(
            id=2,
            title="add-two-numbers",
            difficulty=DifficultyLevel.MEDIUM,
            tags=[Tag.LINKED_LIST, Tag.MATH],
            description="You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.",
            test_cases="(2 -> 4 -> 3) + (5 -> 6 -> 4) -> 7 -> 0 -> 8",
        ),
        Problem(
            id=3,
            title="longest-substring-without-repeating-characters",
            difficulty=DifficultyLevel.MEDIUM,
            tags=[Tag.HASH_TABLE, Tag.STRING, Tag.SLIDING_WINDOW],
            description="Given a string s, find the length of the longest substring without repeating characters.",
            test_cases='"abcabcbb" -> 3',
        ),
    ]

    with Session(engine) as session:
        try:
            session.add_all(sample_problems)
            session.commit()
            print("Sample problems seeded successfully.")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error seeding sample problems: {e}")



if __name__ == "__main__":
    seed_problems()