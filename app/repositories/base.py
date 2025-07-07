from asyncpg import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.repositories.mapper.mappers import LinkDataMapper


class BaseRepository:
    model = None
    mapper = LinkDataMapper
    
    def __init__(self, session):
        self.session = session
    
    async def add_data(self, data: BaseModel):
        query = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(query)
        except IntegrityError as e:
            if isinstance(e.orig.__cause__, UniqueViolationError):
                raise Exception from e # исключение
            else:
                raise e
        return result.scalar_one()
        
    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        try:
            result = await self.session.execute(query)
            data = result.scalar_one()
        except NoResultFound:
            raise Exception # исключение
        
        return self.mapper.map_to_domain_entity(data)
    
    async def get_all(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(obj) for obj in result.scalars().all()]
    
    async def update(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        query = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        try:
            await self.session.execute(query)
        except Exception as e:
            raise Exception # исключение
