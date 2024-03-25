from typing import Optional

from database.models import User, Transaction, Cart, async_session
from sqlalchemy import select, update


async def get_user(telegram_id: int) -> Optional[User | None]:
    """ Получение пользователя по ID """
    async with async_session() as session:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalars().one_or_none()
        return user


async def get_user_email(telegram_id: int) -> Optional[str | None]:
    """ Получение email пользователя """
    user = await get_user(telegram_id=telegram_id)
    return user.email


async def add_user(first_name, user_id):
    """ Добавление пользователя """
    async with async_session() as session:
        user = User(name=first_name, telegram_id=user_id)
        session.add(user)
        await session.commit()


async def add_user_email(telegram_id: int, email: str):
    """ Добавление Email пользователя"""
    async with async_session() as session:
        stmt = update(User).where(User.telegram_id == telegram_id).values({User.email: email})
        await session.execute(stmt)
        await session.commit()


async def debiting_token(telegram_id: int):
    """ Списание токенов """
    async with async_session() as session:
        stmt = update(User).where(User.telegram_id == telegram_id).values({User.token: User.token - 1})
        await session.execute(stmt)
        await session.commit()


async def add_token(telegram_id: int, count_token: int):
    """ Покупка токенов """
    async with async_session() as session:
        stmt = update(User).where(User.telegram_id == telegram_id).values({User.token: User.token + count_token})
        await session.execute(stmt)
        await session.commit()


async def update_tokens():
    """ Добавление 1 токена всем пользователям с балансом 0 """
    async with async_session() as session:
        stmt = update(User).where(User.token == 0).values({User.token: 1})
        await session.execute(stmt)
        await session.commit()


async def get_carts(cart_id: int):
    """ Получение карты по ID """
    async with async_session() as session:
        stmt = select(Cart).where(Cart.id == cart_id)
        result = await session.execute(stmt)
        cart = result.scalars().one_or_none()
        return cart


async def add_transaction(user_id, currency, price):
    """ Добавление транзакции """
    async with async_session() as session:
        transaction = Transaction(user_id=user_id, currency=currency, price=price)
        session.add(transaction)
        await session.commit()
