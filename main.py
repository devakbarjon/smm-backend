from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.database.base import init_models

from app.core.config import settings
from app.core.exceptions import http_error_handler, validation_error_handler
from app.core.logging import logger

from app.api.v1.router import router as api_v1_router

from app.services.telegram.bot_base import bot


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()  # Initialize database models
    yield
    await bot.session.close()
    logger.info("Shutting down...")


app = FastAPI(lifespan=lifespan)

app.include_router(api_v1_router, prefix=settings.API_V1_STR)

app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)