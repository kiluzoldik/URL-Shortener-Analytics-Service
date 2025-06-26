from uuid import UUID
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.models.users import Users
from app.repositories.base import BaseRepository
from app.schemas.auth import UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = Users
    schema = UserWithHashedPassword

    async def user_with_hashed_password(self, name: str):
        query = select(self.model).filter_by(name=name)
        try:
            result = await self.session.execute(query)
            user = result.scalar_one()
        except NoResultFound as e:
            raise Exception from e # исключение
        
        return self.schema.model_validate(user, from_attributes=True)
    
    async def get_user_by_id(self, user_id: UUID):
        query = select(self.model).filter_by(id=user_id)
        try:
            result = await self.session.execute(query)
            user = result.scalar_one()
        except Exception as e:
            raise Exception # исключение
        
        return self.schema.model_validate(user, from_attributes=True)