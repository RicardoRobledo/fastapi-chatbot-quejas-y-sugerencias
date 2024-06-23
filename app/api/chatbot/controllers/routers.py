from fastapi import BackgroundTasks, APIRouter, Request, Body, Depends, status
from fastapi.responses import JSONResponse

from ..services import chatbot_service
from ..desing_patterns.creational_patterns.singleton.openai_singleton import OpenAISingleton
from app.api.authentication import oauth2_scheme


__author__ = 'Ricardo Robledo'
__version__ = '1.0'


router = APIRouter(prefix='/chatbot', tags=['chatbot'])


@router.post('/message', status_code=status.HTTP_200_OK)
async def send_message(body:dict=Body(...), tokens:str=Depends(oauth2_scheme)):

    thread_id = body.get('thread_id')
    user_message = body.get('user_message')
    dates = body.get('dates')

    return JSONResponse(content={'msg':await chatbot_service.send_message(dates, thread_id, user_message)})


@router.get('/thread_id', status_code=status.HTTP_200_OK)
async def create_thread(request:Request):

    thread_id = await OpenAISingleton.create_thread()

    return JSONResponse(content={'thread_id':thread_id.id})


@router.post('/thread_id/{thread_id}', status_code=status.HTTP_200_OK)
async def delete_thread(thread_id:str):

    await OpenAISingleton.delete_thread(thread_id)

    return JSONResponse(content={})
