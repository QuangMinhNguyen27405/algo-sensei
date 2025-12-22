import time
import logging
from sqlalchemy import text
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.requests import Request
from app.config.database import engine, Base
from app.middlewares.cors import setup_cors

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("✅ Database connection successful!")
        
        Base.metadata.create_all(bind=engine)
        logger.info("📊 Database tables created/verified")
        
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

# Global Middleware
setup_cors(app)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Color code status codes
    status_code = response.status_code
    if 200 <= status_code < 300:
        status_color = "\033[92m"
    elif 300 <= status_code < 400:
        status_color = "\033[96m"
    elif 400 <= status_code < 500:
        status_color = "\033[93m"
    else:
        status_color = "\033[91m"
    reset_color = "\033[0m"
    
    logger.info(
        f"{request.client.host} - {request.method} {request.url.path} - "
        f"{status_color}{status_code}{reset_color} - "
        f"{process_time:.4f}s"
    )
    
    return response

# Include routers
app.include_router(auth_router)

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Welcome to AlgoSensei API", "status": "healthy"}

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
