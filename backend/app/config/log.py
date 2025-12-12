import logging
from app.config.settings import settings

def setup_logging():
    """Configure global logging for the application."""
    logging_level = logging.DEBUG if settings.debug else logging.INFO

    logging.basicConfig(
        level=logging_level,
        format='%(levelname)s - %(name)s - %(message)s - %(asctime)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    logging.getLogger("google").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    logging.info("Logging configured successfully")

