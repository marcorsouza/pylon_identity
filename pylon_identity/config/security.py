import datetime
from datetime import timedelta

import httpx
import pytz
from fastapi import Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pylon.api.middlewares.permission_checker import oauth2_scheme
from pylon.api.schemas.token_schema import TokenData
from pylon.config.exceptions.http import UnauthorizedException
from pylon.config.helpers import get_session
from pylon.config.settings import Settings
from sqlalchemy import select
from sqlalchemy.orm import Session

from pylon_identity.api.admin.models import User

settings = Settings()


class CustomOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    def __init__(
        self,
        username: str = Form(...),
        password: str = Form(...),
        acronym: str = Form(None),
    ):
        super().__init__(username=username, password=password)
        self.acronym = acronym


def create_access_token(data: dict):
    to_encode = data.copy()

    brt = pytz.timezone('America/Sao_Paulo')
    issued_at = datetime.datetime.now(brt) - timedelta(hours=0, minutes=1)

    expire = issued_at + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return {'access_token': encoded_jwt, 'expire': expire}


async def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
) -> User:
    credentials_exception = UnauthorizedException(
        'Could not validate credentials'
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenData(**payload)
        if token_data.username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.scalar(
        select(User).where(User.username == token_data.username)
    )

    if user is None:
        raise credentials_exception   # pragma: no cover

    return user
