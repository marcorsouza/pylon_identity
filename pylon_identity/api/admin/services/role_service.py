from pylon.api.services.base_service import BaseService
from pylon.config.exceptions.http import BadRequestException, NotFoundException
from sqlalchemy.orm import Session

from pylon_identity.api.admin.models import Action, Role
from pylon_identity.api.admin.schemas.role_schema import (
    RoleAction,
    RolePublic,
    RoleSchema,
)


class RoleService(BaseService):
    """
    Classe responsável por gerenciar operações relacionadas as regras.
    """

    def __init__(self, session: Session = None):
        super().__init__(session, Role, RoleSchema)
        self.public_schema = RolePublic

    def create(self, role_data) -> Role:
        """
        Cria uma nova regra com os dados fornecidos.

        Args:
            role_data (RoleSchema): Dados da regra a serem criados.

        Returns:
            Role: a regra criada.
        """
        try:
            role = Role(**role_data.model_dump())
            self._create(role)
            return self._get_by_id(role.id)
        except Exception:
            raise BadRequestException('Error inserting role')

    def get_all(self):
        """
        Obtém todos as regras.

        Returns:
            dict: Dicionário contendo todos as regras.
        """

        results = self._get_all()
        return {'roles': results}

    def paged_list(self, filters=None):
        return self._paged_list(filters)

    def get_by_id(self, role_id: int):
        """
        Obtém uma regra pelo ID.

        Args:
            role_id (int): ID da regra a ser obtido.

        Returns:
            Role: a regra correspondente ao ID fornecido.

        Raises:
            HTTPException: Se a regra não for encontrada.
        """
        role = self._get_by_id(role_id)
        if role and role.id == role_id:
            return role
        raise NotFoundException('Role not found.')

    def update(self, role_id: int, role_data):
        """
        Atualiza os dados de uma regra.

        Args:
            role_id (int): ID da regra a ser atualizada.
            role_data (RolePublic): Novos dados da regra.

        Returns:
            Role: a regra atualizada.

        Raises:
            HTTPException: Se a regra não for encontrada.
        """
        try:
            role = self._get_by_id(role_id)
            if not role or role_id < 1:
                raise NotFoundException('Role not found.')   # pragma: no cover

            self._update(role, role_data)
            return role
        except Exception:
            raise BadRequestException('Error updating role')

    def delete(self, role_id: int):
        """
        Exclui uma regra.

        Args:
            role_id (int): ID da regra a ser excluída.

        Returns:
            dict: Dicionário com uma mensagem indicando que a regra foi excluída.

        Raises:
            HTTPException: Se a regra não for encontrada.
        """
        deleted = self._delete(role_id)

        if not deleted or role_id < 1:
            raise NotFoundException('Role not found')   # pragma: no cover

        return {'message': 'Role deleted'}

    def add_actions_to_role(self, role_id: int, role_action: RoleAction):
        role = self._get_by_id(role_id)
        if not role:
            raise NotFoundException('Role not found')

        # Extrair os IDs dos ActionSimple
        ids = [action_simple.id for action_simple in role_action.actions]

        # Buscar os papéis (actions) que correspondem aos IDs fornecidos
        actions_to_add = (
            self.session.query(Action).filter(Action.id.in_(ids)).all()
        )

        # Adicionando os papéis a regra
        for action in actions_to_add:
            if action not in role.actions:
                role.actions.append(action)

        self.session.commit()
        return self._get_by_id(role.id)

    def del_actions_to_role(self, role_id: int, role_action: RoleAction):
        role = self._get_by_id(role_id)
        if not role:
            raise NotFoundException('Role not found')

        # Extrair os IDs dos ActionSimple
        ids = [action_simple.id for action_simple in role_action.actions]

        # Buscar os papéis (actions) que correspondem aos IDs fornecidos
        actions_to_remove = (
            self.session.query(Action).filter(Action.id.in_(ids)).all()
        )

        # Removendo os papéis da regra
        for action in actions_to_remove:
            if action in role.actions:
                role.actions.remove(action)

        self.session.commit()
        return self._get_by_id(role.id)
