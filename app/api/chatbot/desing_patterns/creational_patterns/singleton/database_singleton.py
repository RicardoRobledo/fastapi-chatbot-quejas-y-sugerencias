from sqlalchemy.sql import exists
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.api.authentication.models.user import UserModel
from app import config


__author__ = 'Ricardo'
__version__ = '0.1'


class DatabaseSingleton():
    """
    This class manage our connection to a database
    """


    __client = None


    @classmethod
    def __get_connection(cls):
        """
        This method create our client
        """

        Session = async_sessionmaker(bind=create_async_engine(config.DATABASE_URL, echo=True))

        return Session


    def __new__(cls, *args, **kwargs):
        
        if cls.__client==None:
            cls.__client = cls.__get_connection()

        return cls.__client


    @classmethod
    async def get_active_user(cls, username:str):
        """
        This method get an user
        """

        user = None

        async with cls.__client() as session:

            user = (
                await session.execute(select(UserModel).filter_by(username=username))
            ).scalars().first()
        
        return user


    @classmethod
    async def is_existing_user(cls, username:str):
        """
        This method verify that an user exists
        """

        user = False

        async with cls.__client() as session:

            user = (await session.execute(select(exists().where(UserModel.username==username)))).scalar()
        
        return user
