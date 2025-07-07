from app.repositories.mapper.base import DataMapper
from app.models.links import Links
from app.schemas.links import Link


class LinkDataMapper(DataMapper):
    db_model = Links
    schema = Link
