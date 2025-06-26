import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.config.postgres.database import Base

if TYPE_CHECKING:
    from app.models.links import Links


class Users(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        index=True
    )
    tg_id: Mapped[Optional[str]] = mapped_column(unique=True, nullable=True, default=None)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    hashed_password: Mapped[str]
    
    links: Mapped["Links"] = relationship("Links", back_populates="owner", cascade="all, delete-orphan")