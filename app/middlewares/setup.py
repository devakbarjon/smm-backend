from fastapi import FastAPI
from .cors_middleware import setup_cors
from .request_middleware import log_requests


def setup_middlewares(app: FastAPI):
    setup_cors(app)
    app.middleware("http")(log_requests)
