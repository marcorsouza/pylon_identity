from fastapi import FastAPI

from pylon_identity.api.auth.routes.auth_routes import (  # Import roteador de usuário
    auth_router,
)


def add_api_auth_routes(app: FastAPI):
    app.include_router(auth_router)
