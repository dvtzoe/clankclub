# Copied from https://github.com/grillazz/fastapi-sqlalchemy-asyncpg/blob/main/app/models/base.py

from asyncpg import UniqueViolationError  # pyright: ignore[reportMissingTypeStubs]
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    __tablename__: str

    async def save(self, db_session: AsyncSession):
        db_session.add(self)
        await db_session.flush()
        await db_session.refresh(self)
        return self

    async def delete(self, db_session: AsyncSession):
        try:
            await db_session.delete(self)
            return True
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)
            ) from ex

    async def update(self, **kwargs):  # pyright: ignore[reportMissingParameterType]
        try:
            for k, v in kwargs.items():
                setattr(self, k, v)
            return True
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)
            ) from ex

    async def save_or_update(self, db_session: AsyncSession):
        try:
            db_session.add(self)
            await db_session.flush()
            return True
        except IntegrityError as exception:
            if isinstance(exception.orig, UniqueViolationError):
                return await db_session.merge(self)
            else:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=repr(exception),
                ) from exception
