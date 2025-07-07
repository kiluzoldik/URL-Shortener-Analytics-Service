from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool.impl import NullPool

from app.config.config import settings


engine = create_async_engine(url=settings.DB_URL)
engine_null_pool = create_async_engine(settings.DB_URL, poolclass=NullPool)

sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)
sessionmaker_null_pool = async_sessionmaker(bind=engine_null_pool, expire_on_commit=False)

class Base(DeclarativeBase):
    pass