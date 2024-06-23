from fastapi import HTTPException, status

from ..utils import password_handlers
from ...chatbot import DatabaseSingleton


__author__ = 'Ricardo'
__version__ = '1.0'


async def verify_user(username:str, password:str):

    user_found = await get_active_user(username)
    password_matched = password_handlers.verify_password(password, user_found.password)

    if not password_matched:
        raise HTTPException(status_code=404, detail='credentials not found')
    
    return user_found


async def get_active_user(username:str):

    user_exists = await DatabaseSingleton.is_existing_user(username)

    if user_exists is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='credentials not found',
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_found = await DatabaseSingleton.get_active_user(username)

    return user_found
