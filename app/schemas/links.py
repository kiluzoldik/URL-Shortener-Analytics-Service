from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class AddRequestLink(BaseModel):
    original_url: str
    expires_at: int
    
    
class AddLink(AddRequestLink):
    code: str
    short_link: str
    owner_id: UUID
    
    
class UpdateLink(BaseModel):
    code: str
    active: bool
    
    
class Link(BaseModel):
    id: int
    code: str
    original_url: str
    created_at: datetime
    deleted_at: Optional[datetime] = None
    expires_at: int = 300
    click_count: int = 0
    active: bool = False
    owner_id: UUID
    
    
class RedisLink(BaseModel):
    code: str
    link: str
    original_url: str
    expires_at: int
    