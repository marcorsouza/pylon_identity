from pylon.config.exceptions.http import BadRequestException

from pylon_identity.api.admin.services.user_service import UserService
from pylon_identity.api.auth.schemas.auth_schema import CheckPermissionSchema
from pylon.api.middlewares.logger_middleware import log_decorator


class AuthController:
    def __init__(self, user_service: UserService):
        super().__init__()
        self.user_service = user_service

    @log_decorator
    async def login(self, username, password):
        return self.__authenticate_user(username, password)

    @log_decorator
    async def check_permission(self, data: CheckPermissionSchema):
        result = self.user_service.check_permission(data)
        if(result):
            return {'message': 'OK'}
        
        raise BadRequestException('User does not have permission for this action.')

    # Funções auxiliares (substituem acesso a banco de dados)
    def __authenticate_user(self, username: str, password: str):

        user_by_username = self.user_service.get_user_by_username(username)
        if user_by_username.is_locked():
            raise BadRequestException('User is locked out. Please contact the administrator.')

        user = self.user_service.authenticate(username, password)
        if user is None:
            if user_by_username:
                self.user_service.increment_failed_attempts(user_by_username)
                remaining_attempts = max(
                    0, 5 - user_by_username.failed_pass_att_count
                )
                raise BadRequestException(f'Invalid username or password, remaining_attempts: {remaining_attempts}')

            raise BadRequestException('Invalid username or password')

        self.user_service.update_last_login_date(user)
        self.user_service.reset_failed_attempts(user)
        return user
