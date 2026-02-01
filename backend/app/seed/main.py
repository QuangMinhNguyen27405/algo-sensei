from app.config.database import engine, Base

from app.seed.problems import seed_problems
from app.seed.users import seed_users


if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    seed_users()
    seed_problems()