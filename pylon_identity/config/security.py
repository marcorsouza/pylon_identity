from datetime import timedelta
import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pylon.config.helpers import get_session
from pylon.config.settings import Settings
from sqlalchemy import select
from sqlalchemy.orm import Session
import pytz

from pylon_identity.api.admin.models import User
from pylon_identity.api.admin.schemas.token_schema import TokenData

settings = Settings()


def create_access_token(data: dict):
    to_encode = data.copy()
    
    brt = pytz.timezone('America/Sao_Paulo')
    issued_at = datetime.datetime.now(brt) - timedelta(hours=0, minutes = 1)
    
    expire = issued_at + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return {'access_token': encoded_jwt, 'expire': expire}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


async def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception   # pragma: no cover
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = session.scalar(
        select(User).where(User.username == token_data.username)
    )

    if user is None:
        raise credentials_exception   # pragma: no cover

    return user
