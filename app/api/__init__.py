from fastapi import APIRouter

from .authentication.controllers.routers import router as authentication_router
from .chatbot.controllers.routers import router as chatbot_router


__author__ = 'Ricardo'
__version__ = '1.0'


router = APIRouter(prefix='/api/v1', tags=['API'])
router.include_router(authentication_router)
router.include_router(chatbot_router)
