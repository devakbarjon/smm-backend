from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings


class AdminAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not request.url.path.startswith("/api/v1/admin"):
            return await call_next(request)
        
        if request.url.path == "/api/v1/admin/verify-key":
            return await call_next(request)
        
        admin_key = request.headers.get("x-admin-key")
        
        if admin_key != settings.ADMIN_KEY.get_secret_value():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid admin key"
            )
        
        return await call_next(request)
