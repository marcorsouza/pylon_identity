# application_dependencies.py
from fastapi import Depends
from pylon.config.helpers import get_session
from sqlalchemy.orm import Session

from pylon_identity.api.admin.controllers import (
    ApplicationController,
    RoleController,
    TaskController,
    UserController,
)
from pylon_identity.api.admin.services import (
    ApplicationService,
    RoleService,
    TaskService,
    UserService,
)


def get_application_controller(
    session: Session = Depends(get_session),
) -> ApplicationController:
    application_service = ApplicationService(session)
    return ApplicationController(application_service)


def get_role_controller(
    session: Session = Depends(get_session),
) -> RoleController:
    role_service = RoleService(session)
    return RoleController(role_service)


def get_task_controller(
    session: Session = Depends(get_session),
) -> TaskController:
    task_service = TaskService(session)
    return TaskController(task_service)


def get_user_controller(
    session: Session = Depends(get_session),
) -> UserController:
    user_service = UserService(session)
    return UserController(user_service)
