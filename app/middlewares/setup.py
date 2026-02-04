from fastapi import FastAPI
from .cors_middleware import setup_cors
from .request_middleware import log_requests
from .admin_middleware import AdminAuthMiddleware


def setup_middlewares(app: FastAPI):
    setup_cors(app)
    app.add_middleware(AdminAuthMiddleware)
    app.middleware("http")(log_requests)
