from pylon.api.controllers.base_controller import BaseController

from pylon_identity.api.admin.services.role_service import RoleService


class RoleController(BaseController):
    def __init__(self, role_service: RoleService):
        super().__init__(role_service)

    async def add_actions_to_role(self, role_id: int, action_ids):
        return self.service.add_actions_to_role(role_id, action_ids)

    async def del_actions_to_role(self, role_id: int, action_ids):
        return self.service.del_actions_to_role(role_id, action_ids)
