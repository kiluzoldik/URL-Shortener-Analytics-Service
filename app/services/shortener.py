from uuid import UUID
from string import ascii_letters
from random import choices, randint

from app.schemas.links import AddLink, AddRequestLink
from app.services.base import BaseService
from app.config.config import settings


class ShortenerService(BaseService):
    def _generate_code_for_link(self) -> str:
        length = randint(5, 8)
        code = choices(ascii_letters, k=length)
        
        return code
    
    async def add_link_to_redis(self, link: str) -> None:
        ...
    
    async def create_short_link(self, user_id: UUID, data: AddRequestLink) -> str:
        code = ShortenerService()._generate_code_for_link()
        new_data = AddLink(
            original_url=data.original_url,
            expires_at=data.expires_at,
            code=code,
            owner_id=user_id
        )
        await self.db.links.add_data(new_data)
        await self.add_link_to_redis()
        
        return f"{settings.BASE_URL}{code}"