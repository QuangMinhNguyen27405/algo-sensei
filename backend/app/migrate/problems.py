import math
import pandas as pd
import os
from rich.progress import Progress

from sqlmodel import Session

from app.config.database import engine
from app.problems.models import DifficultyLevel, Problem, Tag
from sqlalchemy.exc import SQLAlchemyError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df_train_path = os.path.join(BASE_DIR, "LeetCodeDataset-train.jsonl")
df_test_path = os.path.join(BASE_DIR, "LeetCodeDataset-test.jsonl")

df_train = pd.read_json(df_train_path, lines=True)
df_test = pd.read_json(df_test_path, lines=True)

def normalize_tag(tag: str) -> str:
    tag = tag.upper().strip()
    tag = tag.replace(" ", "_")
    return tag

def import_dataframe_to_db(df, session: Session):
    BATCH_SIZE = 200

    try:
        with Progress() as progress:
            task = progress.add_task("Importing problems...", total=math.ceil(len(df) / BATCH_SIZE))
            batch = []
            for row in df.itertuples():
                batch.append(
                    Problem(
                        id=row.question_id,
                        title=row.task_id,
                        difficulty=DifficultyLevel(row.difficulty.upper()),
                        tags=[
                            Tag(normalize_tag(tag))
                            for tag in (row.tags or [])
                        ],
                        description=row.problem_description,
                        test_cases=row.test,
                    )
                )

                if len(batch) == BATCH_SIZE:
                    session.add_all(batch)
                    session.commit()
                    batch.clear()
                    progress.advance(task, advance=1)
            
            if batch:
                session.add_all(batch)
                session.commit()
                progress.advance(task, advance=1)

        print(f"Imported {len(df)} rows into the database.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error importing data: {e}")

def main():
    with Session(engine) as session:
        import_dataframe_to_db(df_train, session)
        import_dataframe_to_db(df_test, session)

if __name__ == "__main__":
    main()