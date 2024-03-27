from pylon.api.services.base_service import BaseService
from pylon.config.exceptions.http import BadRequestException, NotFoundException
from sqlalchemy import func
from sqlalchemy.orm import Session

from pylon_identity.api.admin.models import Task,Action
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
        db_task = self._get_by_tag_name(task_data.tag_name)
        if db_task:
            raise BadRequestException('Tag Name already registered')
        
        task_dict = task_data.dict(exclude={'actions'})
        task = Task(**task_dict)
        
        if task_data.actions:
            for action_data in task_data.actions:
                task.actions.append(Action(name = action_data.name))
        
           
        self._create(task)
        return self._get_by_id(task.id)

    def update(self, task_id: int, task_data):
        """
        Atualiza os dados de uma tarefa.

        Args:
            task_id (int): ID da tarefa a ser atualizada.
            task_data (TaskPublic): Novos dados da tarefa.

        Returns:
            Task: a tarefa atualizada.

        Raises:
            HTTPException: Se a tarefa não for encontrada.
        """
        task = self._get_by_id(task_id)
        if not task or task_id < 1:
            raise NotFoundException('Task not found.')   # pragma: no cover

        task_dict = task_data.dict(exclude={'actions'})
        if task:            
            for key, value in task_dict.items():
                setattr(task,key, value)
                
        task.actions.clear()
        if task_data.actions:
            for action_data in task_data.actions:
                task.actions.append(Action(name = action_data.name))
                   
        self.session.commit()
        return task

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

    def _get_by_tag_name(self, tag_name):
        # Consulta o banco de dados para obter a tarefa pelo tag_name
        task = (
            self.session.query(self.model_data)
            .filter(
                func.lower(self.model_data.tag_name) == func.lower(tag_name)
            )
            .first()
        )
        return task
