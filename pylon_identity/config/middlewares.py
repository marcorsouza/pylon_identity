from fastapi import FastAPI
from pylon.api.middlewares.auth_middleware import AuthMiddleware

allow_routes = [
    '/auth/login',
]


def add_api_middlewares(app: FastAPI):
    app.add_middleware(AuthMiddleware, allow_routes=allow_routes)
