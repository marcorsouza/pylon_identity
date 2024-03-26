from typing import Annotated

from fastapi import APIRouter, Body, Depends
from pylon.api.schemas.message_schema import Message
from pylon.config.helpers import get_session
from sqlalchemy.orm import Session

from pylon_identity.api.admin.controllers.task_controller import TaskController
from pylon_identity.api.admin.schemas.task_schema import (
    TaskList,
    TaskPublic,
    TaskSchema,
    TaskUpdate,
)
from pylon_identity.api.admin.services.task_service import TaskService

# Criar roteador
task_router = APIRouter(
    prefix='/admin/tasks',
    tags=['Tasks'],
)

task_service = None

CurrentSession = Annotated[Session, Depends(get_session)]
# Função de fábrica para criar TaskController com TaskService injetado
def get_task_controller(
    session: CurrentSession,
):
    task_service = TaskService(session)
    return TaskController(task_service)


# Rota de criação de aplicação
@task_router.post('/', response_model=TaskPublic, status_code=201)
async def create_task(
    task_in: TaskSchema = Body(...),
    task_controller: TaskController = Depends(get_task_controller),
):
    return await task_controller.create(task_in)


# Rota de recuperação de todas as aplicações
@task_router.get('/', response_model=TaskList)
async def get_tasks(
    task_controller: TaskController = Depends(get_task_controller),
):
    return await task_controller.get_all()


# Rota de recuperação de uma aplicação por ID
@task_router.get('/{task_id}', response_model=TaskPublic)
async def get_task(
    task_id: int,
    task_controller: TaskController = Depends(get_task_controller),
):
    return await task_controller.get_by_id(task_id)


# Rota de atualização de uma aplicação por ID
@task_router.put('/{task_id}', response_model=TaskPublic)
async def update_task(
    task_id: int,
    task_in: TaskUpdate = Body(...),
    task_controller: TaskController = Depends(get_task_controller),
):
    return await task_controller.update(task_id, task_in)


# Rota de exclusão de uma aplicação por ID
@task_router.delete('/{task_id}', response_model=Message)
async def delete_task(
    task_id: int,
    task_controller: TaskController = Depends(get_task_controller),
):
    return await task_controller.delete(task_id)
