from datetime import datetime, timedelta, timezone
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import jwt

from fastapi.exceptions import HTTPException

from app.api.authentication.models.user import UserModel
from app import config


__author__ = "Ricardo Robledo"
__version__ = "1.0"
__all__ = ["create_code", "create_gpt_tokens", "create_tokens"]


def create_tokens(user:UserModel):
    """
    This function creates our access and refresh tokens for our application

    :param token: a jwt token with user information
    :return: a tuple with our access and refresh tokens
    """

    payload = {
        "id": user.id,
        "username": user.username,
    }

    access_token = jwt.encode({**payload, 'exp':datetime.now(timezone.utc)+timedelta(seconds=config.ACCESS_TOKEN_EXPIRE_SECONDS)}, config.SECRET_KEY, algorithm=config.HASH_ALGORITHM)
    refresh_token = jwt.encode({**payload, 'exp':datetime.now(timezone.utc)+timedelta(seconds=config.REFRESH_TOKEN_EXPIRE_SECONDS)}, config.SECRET_KEY, algorithm=config.HASH_ALGORITHM)

    return access_token, refresh_token


def decode_token(token:str):
    """
    This function verify that a token is valid

    :param token: a jwt token with user information
    :return: a decoded jwt token
    """

    try:

        return jwt.decode(token, config.SECRET_KEY, algorithms=[config.HASH_ALGORITHM])

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token has expired')
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')
