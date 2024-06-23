from typing import Annotated
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from fastapi import Depends, APIRouter, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import Response, JSONResponse, RedirectResponse

from ..utils import token_handlers, authentication_handlers
from ..dependencies.token_dependencies import get_active_user
from ..models.user import UserModel

from app import config


__author__ = 'Ricardo'
__version__ = '1.0'


router = APIRouter(prefix='/authentication', tags=['Authentication'])


@router.get("/logout")
def logout(response:Response):
    response = RedirectResponse(url='http://127.0.0.1:8000/frontend/login', status_code= 302)
    return response


@router.post('/oauth/login', status_code=status.HTTP_200_OK)
async def get_access_token(form_data:Annotated[OAuth2PasswordRequestForm, Depends()]):

    user_found = await authentication_handlers.verify_user(form_data.username, form_data.password)
    access_token, refresh_token = token_handlers.create_tokens(user=user_found)

    return create_response(access_token, refresh_token)


@router.post('/oauth/refresh', status_code=status.HTTP_200_OK)
async def get_refresh_token(user:Annotated[UserModel, Depends(get_active_user)]):

    access_token, refresh_token = token_handlers.create_tokens(user=user)
    return create_response(access_token, refresh_token)


def create_response(access_token:str, refresh_token:str):

    return JSONResponse(content={
        'token_type':'bearer',
        'access_token':access_token,
        'expires_in':config.ACCESS_TOKEN_EXPIRE_SECONDS, 
        'refresh_token':refresh_token,
        'refresh_expires_in':config.REFRESH_TOKEN_EXPIRE_SECONDS
    })
