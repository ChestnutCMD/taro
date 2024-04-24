from datetime import datetime

from sqlalchemy import BigInteger, String, ForeignKey, DateTime, Integer
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from os import getenv

engine = create_async_engine(
    f"postgresql+asyncpg://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}@{getenv('DB_HOST')}/{getenv('DB_NAME')}",
    poolclass=NullPool)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String)
    token: Mapped[int] = mapped_column(default=3)
    email: Mapped[str] = mapped_column(String, nullable=True)


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    currency: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)


class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
