from fastapi import HTTPException

from pylon_identity.api.admin.services.user_service import UserService


class AuthController:
    def __init__(self, user_service: UserService):
        super().__init__()
        self.user_service = user_service

    def login(self, username, password):
        return self.__authenticate_user(username, password)

    # Funções auxiliares (substituem acesso a banco de dados)
    def __authenticate_user(self, username: str, password: str):

        user_by_username = self.user_service.get_user_by_username(username)
        if user_by_username.is_locked():
            raise HTTPException(
                status_code=400,
                detail='User is locked out. Please contact the administrator.',
            )

        user = self.user_service.authenticate(username, password)
        if user is None:
            if user_by_username:
                self.user_service.increment_failed_attempts(user_by_username)
                remaining_attempts = max(
                    0, 5 - user_by_username.failed_pass_att_count
                )
                raise HTTPException(
                    status_code=400,
                    detail=f'Invalid username or password, remaining_attempts: {remaining_attempts}',
                )

            raise HTTPException(  # pragma: no cover
                status_code=400, detail='Invalid username or password'
            )

        self.user_service.update_last_login_date(user)
        self.user_service.reset_failed_attempts(user)
        return user
