from fastapi import APIRouter, Body, Depends
from pylon.api.middlewares.permission_middleware import PermissionChecker
from pylon.api.schemas.message_schema import Message

from pylon_identity.api.admin.controllers.task_controller import TaskController
from pylon_identity.api.admin.schemas.action_schema import ActionCreate
from pylon_identity.api.admin.schemas.task_schema import (
    TaskList,
    TaskPagedList,
    TaskPublic,
    TaskSchema,
    TaskUpdate,
)
from pylon_identity.config.dependencies import get_task_controller

# Criar roteador
task_routes = APIRouter(
    prefix='/admin/tasks',
    tags=['Tasks'],
)

# Rota de criação de aplicação
@task_routes.post(
    '/',
    dependencies=[Depends(PermissionChecker('CREATE', 'TASKS'))],
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
@task_routes.get(
    '/',
    dependencies=[Depends(PermissionChecker('READ', 'TASKS'))],
    response_model=TaskList,
    summary='Retrieve all tasks',
    description='Retrieves a list of all tasks currently stored in the system.',
    response_description='A list containing all the tasks.',
)
async def get_tasks(
    task_controller: TaskController = Depends(get_task_controller),
):
    return await task_controller.find_all()


@task_routes.post(
    '/paged-list',
    dependencies=[Depends(PermissionChecker('READ', 'TASKS'))],
    response_model=TaskPagedList,
    summary='Paginated task retrieval',
    description='Retrieves a paginated list of all tasks currently stored in the system. This endpoint is intended for administrative use only and allows for filtering and pagination of task records.',
    response_description='A paginated list containing task details, including metadata about the pagination such as current page and total records.',
)
async def paged_list(
    filters: dict,
    task_controller: TaskController = Depends(get_task_controller),
):
    return await task_controller.paged_list(filters)


# Rota de recuperação de uma aplicação por ID
@task_routes.get(
    '/{task_id}',
    dependencies=[Depends(PermissionChecker('READ', 'TASKS'))],
    response_model=TaskPublic,
    summary='Get a task by ID',
    description='Retrieves a task by its unique ID.',
    response_description='Details of the task.',
)
async def get_task(
    task_id: int,
    task_controller: TaskController = Depends(get_task_controller),
):
    return await task_controller.find_by_id(task_id)


# Rota de atualização de uma aplicação por ID
@task_routes.put(
    '/{task_id}',
    dependencies=[Depends(PermissionChecker('UPDATE', 'TASKS'))],
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
@task_routes.delete(
    '/{task_id}',
    dependencies=[Depends(PermissionChecker('DELETE', 'TASKS'))],
    response_model=Message,
    summary='Delete a task',
    description='Deletes a task from the system based on the provided task ID.',
    response_description='Confirmation message of deletion.',
)
async def destroy_task(
    task_id: int,
    task_controller: TaskController = Depends(get_task_controller),
):
    return await task_controller.delete(task_id)


@task_routes.post(
    '/add_action_to_task/{task_id}',
    dependencies=[Depends(PermissionChecker('CREATE_ACTIONS', 'TASKS'))],
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


@task_routes.put(
    '/delete_action_from_task/{task_id}',
    dependencies=[Depends(PermissionChecker('DELETE_ACTIONS', 'TASKS'))],
    response_model=TaskPublic,
    summary='Remove an action from a task',
    description='Removes a specified action from a task based on the task ID.',
    response_description='Task details after the action removal.',
)
async def destroy_action_from_task(
    task_id: int,
    action_in: ActionCreate = Body(...),
    task_controller: TaskController = Depends(get_task_controller),
):
    return await task_controller.delete_action_from_task(task_id, action_in)
