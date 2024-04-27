from datetime import datetime, timezone

from pylon.api.services.base_service import BaseService
from pylon.config.exceptions.http import BadRequestException, NotFoundException
from pylon.utils.encryption_utils import encrypt_value, is_encrypted
from sqlalchemy import func
from sqlalchemy.orm import Session

from pylon_identity.api.admin.models import Role, User
from pylon_identity.api.admin.schemas.user_schema import (
    UserPublic,
    UserRole,
    UserSchema,
)


class UserService(BaseService):
    """
    Classe responsável por gerenciar operações relacionadas aos usuários.
    """

    def __init__(self, session: Session = None):
        super().__init__(session, User, UserSchema)
        self.public_schema = UserPublic

    def create(self, user_data) -> User:
        """
        Cria um novo usuário com os dados fornecidos.

        Args:
            user_data (UserSchema): Dados do usuário a serem criados.

        Returns:
            User: O usuário criado.
        """
        db_user = self._get_by_username(user_data.username)
        if db_user:
            raise BadRequestException('Username already registered')

        db_user = self._get_by_email(user_data.email)
        if db_user:
            raise BadRequestException('E-mail already registered')

        try:
            user_data.password = encrypt_value(user_data.password)
            user = User(**user_data.model_dump())
            self._create(user)
            return self._get_by_id(user.id)
        except Exception:
            raise BadRequestException('Error inserting user')

    def get_all(self):
        """
        Obtém todos os usuários.

        Returns:
            dict: Dicionário contendo todos os usuários.
        """

        results = self._get_all()
        return {'users': results}

    def get_by_id(self, user_id: int):
        """
        Obtém um usuário pelo ID.

        Args:
            user_id (int): ID do usuário a ser obtido.

        Returns:
            User: O usuário correspondente ao ID fornecido.

        Raises:
            NotFoundException: Se o usuário não for encontrado.
        """
        user = self._get_by_id(user_id)
        if user and user.id == user_id:
            return user
        raise NotFoundException('User not found.')

    def update(self, user_id: int, user_data):
        """
        Atualiza os dados de um usuário.

        Args:
            user_id (int): ID do usuário a ser atualizado.
            user_data (UserPublic): Novos dados do usuário.

        Returns:
            User: O usuário atualizado.

        Raises:
            NotFoundException: Se o usuário não for encontrado.
        """
        user = self._get_by_id(user_id)
        if not user or user_id < 1:
            raise NotFoundException('User not found.')   # pragma: no cover

        try:
            self._update(user, user_data)
            return user
        except Exception:
            raise BadRequestException('Error updating user')

    def delete(self, user_id: int):
        """
        Exclui um usuário.

        Args:
            user_id (int): ID do usuário a ser excluído.

        Returns:
            dict: Dicionário com uma mensagem indicando que o usuário foi excluído.

        Raises:
            NotFoundException: Se o usuário não for encontrado.
        """
        deleted = self._delete(user_id)

        if not deleted or user_id < 1:
            raise NotFoundException('User not found.')  # pragma: no cover

        return {'message': 'User deleted'}

    def _get_by_username(self, username):
        # Consulta o banco de dados para obter o usuário pelo username
        user = (
            self.session.query(self.model_data)
            .filter(
                func.lower(self.model_data.username) == func.lower(username)
            )
            .first()
        )
        return user

    def _get_by_email(self, email):
        # Consulta o banco de dados para obter o usuário pelo email
        user = (
            self.session.query(self.model_data)
            .filter(func.lower(self.model_data.email) == func.lower(email))
            .first()
        )
        return user

    def get_user_by_username(self, username: str):
        """
        Obtém um usuário pelo nome de usuário.

        Args:
            username (str): Nome de usuário a ser pesquisado.

        Returns:
            User: O usuário correspondente ao nome de usuário fornecido.

        Raises:
            NotFoundException: Se o usuário não for encontrado.
        """
        user = self._get_by_username(username)
        if user:
            return user
        raise NotFoundException('User not found.')

    def authenticate(self, username, password):
        """
        Método estático para autenticar um usuário com base no nome de usuário e senha fornecidos.

        Args:
            username (str): Nome de usuário (login).
            password (str): Senha do usuário.

        Returns:
            User or None: Objeto User se a autenticação for bem-sucedida, caso contrário None.
        """
        user = self.get_user_by_username(username)
        if user:
            # Verificar se a senha fornecida coincide com a senha temporária
            if (
                user.temporary_password
                and is_encrypted(password, user.temporary_password)
                and (
                    user.temporary_password_expiration is None
                    or user.temporary_password_expiration
                    >= datetime.now(timezone.utc)
                )
            ):
                return user   # pragma: no cover
            # Verificar se a senha fornecida coincide com a senha normal
            elif is_encrypted(password, user.password):
                self.clear_temporary_password(
                    user
                )  # Limpar os campos temporary_password e temporary_password_expiration
                return user
        return None

    def clear_temporary_password(self, user):
        """
        Limpa os campos temporary_password e temporary_password_expiration do usuário, removendo a senha temporária.
        """
        user.temporary_password = None
        user.temporary_password_expiration = None
        self.session.commit()

    def increment_failed_attempts(self, user):
        """
        Incrementa o número de tentativas de falha de senha do usuário.

        Se o número de tentativas exceder ou igual a 5, o usuário é bloqueado.
        """
        user.failed_pass_att_count += 1
        if user.failed_pass_att_count >= 5:
            user.is_locked_out = True   # pragma: no cover
        self.session.commit()

    def reset_failed_attempts(self, user):
        """
        Reseta o número de tentativas de falha de senha e desbloqueia o usuário.
        """
        user.failed_pass_att_count = 0
        user.is_locked_out = False
        self.session.commit()

    def update_last_login_date(self, user):
        """
        Atualiza a data do último login do usuário para o momento atual.
        """
        user.last_login_date = datetime.now(timezone.utc)
        self.session.commit()

    def add_roles_to_user(self, user_id: int, user_role: UserRole):
        user = self._get_by_id(user_id)
        if not user:
            raise NotFoundException('User not found.')

        # Extrair os IDs dos RoleSimple
        ids = [role_simple.id for role_simple in user_role.roles]

        # Buscar os papéis (roles) que correspondem aos IDs fornecidos
        roles_to_add = self.session.query(Role).filter(Role.id.in_(ids)).all()

        # Adicionando os papéis ao usuário
        for role in roles_to_add:
            if role not in user.roles:
                user.roles.append(role)

        self.session.commit()
        return self._get_by_id(user.id)

    def del_roles_to_user(self, user_id: int, user_role: UserRole):
        user = self._get_by_id(user_id)
        if not user:
            raise NotFoundException('User not found.')

        # Extrair os IDs dos RoleSimple
        ids = [role_simple.id for role_simple in user_role.roles]

        # Buscar os papéis (roles) que correspondem aos IDs fornecidos
        roles_to_remove = (
            self.session.query(Role).filter(Role.id.in_(ids)).all()
        )

        # Removendo os papéis do usuário
        for role in roles_to_remove:
            if role in user.roles:
                user.roles.remove(role)

        self.session.commit()
        return self._get_by_id(user.id)
