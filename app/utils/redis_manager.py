from fastapi import FastAPI
import redis.asyncio as aioredis

from app.config.config import settings
from app.schemas.links import RedisLink


class RedisManager:
    def __init__(self, app: FastAPI | None = None):
        self.app = app
        self.redis_client = aioredis.from_url(
            url=settings.REDIS_URL,
            health_check_interval=30,
            decode_responses=True
        )
        
    async def __aenter__(self):
        await self.redis_client.ping()
        
        return self
    
    async def __aexit__(self, *args):
        await self.redis_client.close()
        
    async def create_link(self, data: RedisLink) -> None:
        await self.redis_client.hset(f"code:{data.code}", mapping={
            "link": data.link,
            "original_url": data.original_url,
            "clicks": 0
        })
        await self.redis_client.expire(f"code:{data.code}", data.expires_at)
        
    async def get_link(self, code: str) -> dict:
        return await self.redis_client.hgetall(f"code:{code}")
        
    async def delete_link(self, code: str) -> None:
        await self.redis_client.delete(f"code:{code}")
        
    async def click_count_increase(self, code: str) -> None:
        await self.redis_client.hincrby(f"code:{code}", "clicks", 1)

    def pubsub(self):
        return self.redis_client.pubsub()