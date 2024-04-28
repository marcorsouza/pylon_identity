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
@role_router.post('/', response_model=RolePublic, status_code=201,
                  summary="Create a new role",
                  description="Creates a new role with the provided role data.",
                  response_description="The details of the created role.")
async def create_role(
    role_in: RoleSchema = Body(...),
    role_controller: RoleController = Depends(get_role_controller),
):
    return await role_controller.create(role_in)


# Rota de recuperação de todas as regras
@role_router.get('/', response_model=RoleList,
                 summary="Retrieve all roles",
                 description="Retrieves a list of all roles in the system.",
                 response_description="A list containing all roles.")
async def get_roles(
    role_controller: RoleController = Depends(get_role_controller),
):
    return await role_controller.get_all()


# Rota de recuperação de uma regra por ID
@role_router.get('/{role_id}', response_model=RolePublic,
                 summary="Get a role by ID",
                 description="Retrieves a role by its unique ID.",
                 response_description="Details of the role.")
async def get_role(
    role_id: int,
    role_controller: RoleController = Depends(get_role_controller),
):
    return await role_controller.get_by_id(role_id)


# Rota de atualização de uma regra por ID
@role_router.put('/{role_id}', response_model=RolePublic,
                 summary="Update a role",
                 description="Updates the details of an existing role identified by its ID.",
                 response_description="The updated role details.")
async def update_role(
    role_id: int,
    role_in: RoleUpdate = Body(...),
    role_controller: RoleController = Depends(get_role_controller),
):
    return await role_controller.update(role_id, role_in)


# Rota de exclusão de uma regra por ID
@role_router.delete('/{role_id}', response_model=Message,
                    summary="Delete a role",
                    description="Deletes a role from the system based on the provided role ID.",
                    response_description="Confirmation message of deletion.")
async def delete_role(
    role_id: int,
    role_controller: RoleController = Depends(get_role_controller),
):
    return await role_controller.delete(role_id)


@role_router.post('/add_actions_to_role/{role_id}', response_model=RolePublic,
                  summary="Add actions to a role",
                  description="Adds specified actions to a role based on the role ID.",
                  response_description="Role details with updated actions.")
async def add_actions_to_role(
    role_id: int,
    action_in: RoleAction = Body(...),
    role_controller: RoleController = Depends(get_role_controller),
):
    return await role_controller.add_actions_to_role(role_id, action_in)


@role_router.put('/del_actions_to_role/{role_id}', response_model=RolePublic,
                 summary="Remove actions from a role",
                 description="Removes specified actions from a role based on the role ID.",
                 response_description="Role details after actions removal.")
async def del_actions_to_role(
    role_id: int,
    action_in: RoleAction = Body(...),
    role_controller: RoleController = Depends(get_role_controller),
):
    return await role_controller.del_actions_to_role(role_id, action_in)
