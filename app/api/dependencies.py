from typing import Annotated
import asyncio

from fastapi import Depends, FastAPI, Request

from app.services.shortener import ShortenerService
from app.utils.db_manager import DBManager
from app.utils.redis_manager import RedisManager
from app.services.auth import AuthService
from app.config.postgres.database import sessionmaker


async def db():
    async with DBManager(sessionmaker) as db:
        yield db
        
DBDep = Annotated[DBManager, Depends(db)]

async def listener_channel_task(redis: RedisManager, db: DBDep):
    pubsub = redis.pubsub()
    await pubsub.psubscribe("__keyevent@0__:expired")
    try:
        print("Стою перед циклом")
        async for msg in pubsub.listen():
            print("Зашел в цикл")
            if msg["type"] != "pmessage":
                continue
            print(f"{msg=}")
            data = msg["data"]
            if isinstance(data, bytes):
                key = data.decode()
            else:
                key = str(data)
            print(f"{key=}")
            if not key.startswith("code:"):
                continue
            code = key.split(":", 1)[1]
            print(f"{code=}")
            print("Готовлю на запись")
            await ShortenerService(db, redis)._handle_expire(code)
            print("Записал")
    finally:
        await pubsub.punsubscribe("__keyevent@0__:expired")

async def redis_lifespan(app: FastAPI, db: DBDep = Depends(db)):
    async with RedisManager(app) as redis:
        print("Начало приложения")
        listener_task = asyncio.create_task(listener_channel_task(redis, db))
        yield
        print("Конец приложения")
        listener_task.cancel()
        
async def redis_dep():
    async with RedisManager() as redis:
        yield redis
        
RedisDep = Annotated[RedisManager, Depends(redis_dep)]

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
