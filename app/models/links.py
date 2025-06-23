from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.postgres.database import Base

if TYPE_CHECKING:
    from app.models.users import Users


class Links(Base):
    __tablename__ = "links"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    original_url: Mapped[str] = mapped_column(nullable=False, unique=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    expires_at: Mapped[int] = mapped_column(nullable=True, unique=False)
    click_count: Mapped[int] = mapped_column(default=0)
    active: Mapped[bool] = mapped_column(default=True)
    
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    owner: Mapped["Users"] = relationship("Users", back_populates="links")