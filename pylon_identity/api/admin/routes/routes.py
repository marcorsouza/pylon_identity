from fastapi import FastAPI

from pylon_identity.api.admin.routes.application_routes import (  # Import roteador de usuário
    application_router,
)
from pylon_identity.api.admin.routes.user_routes import (  # Import roteador de usuário
    user_router,
)


def add_api_routes(app: FastAPI):
    app.include_router(user_router)
    app.include_router(application_router)
