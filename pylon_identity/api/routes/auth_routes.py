from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from pylon_identity.api.controllers.auth_controller import AuthController
from pylon_identity.api.services.user_service import UserService
from pylon_identity.helpers import get_session
from pylon_identity.security import create_access_token

# Criar roteador
auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

# Definir esquema de segurança
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')

user_service = None
# Função de fábrica para criar AuthController com UserService injetado
def get_auth_controller(
    session: Session = Depends(get_session),
):
    user_service = UserService(session)
    return AuthController(user_service)


# Rota de login (sem autenticação real por enquanto)
@auth_router.post('/login')
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_controller: AuthController = Depends(get_auth_controller),
):
    # Simular autenticação
    user = auth_controller.login(form_data.username, form_data.password)
    if user is None:
        return {'error': 'Usuário ou senha inválidos'}   # pragma: no cover

    access_token = create_access_token(data={'sub': user.username})

    return {'access_token': access_token, 'token_type': 'bearer'}
