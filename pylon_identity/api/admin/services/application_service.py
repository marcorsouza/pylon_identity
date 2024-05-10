from pylon.api.services.base_service import BaseService
from pylon.config.exceptions.http import BadRequestException, NotFoundException
from sqlalchemy import func
from sqlalchemy.orm import Session

from pylon_identity.api.admin.models import Application
from pylon_identity.api.admin.schemas.application_schema import (
    ApplicationPublic,
    ApplicationSchema,
)


class ApplicationService(BaseService):
    """
    Classe responsável por gerenciar operações relacionadas as aplicações.
    """

    def __init__(self, session: Session = None):
        super().__init__(session, Application, ApplicationSchema)
        self.public_schema = ApplicationPublic

    def create(self, application_data) -> Application:

        """
        Cria uma nova aplicação com os dados fornecidos.

        Args:
            application_data (ApplicationSchema): Dados da aplicação a serem criados.

        Returns:
            Application: a aplicação criado.
        """

        db_application = self._find_by_acronym(application_data.acronym)
        if db_application:
            raise BadRequestException('Acronym already registered')

        try:
            application = Application(**application_data.model_dump())
            self._create(application)
            return self._find_by_id(application.id)
        except Exception:
            raise BadRequestException('Error')

    def find_all(self):
        """
        Obtém todos os aplicações.

        Returns:
            dict: Dicionário contendo todos os aplicações.
        """

        results = self._find_all()
        return {'applications': results}

    def paged_list(self, filters=None):
        return self._paged_list(filters)

    def find_by_id(self, application_id: int):
        """
        Obtém uma aplicação pelo ID.

        Args:
            application_id (int): ID da aplicação a ser obtido.

        Returns:
            Application: a aplicação correspondente ao ID fornecido.

        Raises:
            HTTPException: Se a aplicação não for encontrada.
        """
        application = self._find_by_id(application_id)
        if application and application.id == application_id:
            return application
        raise NotFoundException('Application not found.')

    def update(self, application_id: int, application_data):
        """
        Atualiza os dados de uma aplicação.

        Args:
            application_id (int): ID da aplicação a ser atualizada.
            application_data (ApplicationPublic): Novos dados da aplicação.

        Returns:
            Application: a aplicação atualizada.

        Raises:
            HTTPException: Se a aplicação não for encontrada.
        """
        application = self._find_by_id(application_id)
        if not application or application_id < 1:
            raise NotFoundException(
                'Application not found.'
            )   # pragma: no cover

        self._update(application, application_data)
        return application

    def destroy(self, application_id: int):
        """
        Exclui uma aplicação.

        Args:
            application_id (int): ID da aplicação a ser excluída.

        Returns:
            dict: Dicionário com uma mensagem indicando que a aplicação foi excluída.

        Raises:
            HTTPException: Se a aplicação não for encontrada.
        """
        deleted = self._destroy(application_id)

        if not deleted or application_id < 1:
            raise NotFoundException(
                'Application not found'
            )   # pragma: no cover

        return {'message': 'Application deleted'}

    def _find_by_acronym(self, acronym):
        # Consulta o banco de dados para obter a aplicação pelo acronym
        application = (
            self.session.query(self.model_data)
            .filter(func.lower(self.model_data.acronym) == func.lower(acronym))
            .first()
        )
        return application
