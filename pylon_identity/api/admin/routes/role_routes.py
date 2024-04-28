from fastapi import APIRouter, Body, Depends
from pylon.api.schemas.message_schema import Message

from pylon_identity.api.admin.controllers.role_controller import RoleController
from pylon_identity.api.admin.dependencies import get_role_controller
from pylon_identity.api.admin.schemas.role_schema import (
    RoleAction,
    RoleList,
    RolePublic,
    RoleSchema,
    RoleUpdate,
)

# Criar roteador
role_router = APIRouter(
    prefix='/admin/roles',
    tags=['Roles'],
)

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


@role_router.post('/add_actions_to_role/{role_id}', response_model=RolePublic)
async def add_actions_to_role(
    role_id: int,
    action_in: RoleAction = Body(...),
    role_controller: RoleController = Depends(get_role_controller),
):
    return await role_controller.add_actions_to_role(role_id, action_in)


@role_router.put('/del_actions_to_role/{role_id}', response_model=RolePublic)
async def del_actions_to_role(
    role_id: int,
    action_in: RoleAction = Body(...),
    role_controller: RoleController = Depends(get_role_controller),
):
    return await role_controller.del_actions_to_role(role_id, action_in)
