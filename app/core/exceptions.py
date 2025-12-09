from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from fastapi import Request, status
from app.schemas.base import ResponseSchema


async def http_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseSchema(
            success=False,
            message=exc.detail,
            data=None
        ).model_dump()
    )


async def not_found_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=ResponseSchema(
            success=False,
            message="The requested resource was not found.",
            data=None
        ).model_dump()
    )


async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ResponseSchema(
            success=False,
            message="Validation error",
            data=exc.errors()
        ).model_dump()
    )
