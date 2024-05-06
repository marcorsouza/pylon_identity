from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pylon.api.middlewares.auth_middleware import AuthMiddleware

allow_routes = [
    '/auth/login',
    '/health',
    '/docs',
    '/openapi.json',
    '/do_login',
]


def add_api_middlewares(app: FastAPI):
    add_auth_middleware(app)
    add_cors_middleware(app)


def add_auth_middleware(app: FastAPI):
    app.add_middleware(AuthMiddleware, allow_routes=allow_routes)


def add_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            '*'
        ],  # Lista de origens permitidas, use domínios específicos em produção
        allow_credentials=True,
        allow_methods=['*'],  # Métodos HTTP permitidos
        allow_headers=['*'],  # Headers HTTP permitidos
    )
