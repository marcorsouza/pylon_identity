from fastapi import HTTPException
from pylon.api.services.base_service import BaseService
from sqlalchemy.orm import Session

from pylon_identity.api.admin.models import Role
from pylon_identity.api.admin.schemas.role_schema import RolePublic, RoleSchema


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

        role = Role(**role_data.model_dump())
        self._create(role)
        return self._get_by_id(role.id)

    def get_all(self):
        """
        Obtém todos as regras.

        Returns:
            dict: Dicionário contendo todos as regras.
        """

        results = self._get_all()
        return {'roles': results}

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
        raise HTTPException(status_code=404, detail='Role not found.')

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
        role = self._get_by_id(role_id)
        if not role or role_id < 1:
            raise HTTPException(
                status_code=404, detail='Role not found.'
            )   # pragma: no cover

        self._update(role, role_data)
        return role

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
            raise HTTPException(
                status_code=404, detail='Role not found'
            )   # pragma: no cover

        return {'message': 'Role deleted'}
