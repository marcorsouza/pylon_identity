from unittest.mock import Mock

import pytest
from fastapi import HTTPException
from jose import jwt
from pylon.config.settings import Settings
from sqlalchemy.orm import Session

from pylon_identity.config.security import (
    create_access_token,
    get_current_user,
)


def test_jwt():
    user_info = {'username': 'manz'}
    settings = Settings()
    result = create_access_token(data=user_info)
    token = result['access_token']
    payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert payload['username'] == user_info['username']


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    # Mock da session e do token
    mock_session = Mock(spec=Session)
    mock_token = 'invalid_token'

    # Chamar o método get_current_user com um token inválido
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(session=mock_session, token=mock_token)

    # Verificar se uma exceção HTTP foi levantada
    assert exc_info.type == HTTPException
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == 'Could not validate credentials'


@pytest.mark.asyncio
async def test_get_current_user_missing_username():
    # Mock da session e do token
    mock_session = Mock(spec=Session)
    mock_token = 'token_without_username'

    # Chamar o método get_current_user com um token sem o username
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(session=mock_session, token=mock_token)

    # Verificar se uma exceção HTTP foi levantada
    assert exc_info.type == HTTPException
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == 'Could not validate credentials'


@pytest.mark.asyncio
async def test_get_current_user_user_not_found():
    # Mock da session e do token
    mock_session = Mock(spec=Session)
    mock_session.scalar.return_value = (
        None  # Simular usuário não encontrado no banco de dados
    )
    mock_token = 'valid_token'

    # Chamar o método get_current_user com um token válido, mas usuário não encontrado
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(session=mock_session, token=mock_token)

    # Verificar se uma exceção HTTP foi levantada
    assert exc_info.type == HTTPException
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == 'Could not validate credentials'
