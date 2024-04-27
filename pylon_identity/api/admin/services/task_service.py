from pylon.api.services.base_service import BaseService
from pylon.config.exceptions.http import BadRequestException, NotFoundException
from sqlalchemy import func
from sqlalchemy.orm import Session

from pylon_identity.api.admin.models import Action, Task
from pylon_identity.api.admin.schemas.action_schema import ActionCreate
from pylon_identity.api.admin.schemas.task_schema import TaskPublic, TaskSchema


class TaskService(BaseService):
    """
    Classe responsável por gerenciar operações relacionadas as tarefas.
    """

    def __init__(self, session: Session = None):
        super().__init__(session, Task, TaskSchema)
        self.public_schema = TaskPublic

    def get_all(self):
        """
        Obtém todos as tarefas.

        Returns:
            dict: Dicionário contendo todos as tarefas.
        """

        results = self._get_all()
        return {'tasks': results}

    def get_by_id(self, task_id: int):
        """
        Obtém uma tarefa pelo ID.

        Args:
            task_id (int): ID da tarefa a ser obtida.

        Returns:
            Task: a tarefa correspondente ao ID fornecido.

        Raises:
            HTTPException: Se a tarefa não for encontrada.
        """
        task = self._get_by_id(task_id)
        if task and task.id == task_id:
            return task
        raise NotFoundException('Task not found.')

    def create(self, task_data) -> Task:
        """
        Cria uma nova tarefa com os dados fornecidos.

        Args:
            task_data (TaskSchema): Dados da tarefa a serem criados.

        Returns:
            Task: a tarefa criado.
        """
        db_task = self._find_by_field('tag_name', task_data.tag_name)
        if db_task:
            raise BadRequestException('Tag Name already registered')

        try:
            task_dict = task_data.dict(exclude={'actions'})
            task = Task(**task_dict)

            if task_data.actions:
                for action_data in task_data.actions:
                    task.actions.append(Action(name=action_data.name))

            self._create(task)
            return self._get_by_id(task.id)
        except Exception:
            raise BadRequestException(f'Error inserting action')

    def update(self, task_id: int, task_data):
        """
        Atualiza os dados de uma tarefa.

        Args:
            task_id (int): ID da tarefa a ser atualizada.
            task_data (TaskUpdate): Novos dados da tarefa.

        Returns:
            Task: a tarefa atualizada.

        Raises:
            HTTPException: Se a tarefa não for encontrada.
        """
        task = self._get_by_id(task_id)
        if not task or task_id < 1:
            raise NotFoundException('Task not found.')   # pragma: no cover

        try:
            task_dict = task_data.dict(exclude={'actions'})
            if task:
                for key, value in task_dict.items():
                    setattr(task, key, value)

            self.session.commit()
            return task
        except Exception:
            raise BadRequestException('Error updating action')

    def delete(self, task_id: int):
        """
        Exclui uma tarefa.

        Args:
            task_id (int): ID da tarefa a ser excluída.

        Returns:
            dict: Dicionário com uma mensagem indicando que a tarefa foi excluída.

        Raises:
            HTTPException: Se a tarefa não for encontrada.
        """
        deleted = self._delete(task_id)

        if not deleted or task_id < 1:
            raise NotFoundException('Task not found.')  # pragma: no cover

        return {'message': 'Task deleted'}

    def add_action_to_task(self, task_id, action_in: ActionCreate):
        """
        Adiciona uma nova ação a uma tarefa específica.

        Args:
            task_id (int): ID da tarefa à qual a ação será adicionada.
            action_in (ActionCreate): Nome da ação a ser adicionada.

        Raises:
            BadRequestException: Se a ação já existir ou a tarefa não for encontrada.
        """
        task = self._get_by_id(task_id)
        if not task:
            raise NotFoundException('Task not found')

        # Verifica se a ação já existe na tarefa
        if any(action.name == action_in.name for action in task.actions):
            raise BadRequestException('Action already exists')

        # Adiciona a nova ação se não existir
        new_action = Action(name=action_in.name)
        task.actions.append(new_action)
        self.session.commit()
        return task

    def delete_action_from_task(self, task_id, action_in: ActionCreate):
        """
        Remove uma ação de uma tarefa específica.

        Args:
            task_id (int): ID da tarefa da qual a ação será removida.
            action_name (str): Nome da ação a ser removida.

        Raises:
            BadRequestException: Se a ação não for encontrada ou a tarefa não for encontrada.
        """
        task = self._get_by_id(task_id)
        if not task:
            raise NotFoundException('Task not found')

        # Encontra a ação pelo nome
        action_to_remove = next(
            (
                action
                for action in task.actions
                if action.name == action_in.name
            ),
            None,
        )
        if not action_to_remove:
            raise NotFoundException('Action not found')

        # Remove a ação da tarefa
        task.actions.remove(action_to_remove)
        self.session.commit()
        return task
