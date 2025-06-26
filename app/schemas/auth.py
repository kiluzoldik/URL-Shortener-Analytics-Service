from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class AddUser(BaseModel):
    name: str
    password: str
    
    
class DBUser(BaseModel):
    name: str
    hashed_password: str
    
    
class UserWithHashedPassword(BaseModel):
    id: UUID
    tg_id: Optional[int] = None
    name: str
    hashed_password: str
    
    
class User(BaseModel):
    id: UUID
    tg_id: Optional[str] = None
    name: str
    links: Optional[list[str]] = []