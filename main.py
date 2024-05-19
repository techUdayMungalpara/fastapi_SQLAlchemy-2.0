import logging
import time
from contextlib import asynccontextmanager
from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, joinedload

import models
from database import async_session, engine
from models import Base

logger = logging.getLogger()


async def init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


logger.info("create all table")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:  # noqa: ARG001
    await init_models()
    yield


# async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session() as session:
#         try:
#             yield session
#         except  Exception as error:
#             logger.info(error)
#             await session.rollback()


async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session() as session, session.begin():
        yield session


app = FastAPI(lifespan=lifespan)


@app.get("/all_user")
async def get_all(session: Annotated[AsyncSession, Depends(get_db)]):
    try:
        data = (await session.execute(select(models.User))).scalars().all()
        return data
    except Exception as e:
        logger.error(e)
        raise False


class UserIn(BaseModel):
    name: str
    email: str
    password: str
    is_admin: bool


@app.post("/add_user")
async def add_user(data: UserIn, session: Annotated[AsyncSession, Depends(get_db)]):
    if data is None:
        raise HTTPException(status_code=404)
    add_user = models.User(**data.model_dump())
    session.add(add_user)
    await session.flush()
    await session.refresh(add_user)
    print(add_user, add_user.email)
    await session.commit()
    return add_user


@app.post("/add_user2")
async def add_user(data: UserIn, session: Annotated[AsyncSession, Depends(get_db)]):
    if data is None:
        raise HTTPException(status_code=404)
    add_user = models.User(**data.model_dump())
    session.add(add_user)
    await session.flush()
    await session.refresh(add_user)
    print(add_user, add_user.email)
    await session.commit()
    return add_user


@app.patch("/update-user")
async def update_user(
    user_id: int, email: str, session: Annotated[AsyncSession, Depends(get_db)]
):

    query = select(models.User).where(models.User.user_id == user_id)
    data = (await session.execute(query)).scalars().first()

    print(data.email)
    data.email = "ai@gmail.com"
    await session.refresh(data)
    print(data.email, data, data.name)
    await session.commit()
    return data


@app.get("/getsd")
async def update_user(user_id: int, session: Annotated[AsyncSession, Depends(get_db)]):
    query = select(models.User).filter(models.User.user_id == user_id)
    data = (await session.execute(query)).scalars().first()
    if data is None:
        raise HTTPException(status_code=404, detail="User not found")
    data.email = "ai@gmail.com"
    await session.refresh(data)
    print(data.email, data, data.name)
    await session.commit()
    print("hello")
    return data


#     order = db.query(models.Order).options(joinedload(models.Order.products)).filter(
# models.Order.order_id == order_id).first()


@app.get("/get_relationship")
async def get_user(user_id: int, session: Annotated[AsyncSession, Depends(get_db)]):
    query = (
        select(models.User)
        .options(joinedload(models.User.todo))
        .filter(models.User.user_id == user_id)
    )
    data = (await session.execute(query)).scalars().first()
    if data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return data


# <!-- https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html -->

# <!-- https://www.youtube.com/watch?v=Uym2DHnUEno -->


# https://docs.sqlalchemy.org/en/20/changelog/migration_20.htmlhttps://docs.sqlalchemy.org/en/20/changelog/migration_20.html

# https://blog.miguelgrinberg.com/post/what-s-new-in-sqlalchemy-2-0


# https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#order-by
