from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException

from contextlib import asynccontextmanager

from app.frontend.controller.routers import router as frontend_router
from app.api import router as api_router
from app.api.chatbot import OpenAISingleton, DatabaseSingleton


__author__ = 'Ricardo Robledo'
__version__ = '1.0'


@asynccontextmanager
async def lifespan(app:FastAPI):
    print('startup')
    OpenAISingleton()
    DatabaseSingleton()
    yield
    print('shutdown')

app = FastAPI(
    title="Customer complaints handler",
    description="API to chat about customer complaints and feedbacks",
    version="1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.mount('/static', StaticFiles(directory='app/frontend/frontend_templates/static'), name='static')
templates = Jinja2Templates(directory='app/frontend/frontend_templates/templates')


# 404 page
@app.exception_handler(404)
async def http_exception_handler(request, exc):
    return templates.TemplateResponse('404.html', {'request': request})


app.include_router(frontend_router)
app.include_router(api_router)
