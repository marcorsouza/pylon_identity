from fastapi import APIRouter, Body, Depends
from pylon.api.schemas.message_schema import Message

from pylon_identity.api.admin.controllers.task_controller import TaskController
from pylon_identity.api.dependencies import get_task_controller
from pylon_identity.api.admin.schemas.action_schema import ActionCreate
from pylon_identity.api.admin.schemas.task_schema import (
    TaskList,
    TaskPublic,
    TaskSchema,
    TaskUpdate,
)

# Criar roteador
task_router = APIRouter(
    prefix='/admin/tasks',
    tags=['Tasks'],
)

# Rota de criação de aplicação
@task_router.post(
    '/',
    response_model=TaskPublic,
    status_code=201,
    summary='Create a new task',
    description='Creates a new task with the provided task data.',
    response_description='The details of the newly created task.',
)
async def create_task(
    task_in: TaskSchema = Body(...),
    task_controller: TaskController = Depends(get_task_controller),
):
    return await task_controller.create(task_in)


# Rota de recuperação de todas as aplicações
@task_router.get(
    '/',
    response_model=TaskList,
    summary='Retrieve all tasks',
    description='Retrieves a list of all tasks currently stored in the system.',
    response_description='A list containing all the tasks.',
)
async def get_tasks(
    task_controller: TaskController = Depends(get_task_controller),
):
    return await task_controller.get_all()


# Rota de recuperação de uma aplicação por ID
@task_router.get(
    '/{task_id}',
    response_model=TaskPublic,
    summary='Get a task by ID',
    description='Retrieves a task by its unique ID.',
    response_description='Details of the task.',
)
async def get_task(
    task_id: int,
    task_controller: TaskController = Depends(get_task_controller),
):
    return await task_controller.get_by_id(task_id)


# Rota de atualização de uma aplicação por ID
@task_router.put(
    '/{task_id}',
    response_model=TaskPublic,
    summary='Update a task',
    description='Updates the details of an existing task identified by its ID.',
    response_description='The updated task details.',
)
async def update_task(
    task_id: int,
    task_in: TaskUpdate = Body(...),
    task_controller: TaskController = Depends(get_task_controller),
):
    return await task_controller.update(task_id, task_in)


# Rota de exclusão de uma aplicação por ID
@task_router.delete(
    '/{task_id}',
    response_model=Message,
    summary='Delete a task',
    description='Deletes a task from the system based on the provided task ID.',
    response_description='Confirmation message of deletion.',
)
async def delete_task(
    task_id: int,
    task_controller: TaskController = Depends(get_task_controller),
):
    return await task_controller.delete(task_id)


@task_router.post(
    '/add_action_to_task/{task_id}',
    response_model=TaskPublic,
    summary='Add an action to a task',
    description='Adds a specified action to a task based on the task ID.',
    response_description='Task details with the newly added action.',
)
async def add_action_to_task(
    task_id: int,
    action_in: ActionCreate = Body(...),
    task_controller: TaskController = Depends(get_task_controller),
):
    return await task_controller.add_action_to_task(task_id, action_in)


@task_router.put(
    '/delete_action_from_task/{task_id}',
    response_model=TaskPublic,
    summary='Remove an action from a task',
    description='Removes a specified action from a task based on the task ID.',
    response_description='Task details after the action removal.',
)
async def delete_action_from_task(
    task_id: int,
    action_in: ActionCreate = Body(...),
    task_controller: TaskController = Depends(get_task_controller),
):
    return await task_controller.delete_action_from_task(task_id, action_in)
