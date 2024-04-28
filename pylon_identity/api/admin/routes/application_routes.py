from fastapi import APIRouter, Body, Depends
from pylon.api.schemas.message_schema import Message

from pylon_identity.api.admin.controllers.application_controller import (
    ApplicationController,
)
from pylon_identity.api.admin.dependencies import get_application_controller
from pylon_identity.api.admin.schemas.application_schema import (
    ApplicationList,
    ApplicationPublic,
    ApplicationSchema,
    ApplicationUpdate,
)

# Criar roteador
application_router = APIRouter(
    prefix='/admin/applications',
    tags=['Applications'],
)


# Rota de criação de aplicação
@application_router.post(
    '/', 
    response_model=ApplicationPublic, 
    status_code=201,
    summary="Create a new application",
    description="Creates a new application with the specified details provided in the request.",
    response_description="The details of the newly created application."
)
async def create_application(
    application_in: ApplicationSchema = Body(...),
    application_controller: ApplicationController = Depends(
        get_application_controller
    ),
):
    return await application_controller.create(application_in)


# Rota de recuperação de todas as aplicações
@application_router.get(
    '/', 
    response_model=ApplicationList, 
    summary="Get all applications",
    description="Retrieves a list of all applications currently stored in the system.",
    response_description="A list containing all the applications."
)
async def get_applications(
    application_controller: ApplicationController = Depends(
        get_application_controller
    ),
):
    return await application_controller.get_all()


# Rota de recuperação de uma aplicação por ID
@application_router.get(
    '/{application_id}', 
    response_model=ApplicationPublic,
    summary="Get an application by ID",
    description="Retrieves the details of an application specified by its ID.",
    response_description="The details of the specified application."
)
async def get_application(
    application_id: int,
    application_controller: ApplicationController = Depends(
        get_application_controller
    ),
):
    return await application_controller.get_by_id(application_id)


# Rota de atualização de uma aplicação por ID
@application_router.put(
    '/{application_id}', 
    response_model=ApplicationPublic,
    summary="Update an application",
    description="Updates the details of an existing application specified by its ID.",
    response_description="The updated details of the application."
)
async def update_application(
    application_id: int,
    application_in: ApplicationUpdate = Body(...),
    application_controller: ApplicationController = Depends(
        get_application_controller
    ),
):
    return await application_controller.update(application_id, application_in)


# Rota de exclusão de uma aplicação por ID
@application_router.delete(
    '/{application_id}', 
    response_model=Message,
    summary="Delete an application",
    description="Deletes an application from the system based on the provided application ID.",
    response_description="Confirmation message of deletion."
)
async def delete_application(
    application_id: int,
    application_controller: ApplicationController = Depends(
        get_application_controller
    ),
):
    return await application_controller.delete(application_id)
