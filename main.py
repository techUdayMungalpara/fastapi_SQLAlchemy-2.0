import models
import logging
from fastapi import FastAPI,Depends
from pydantic import BaseModel
from typing import Any, AsyncGenerator, Annotated
from contextlib import asynccontextmanager

from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from database import async_session

from database import engine
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
    
    

@app.get('/all_user')
async def get_all(session:Annotated[AsyncSession,Depends(get_db)]):
    try:
        data=(await session.execute(select(models.User))).scalars().all()
        return data
    except Exception as e:
        logger.error(e)
        raise False

class UserIn(BaseModel):
    name:str
    email:str
    password:str
    is_admin:bool

@app.post('/add_user')
async def add_user(data:UserIn,session:Annotated[AsyncSession,Depends(get_db)]):
    add_user= models.User(**data.model_dump())
    await session.add(add_user)
    await session.commit()
    await session.refresh(add_user)
    return add_user
           
           
@app.patch('/update-user')
async def update_user(user_id:int,email: str,session:Annotated[AsyncSession,Depends(get_db)]):
    data=(await session.execute(select(models.User).where(models.User.user_id==user_id))).scalars().first()
    print(data.email)
    data.email='ai@gmail.com'
    await session.refresh(data)
    print(data.email,data,data.name)
    await session.commit()
    return data

