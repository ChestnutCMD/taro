from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import User
from database.requests import add_token, add_transaction, get_user
from utils.yookassa import create, check


async def buy_handler(call: CallbackQuery):
    if call.data == '10':
        price = '100.00'
    elif call.data == '20':
        price = '200.00'
    else:
        price = '500.00'

    user: User = await get_user(call.message.chat.id)
    payment_url, payment_id = create(price, call, user)

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='Оплатить',
        url=payment_url
    ))
    builder.add(types.InlineKeyboardButton(
        text='Проверить оплату',
        callback_data=f'check_{payment_id}'
    ))

    await call.message.answer(f"Счет на оплату {int(float(price)/10)} токенов сформирован!", reply_markup=builder.as_markup())


async def check_handler(callback: types.CallbackQuery):
    result = check(callback.data.split('_')[-1])
    if result:
        price = result.amount.value
        currency = result.amount.currency
        chat_id = int(result.metadata['chat_id'])
        user = await get_user(chat_id)
        await add_token(user.telegram_id, int(price / 10))
        await add_transaction(user_id=user.id, currency=currency, price=price)
        await callback.message.answer(f'Ваш баланс пополнен на {price/10} токенов')
    else:
        await callback.message.answer('Оплата еще не прошла или возникла ошибка')
    await callback.answer()


async def check_payment(telegram_id, price, currency):
    user = await get_user(telegram_id)
    await add_token(telegram_id, int(price / 10))
    await add_transaction(user_id=user.id, currency=currency, price=price)


