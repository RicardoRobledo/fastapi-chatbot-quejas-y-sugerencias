from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.api.authentication.models.user import UserModel

from app import config


__author__ = "Ricardo Robledo"
__version__ = "1.0"


router = APIRouter(prefix='/frontend')

templates = Jinja2Templates(directory='app/frontend/frontend_templates/templates')

 
@router.get('/chat')
async def get_home_page(request:Request):
    return templates.TemplateResponse('chat.html', {'request': request})

@router.get('/login')
async def get_login_page(request:Request):
    return templates.TemplateResponse('login.html', {'request': request})
