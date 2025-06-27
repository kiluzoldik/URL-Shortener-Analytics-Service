from app.models.links import Links
from app.repositories.base import BaseRepository
from app.schemas.links import Link


class LinksRepository(BaseRepository):
    model = Links
    schema = Link
    
    