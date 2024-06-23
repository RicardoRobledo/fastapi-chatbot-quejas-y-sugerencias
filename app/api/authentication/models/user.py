from typing import List, Optional
import datetime

from sqlalchemy import DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from app.api.base.models.base_models import BaseModel


__author__ = "Ricardo Robledo"
__version__ = "1.0"
__all__ = ["UserModel"]


class UserModel(BaseModel):

    __tablename__ = "users"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    username:Mapped[str] = mapped_column(VARCHAR(30), nullable=False, unique=True)
    password:Mapped[str] = mapped_column(VARCHAR(255), nullable=False, unique=True)
    is_active:Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_superuser:Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, username={self.username}, password={self.password}, is_active={self.is_active}, is_superuser={self.is_superuser}, created_at={self.created_at}, updated_at={self.updated_at})"
