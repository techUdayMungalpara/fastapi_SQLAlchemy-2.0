from datetime import datetime
from typing import Annotated, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, Integer, String, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declarative_base,
    mapped_column,
    registry,
    relationship,
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(10))
    email: Mapped[str]
    password: Mapped[str]
    creater_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    status: Mapped[Optional[str]]
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    todo: Mapped[List["Todo"]] = relationship("Todo")


class Todo(Base):
    __tablename__ = "todo"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task: Mapped[str]
    user_fk: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
