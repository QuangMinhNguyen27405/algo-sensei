from fastapi import FastAPI
from app.config.settings import settings
from fastapi.middleware.cors import CORSMiddleware

""" 
This settings is used to configure CORS (Cross-Origin Resource Sharing) 
in a FastAPI application.

CORS is a security feature implemented by web browsers to restrict web pages 
from making requests to a different domain than the one that served the web page.

We configure CORS based on environment
"""
def setup_cors(app: FastAPI):
    if settings.debug:
        allow_origins = ["*"]
    else:
        allow_origins = [settings.frontend_url] if settings.frontend_url else []
        
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )