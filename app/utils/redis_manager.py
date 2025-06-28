from fastapi import FastAPI
import redis.asyncio as aioredis

from app.config.config import settings
from app.schemas.links import RedisLink


class RedisManager:
    redis_client = aioredis.from_url(
        url=settings.REDIS_URL,
        health_check_interval=30,
        decode_responses=True
    )
    
    def __init__(self, app: FastAPI):
        self.app = app
        
    async def __aenter__(self):
        await self.redis_client.ping()
        self.app.state.redis = self.redis_client
    
    async def __aexit__(self, *args):
        await self.redis_client.close()
        
    async def create_link(self, data: RedisLink) -> None:
        await self.redis_client.set(
            name=data.code,
            value={
                "link": data.link,
                "original_url": data.original_url,
                "clicks": 0,
            },
            ex=data.expires_at
        )
        
    async def get_link(self, code: str) -> dict:
        return await self.redis_client.get(code)
        
    async def delete_link(self, code: str) -> None:
        await self.redis_client.delete(code)
        
    async def click_count_increase(self, code: str) -> None:
        link_data: dict = await self.redis_client.get(code)
        await self.redis_client.set(
            name=code,
            value={
                "link": link_data.get("link"),
                "original_url": link_data.get("original_url"),
                "clicks": link_data.get("clicks") + 1,
            }
        )
        