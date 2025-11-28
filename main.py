from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.db.base import engine, Base
from backend.app.core.logging import logger
from app.api.v1.router import router as api_v1_router
from app.services.telegram.bot.bot_base import bot
from app.core.config import settings


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database models initialized.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()  # Initialize database models
    yield
    await bot.session.close()
    logger.info("Shutting down...")


app = FastAPI(lifespan=lifespan)

app.include_router(api_v1_router, prefix=settings.API_V1_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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