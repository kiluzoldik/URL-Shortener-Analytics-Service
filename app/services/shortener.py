from uuid import UUID
from string import ascii_letters
from random import choices, randint

from fastapi.responses import RedirectResponse

from app.schemas.links import AddLink, AddRequestLink, RedisLink
from app.services.base import BaseService
from app.config.config import settings


class ShortenerService(BaseService):
    def _generate_code_for_link(self) -> str:
        length = randint(5, 8)
        code = choices(ascii_letters, k=length)
        
        return code
    
    async def create_short_link(self, user_id: UUID, data: AddRequestLink) -> str:
        code = ShortenerService()._generate_code_for_link()
        short_link = f"{settings.BASE_URL}{code}"
        new_data = AddLink(
            original_url=data.original_url,
            expires_at=data.expires_at,
            code=code,
            short_link=short_link,
            owner_id=user_id
        )
        redis_data = RedisLink(
            code=code,
            link=short_link,
            original_url=new_data.original_url,
            expires_at=new_data.expires_at
        )
        await self.db.links.add_data(new_data)
        await self.redis.create_link(redis_data)
        
        return short_link
    
    async def redirect(self, code: str):
        link_data = await self.redis.get_link(code)
        original_url = link_data.get("original_url")
        await self.redis.click_count_increase(code)
        
        return RedirectResponse(url=original_url)