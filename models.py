import datetime
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
    status: Mapped[Optional[str]]
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    

    