from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pylon.api.schemas.message_schema import Message

from pylon_identity.api.admin.schemas.user_schema import TokenAndUserPublic
from pylon_identity.api.auth.controllers.auth_controller import AuthController
from pylon_identity.api.auth.schemas.auth_schema import CheckPermissionSchema
from pylon_identity.config.dependencies import get_auth_controller
from pylon_identity.config.security import create_access_token

# Criar roteador
auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

# Rota de login (sem autenticação real por enquanto)
@auth_router.post(
    '/login',
    response_model=TokenAndUserPublic,
    summary='Authenticate a user',
    description='Performs authentication for a user using username and password credentials. If successful, it returns an access token and user details.',
    response_description='The authentication token along with public user details.',
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_controller: AuthController = Depends(get_auth_controller),
):
    # Simular autenticação
    user = await auth_controller.login(form_data.username, form_data.password)
    if user is None:
        return {'error': 'Usuário ou senha inválidos'}   # pragma: no cover

    user_info = {
        'username': user.username,
        'acronym': 'APS'  # app_by_acronym.acronym
        # outras informações que você deseja incluir no token
    }

    token_data = create_access_token(data=user_info)
    access_token = token_data['access_token']
    expire = token_data['expire']

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'expire_at': expire,
        'user': user,  # Formato de data e hora como string
    }


@auth_router.post(
    '/check-permission',
    response_model=Message,
    summary='Check user permissions',
    description='Checks if the authenticated user has permission to perform a specific action on a resource, based on provided data including username, tag name, acronym, and action name.',
    response_description='A message indicating if the user has the required permission.',
)
async def check_user_permission(
    permission_data: CheckPermissionSchema = Body(...),
    auth_controller: AuthController = Depends(get_auth_controller),
):
    # Utilizar o método check_permission do AuthController para verificar a permissão
    result = await auth_controller.check_permission(permission_data)

    return result
