from typing import Annotated

from fastapi import Depends, Request

from app.utils.db_manager import DBManager
from app.utils.redis_manager import RedisManager
from app.services.auth import AuthService
from app.config.postgres.database import sessionmaker


async def db():
    async with DBManager(sessionmaker) as db:
        yield db
        
DBDep = Annotated[DBManager, Depends(db)]

async def redis():
    async with RedisManager(Request().app) as redis:
        yield
        
RedisDep = Annotated[RedisManager, Depends(redis)]

def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise Exception # исключение
    
    return token

def get_user(token: str = Depends(get_token)):
    try:
        user_id = AuthService().decode_token(token)
    except Exception:
        raise Exception # исключение
    
    return user_id

UserIdDep = Annotated[int, Depends(get_user)]