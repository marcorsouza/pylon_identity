from typing import Annotated

from fastapi import APIRouter, Body, Depends
from pylon.api.schemas.message_schema import Message
from pylon.config.helpers import get_session
from sqlalchemy.orm import Session

from pylon_identity.api.admin.controllers.application_controller import (
    ApplicationController,
)
from pylon_identity.api.admin.schemas.application_schema import (
    ApplicationList,
    ApplicationPublic,
    ApplicationSchema,
    ApplicationUpdate,
)
from pylon_identity.api.admin.services.application_service import (
    ApplicationService,
)

# Criar roteador
application_router = APIRouter(
    prefix='/admin/applications',
    tags=['Applications'],
)

application_service = None

CurrentSession = Annotated[Session, Depends(get_session)]
# Função de fábrica para criar ApplicationController com ApplicationService injetado
def get_application_controller(
    session: CurrentSession,
):
    application_service = ApplicationService(session)
    return ApplicationController(application_service)


# Rota de criação de aplicação
@application_router.post(
    '/', response_model=ApplicationPublic, status_code=201
)
async def create_application(
    application_in: ApplicationSchema = Body(...),
    application_controller: ApplicationController = Depends(
        get_application_controller
    ),
):
    return await application_controller.create(application_in)


# Rota de recuperação de todas as aplicações
@application_router.get('/', response_model=ApplicationList)
async def get_applications(
    application_controller: ApplicationController = Depends(
        get_application_controller
    ),
):
    return await application_controller.get_all()


# Rota de recuperação de uma aplicação por ID
@application_router.get('/{application_id}', response_model=ApplicationPublic)
async def get_application(
    application_id: int,
    application_controller: ApplicationController = Depends(
        get_application_controller
    ),
):
    return await application_controller.get_by_id(application_id)


# Rota de atualização de uma aplicação por ID
@application_router.put('/{application_id}', response_model=ApplicationPublic)
async def update_application(
    application_id: int,
    application_in: ApplicationUpdate = Body(...),
    application_controller: ApplicationController = Depends(
        get_application_controller
    ),
):
    return await application_controller.update(application_id, application_in)


# Rota de exclusão de uma aplicação por ID
@application_router.delete('/{application_id}', response_model=Message)
async def delete_application(
    application_id: int,
    application_controller: ApplicationController = Depends(
        get_application_controller
    ),
):
    return await application_controller.delete(application_id)
