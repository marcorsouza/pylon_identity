from fastapi import FastAPI

from pylon_identity.api.admin.routes.application_routes import (  # Import roteador de aplicações
    application_router,
)
from pylon_identity.api.admin.routes.role_routes import (  # Import roteador de regras
    role_router,
)
from pylon_identity.api.admin.routes.task_routes import (  # Import roteador de tarefas
    task_router,
)
from pylon_identity.api.admin.routes.user_routes import (  # Import roteador de usuarios
    user_router,
)


def add_api_routes(app: FastAPI):
    app.include_router(user_router)
    app.include_router(application_router)
    app.include_router(role_router)
    app.include_router(task_router)
