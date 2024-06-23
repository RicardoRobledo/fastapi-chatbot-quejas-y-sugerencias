from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from ..utils import token_handlers, authentication_handlers


__author__ = 'Ricardo'
__version__ = '1.0'
__all__ = ['oauth2_scheme', 'get_active_user']


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/oauth/login")


async def get_active_user(token:str=Depends(oauth2_scheme)):

    decoded_token = token_handlers.decode_token(token)
    user_found = await authentication_handlers.get_active_user(decoded_token['username'])

    return user_found
