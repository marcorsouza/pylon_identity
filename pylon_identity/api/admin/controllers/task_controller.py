from pylon.api.controllers.base_controller import BaseController
from pylon.api.middlewares.logger_middleware import log_decorator

from pylon_identity.api.admin.services.task_service import TaskService


class TaskController(BaseController):
    def __init__(self, task_service: TaskService):
        super().__init__(task_service)

    @log_decorator
    async def add_action_to_task(self, task_id: int, action_name):
        return self.service.add_action_to_task(task_id, action_name)

    @log_decorator
    async def destroy_action_from_task(self, task_id: int, action_name):
        return self.service.delete_action_from_task(task_id, action_name)
