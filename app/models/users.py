from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.postgres.database import Base

if TYPE_CHECKING:
    from app.models.links import Links


class Users(Base):
    __tablename__ = "users"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    tg_id: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    hashed_password: Mapped[str]
    
    links: Mapped["Links"] = relationship("Links", back_populates="owner", cascade="all, delete-orphan")