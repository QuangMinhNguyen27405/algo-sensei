import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.database import Base
from app.auth.repository import AuthRepository
from app.auth.models import User

# Setup in-memory SQLite DB
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_create_user(db_session):
    repo = AuthRepository(db_session)
    user = repo.create_user("testuser", "test@example.com", "hashed_password")
    assert user is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.is_active is True

def test_create_duplicate_user(db_session):
    repo = AuthRepository(db_session)
    repo.create_user("testuser", "test@example.com", "hashed_password")
    
    # Try duplicate username
    user2 = repo.create_user("testuser", "other@example.com", "pass")
    assert user2 is None
    
    # Try duplicate email
    user3 = repo.create_user("other", "test@example.com", "pass")
    assert user3 is None

def test_soft_delete_and_reactivation(db_session):
    repo = AuthRepository(db_session)
    # Create
    user = repo.create_user("testuser", "test@example.com", "hashed_password")
    assert user is not None
    assert user.is_active is True
    user_id = user.id
    
    # Delete
    deleted_user = repo.delete_user(user_id)
    assert deleted_user is not None
    assert deleted_user.is_active is False
    
    # Check it's not found by get_user_by_username (which filters by active)
    assert repo.get_user_by_username("testuser") is None
    
    # Check it is found by get_user_all_by_username
    assert repo.get_user_all_by_username("testuser") is not None
    
    # Reactivate via create_user
    reactivated_user = repo.create_user("testuser", "test@example.com", "new_hashed_password")
    assert reactivated_user is not None
    assert reactivated_user.id == user_id
    assert reactivated_user.is_active is True
    assert reactivated_user.password == "new_hashed_password"

def test_get_user_by_id(db_session):
    repo = AuthRepository(db_session)
    user = repo.create_user("testuser", "test@example.com", "pwd")
    assert user is not None
    found = repo.get_user_by_id(user.id)
    assert found is not None
    assert found.id == user.id

def test_update_user(db_session):
    repo = AuthRepository(db_session)
    user = repo.create_user("testuser", "test@example.com", "pwd")
    assert user is not None
    updated = repo.update_user(user.id, email="new@example.com")
    assert updated is not None
    assert updated.email == "new@example.com"
    
    # Verify in DB
    from_db = repo.get_user_by_id(user.id)
    assert from_db is not None
    assert from_db.email == "new@example.com"
