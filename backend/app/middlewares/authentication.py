"""Authentication middleware for extracting user_id from JWT token."""
import jwt
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.config.settings import settings

"""Middleware to extract user_id from JWT token and store in request.state"""
class AuthenticationMiddleware(BaseHTTPMiddleware):
        
    async def dispatch(self, request: Request, call_next):
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
            try:
                # Decode token and extract user_id
                payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
                user_id = payload.get("sub")
                if user_id:
                    request.state.user_id = int(user_id)
            except:
                # If token is invalid, set user_id to None
                request.state.user_id = None
        else:
            request.state.user_id = None
        
        response = await call_next(request)
        return response