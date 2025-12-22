from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
import logging

from app.config.log import setup_logging
setup_logging()

from app.config.database import engine
from app.auth.router import router as auth_router

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("✅ Database connection successful!")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise
    
    yield
    
    logger.info("Shutting down...")

app = FastAPI(
    title="AlgoSensei API",
    description="Backend API for AlgoSensei platform",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Welcome to AlgoSensei API", "status": "healthy"}

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
