from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pylon.api.schemas.message_schema import Message
from pylon.config.helpers import get_session
from sqlalchemy.orm import Session

from pylon_identity.api.admin.controllers.user_controller import UserController
from pylon_identity.api.admin.models import User
from pylon_identity.api.admin.schemas.user_schema import (
    UserList,
    UserPublic,
    UserRole,
    UserSchema,
    UserUpdate,
)
from pylon_identity.api.admin.services.user_service import UserService
from pylon_identity.config.security import get_current_user

# Criar roteador
user_router = APIRouter(
    prefix='/admin/users',
    tags=['Users'],
)

# Definir esquema de segurança
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')
user_service = None

CurrentSession = Annotated[Session, Depends(get_session)]
# Função de fábrica para criar UserController com UserService injetado
def get_user_controller(
    session: CurrentSession,
):
    user_service = UserService(session)
    return UserController(user_service)


CurrentUser = Annotated[User, Depends(get_current_user)]

# Rota de criação de usuário
@user_router.post('/', response_model=UserPublic, status_code=201)
async def create_user(
    user_in: UserSchema = Body(...),
    user_controller: UserController = Depends(get_user_controller),
):
    return await user_controller.create(user_in)


# Rota de recuperação de todos os usuários
@user_router.get('/', response_model=UserList)
async def get_users(
    user_controller: UserController = Depends(get_user_controller),
):
    return await user_controller.get_all()


# Rota de recuperação de um usuário por ID
@user_router.get('/{user_id}', response_model=UserPublic)
async def get_user(
    user_id: int,
    user_controller: UserController = Depends(get_user_controller),
):
    return await user_controller.get_by_id(user_id)


# Rota de atualização de um usuário por ID
@user_router.put('/{user_id}', response_model=UserPublic)
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
@user_router.delete('/{user_id}', response_model=Message)
async def delete_user(
    user_id: int,
    user_controller: UserController = Depends(get_user_controller),
    current_user: CurrentUser = CurrentUser,
):
    return await user_controller.delete(user_id)


@user_router.post('/add_roles_to_user/{user_id}', response_model=UserPublic)
async def add_roles_to_user(
    user_id: int,
    user_in: UserRole = Body(...),
    user_controller: UserController = Depends(get_user_controller),
    current_user: CurrentUser = CurrentUser,
):
    return await user_controller.add_roles_to_user(user_id, user_in)

@user_router.put('/del_roles_to_user/{user_id}', response_model=UserPublic)
async def del_roles_to_user(
    user_id: int,
    user_in: UserRole = Body(...),
    user_controller: UserController = Depends(get_user_controller),
    current_user: CurrentUser = CurrentUser,
):
    return await user_controller.del_roles_to_user(user_id, user_in)