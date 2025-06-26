import datetime
from uuid import UUID

from fastapi import Response
import jwt
from passlib.context import CryptContext
from sqlalchemy.exc import NoResultFound

from app.exceptions.api import InvalidAuthToken
from app.schemas.auth import DBUser, AddUser, User
from app.services.base import BaseService
from app.config.postgres.config import settings


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def verify_password(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)
    
    def password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt
    
    def decode_token(self, token: str) -> UUID:
        try:
            user_id = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.exceptions.InvalidTokenError:
            raise InvalidAuthToken
        
        return UUID(user_id["user_id"])
        
    async def registration(self, data: AddUser):
        hashed_password = AuthService().password_hash(data.password)
        new_user_data = DBUser(name=data.name, hashed_password=hashed_password)
        try:
            await self.db.users.add_data(new_user_data)
        except Exception:
            raise Exception # исключение
        await self.db.commit()
        
    async def login_user(self, response: Response, data: AddUser) -> str:
        try:
            user = await self.db.users.user_with_hashed_password(data.name)
        except NoResultFound:
            raise Exception # исключение
        if not self.verify_password(data.password, user.hashed_password):
            raise Exception # исключение
        access_token = AuthService().create_access_token({"user_id": str(user.id)})
        response.set_cookie("access_token", access_token)
        
        return access_token
        
    async def user_info(self, user_id: UUID) -> User:
        try:
            user = await self.db.users.get_user_by_id(user_id=user_id)
        except NoResultFound:
            raise Exception # исключение
        user_data = User(
            id=user.id,
            tg_id=user.tg_id,
            name=user.name,
        )
        
        return user_data
        
    async def logout_user(self, response: Response):
        response.delete_cookie("access_token")