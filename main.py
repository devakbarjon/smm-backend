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