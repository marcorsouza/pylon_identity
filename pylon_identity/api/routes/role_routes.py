from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from pylon_identity.api.controllers.role_controller import RoleController
from pylon_identity.api.schemas.message_schema import Message
from pylon_identity.api.schemas.role_schema import (
    RoleList,
    RolePublic,
    RoleSchema,
    RoleUpdate,
)
from pylon_identity.api.services.role_service import RoleService
from pylon_identity.helpers import get_session

# Criar roteador
role_router = APIRouter(
    prefix='/roles',
    tags=['Roles'],
)

role_service = None

CurrentSession = Annotated[Session, Depends(get_session)]
# Função de fábrica para criar RoleController com RoleService injetado
def get_role_controller(
    session: CurrentSession,
):
    role_service = RoleService(session)
    return RoleController(role_service)


# Rota de criação de regra
@role_router.post('/', response_model=RolePublic, status_code=201)
async def create_role(
    role_in: RoleSchema = Body(...),
    role_controller: RoleController = Depends(get_role_controller),
):
    return await role_controller.create(role_in)


# Rota de recuperação de todas as regras
@role_router.get('/', response_model=RoleList)
async def get_roles(
    role_controller: RoleController = Depends(get_role_controller),
):
    return await role_controller.get_all()


# Rota de recuperação de uma regra por ID
@role_router.get('/{role_id}', response_model=RolePublic)
async def get_role(
    role_id: int,
    role_controller: RoleController = Depends(get_role_controller),
):
    return await role_controller.get_by_id(role_id)


# Rota de atualização de uma regra por ID
@role_router.put('/{role_id}', response_model=RolePublic)
async def update_role(
    role_id: int,
    role_in: RoleUpdate = Body(...),
    role_controller: RoleController = Depends(get_role_controller),
):
    return await role_controller.update(role_id, role_in)


# Rota de exclusão de uma regra por ID
@role_router.delete('/{role_id}', response_model=Message)
async def delete_role(
    role_id: int,
    role_controller: RoleController = Depends(get_role_controller),
):
    return await role_controller.delete(role_id)
