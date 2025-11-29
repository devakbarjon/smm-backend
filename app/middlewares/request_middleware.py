from fastapi import Request

from main import app
from app.core.config import settings
from app.core.logging import logger


@app.middleware("http")
async def log_requests(request: Request, call_next):
    if settings.ENVIRONMENT == "development":
        client_host = request.client.host
    else:
        client_host = request.headers.get("X-Forwarded-For", request.client.host)
    logger.info(f"Incoming request: {request.method} {request.url} {client_host}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response