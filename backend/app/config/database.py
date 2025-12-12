import os
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector

from app.config.settings import settings

"""
Initialize Cloud SQL Python Connector
"""

logger = logging.getLogger(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials or ""

connector = Connector()

def getconn():
    """Create a connection to Cloud SQL PostgreSQL."""
    try:
        conn = connector.connect(
            settings.instance_connection_name,
            "pg8000",
            user=settings.db_user,
            password=settings.db_pass,
            db=settings.db_name,
        )
        logger.info(f"Successfully connected to database: {settings.db_name}")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise

"""
Create the database engine, which is the connection interface to the database
Mangese the connection pool and handles communication within the database.
"""
engine = create_engine(
    "postgresql+pg8000://",
    creator=getconn,
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800,
)

"""
Create a session factory that produces database sessions. A session manages the operations
for ORM-mapped objects, including querying, persisting, and transactions.
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

"""
Create a base class for declarative class definitions. All ORM-mapped classes will
inherit from this base class.
"""
Base = declarative_base()

def get_db():
    """
    Dependency that provides a database session for each request.
    Ensures that the session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

