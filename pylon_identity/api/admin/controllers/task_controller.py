from pylon.api.controllers.base_controller import BaseController

from pylon_identity.api.admin.services.task_service import TaskService


class TaskController(BaseController):
    def __init__(self, task_service: TaskService):
        super().__init__(task_service)
