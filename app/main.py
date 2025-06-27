from contextlib import asynccontextmanager
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI
import redis.asyncio as aioredis

from app.api.shortener import short_router
from app.api.auth import auth_router
from app.config.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = aioredis.from_url(
        url=settings.REDIS_URL,
        health_check_interval=30,
        decode_responses=True
    )
    await redis_client.ping()
    app.state.redis = redis_client
    try:
        yield
    finally:
        await redis_client.close()
    

app = FastAPI(title="URL Shortener", lifespan=lifespan)

app.include_router(short_router)
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", reload=True)