from pylon.api.controllers.base_controller import BaseController

from pylon_identity.api.admin.services.role_service import RoleService


class RoleController(BaseController):
    def __init__(self, role_service: RoleService):
        super().__init__(role_service)
