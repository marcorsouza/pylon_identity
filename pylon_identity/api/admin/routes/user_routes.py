from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from pylon.api.schemas.message_schema import Message

from pylon_identity.api.admin.controllers.user_controller import UserController
from pylon_identity.api.admin.dependencies import get_user_controller
from pylon_identity.api.admin.models import User
from pylon_identity.api.admin.schemas.user_schema import (
    UserList,
    UserPublic,
    UserRole,
    UserSchema,
    UserUpdate,
)
from pylon_identity.config.security import get_current_user

# Criar roteador
user_router = APIRouter(
    prefix='/admin/users',
    tags=['Users'],
)

# Definir esquema de segurança
CurrentUser = Annotated[User, Depends(get_current_user)]

# Rota de criação de usuário
@user_router.post('/', response_model=UserPublic, status_code=201,
                  summary="Create a new user",
                  description="Creates a new user with the provided user data. This route requires administrative permissions.",
                  response_description="The details of the created user.")
async def create_user(
    user_in: UserSchema = Body(...),
    user_controller: UserController = Depends(get_user_controller),
):
    return await user_controller.create(user_in)


# Rota de recuperação de todos os usuários
@user_router.get('/', response_model=UserList,
                 summary="Retrieve all users",
                 description="Retrieves a list of all users currently stored in the system. This can be accessed by admin users only.",
                 response_description="A list containing all user details.")
async def get_users(
    user_controller: UserController = Depends(get_user_controller),
):
    return await user_controller.get_all()


# Rota de recuperação de um usuário por ID
@user_router.get('/{user_id}', response_model=UserPublic,
                 summary="Get a user by ID",
                 description="Retrieves detailed information about a user by their unique ID. Access is restricted to the user themselves or an admin.",
                 response_description="Details of the user.")
async def get_user(
    user_id: int,
    user_controller: UserController = Depends(get_user_controller),
):
    return await user_controller.get_by_id(user_id)


# Rota de atualização de um usuário por ID
@user_router.put('/{user_id}', response_model=UserPublic,
                 summary="Update a user",
                 description="Updates the details of an existing user identified by their ID. Users can only update their own information unless they are an admin.",
                 response_description="The updated user details.")
async def update_user(
    user_id: int,
    user_in: UserUpdate = Body(...),
    user_controller: UserController = Depends(get_user_controller),
    current_user: CurrentUser = CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')

    return await user_controller.update(user_id, user_in)


# Rota de exclusão de um usuário por ID
@user_router.delete('/{user_id}', response_model=Message,
                    summary="Delete a user",
                    description="Deletes a user from the system based on the provided user ID. Restricted to admin users.",
                    response_description="Confirmation message of deletion.")
async def delete_user(
    user_id: int,
    user_controller: UserController = Depends(get_user_controller),
    current_user: CurrentUser = CurrentUser,
):
    return await user_controller.delete(user_id)


@user_router.post('/add_roles_to_user/{user_id}', response_model=UserPublic,
                  summary="Add roles to a user",
                  description="Adds specified roles to a user based on the user ID. Only accessible by admins.",
                  response_description="User details with updated roles.")
async def add_roles_to_user(
    user_id: int,
    user_in: UserRole = Body(...),
    user_controller: UserController = Depends(get_user_controller),
    current_user: CurrentUser = CurrentUser,
):
    return await user_controller.add_roles_to_user(user_id, user_in)


@user_router.put('/del_roles_to_user/{user_id}', response_model=UserPublic,
                 summary="Remove roles from a user",
                 description="Removes specified roles from a user based on the user ID. Only accessible by admins.",
                 response_description="User details after roles removal.")
async def del_roles_to_user(
    user_id: int,
    user_in: UserRole = Body(...),
    user_controller: UserController = Depends(get_user_controller),
    current_user: CurrentUser = CurrentUser,
):
    return await user_controller.del_roles_to_user(user_id, user_in)
