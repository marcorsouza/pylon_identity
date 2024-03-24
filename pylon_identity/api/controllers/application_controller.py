from pylon.api.controllers.base_controller import BaseController

from pylon_identity.api.services.application_service import ApplicationService


class ApplicationController(BaseController):
    def __init__(self, application_service: ApplicationService):
        super().__init__(application_service)
