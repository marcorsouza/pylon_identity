from pylon.api.controllers.base_controller import BaseController
from pylon.api.middlewares.logger_middleware import log_decorator

from pylon_identity.api.admin.services.user_service import UserService


class UserController(BaseController):
    def __init__(self, user_service: UserService):
        super().__init__(user_service)

    @log_decorator
    async def add_roles_to_user(self, user_id: int, role_ids):
        return self.service.add_roles_to_user(user_id, role_ids)

    @log_decorator
    async def del_roles_to_user(self, user_id: int, role_ids):
        return self.service.del_roles_to_user(user_id, role_ids)
