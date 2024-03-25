from pylon.api.controllers.base_controller import BaseController

from pylon_identity.api.admin.services.user_service import UserService


class UserController(BaseController):
    def __init__(self, user_service: UserService):
        super().__init__(user_service)
